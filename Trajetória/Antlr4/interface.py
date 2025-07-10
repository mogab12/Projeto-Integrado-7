import tkinter as tk
from tkinter import filedialog, messagebox
import serial 
import time
import subprocess
import sys
import threading


ser = None
PORTA_SERIAL = '/dev/ttyACM0'
BAUD_RATE = 115200


def serial_reader_thread(app, stop_event):
    """
    Thread que gerencia a conexão e a leitura da porta serial.
    """
    global ser # Usaremos a variável global 'ser'

    print("[THREAD] Leitor serial iniciado. Aguardando conexão da Pico...")
    
    while not stop_event.is_set():
        # --- Lógica de Conexão ---
        if ser is None or not ser.is_open:
            try:
                # Tenta abrir a porta
                ser = serial.Serial(PORTA_SERIAL, BAUD_RATE, timeout=1)
                print(f"[THREAD] Conectado com sucesso à porta {PORTA_SERIAL}!")
                app.status_label.config(text="Pico Conectada", fg="green")
            except serial.SerialException:
                # Se falhar, não faz nada e tenta de novo na próxima iteração
                app.status_label.config(text="Aguardando Pico na porta " + PORTA_SERIAL, fg="orange")
                time.sleep(2) # Espera 2 segundos antes de tentar de novo
                continue # Volta para o início do loop

        # --- Lógica de Leitura ---
        try:
            if ser.in_waiting > 0:
                line = ser.readline().decode('ascii', errors='ignore').strip()
                if line:
                    print(f"[PICO] {line}")
        except serial.SerialException:
            # A Pico foi desconectada
            print("[THREAD] Conexão perdida. Tentando reconectar...")
            app.status_label.config(text="Pico Desconectada!", fg="red")
            ser.close()
            ser = None # Força a tentativa de reconexão no próximo loop
            time.sleep(1)

    # Limpeza ao final da thread
    if ser and ser.is_open:
        ser.close()
    print("[THREAD] Leitor serial finalizado.")

def enviar_msg(msg_bytes):
    if ser and ser.is_open:
        ser.write(msg_bytes)
    else:
        print("[ERRO ENVIO] Não foi possível enviar. Pico não está conectada.")
        messagebox.showerror("Erro de Conexão", "A Raspberry Pi Pico não está conectada.")
    
#lrc é calculado para colocar no final da msg e conferir depois
def calcular_lrc(data_bytes):

    soma = sum(data_bytes)
    lrc = (-soma) & 0xFF
    return [ord(f"{lrc:02X}"[0]), ord(f"{lrc:02X}"[1])]



#aqui é encodado os valores do conteudo da msg para writefile
def ascii_hex_encode(texto):
    result = []
    for c in texto:
        byte_val = ord(c)  
        high_nibble = (byte_val >> 4) & 0x0F
        low_nibble = byte_val & 0x0F
        result.append(ord("0123456789ABCDEF"[high_nibble]))
        result.append(ord("0123456789ABCDEF"[low_nibble]))
    return result

# Adicione esta função mais simples para calcular o LRC
def calcular_lrc_byte_unico(data_bytes):
    """Calcula o LRC e retorna um único byte (inteiro)."""
    soma = sum(data_bytes)
    lrc = (-soma) & 0xFF
    return lrc

def enviar_comando_write_register(register_addr, value):
    """
    Função genérica para montar e enviar um comando Write Register (0x06).
    """
    try:
        # 1. Monta o payload binário
        payload_binario = bytearray()
        payload_binario.append(0x01) # Endereço
        payload_binario.append(0x06) # Função Write Register
        payload_binario.extend(register_addr.to_bytes(2, 'big'))
        payload_binario.extend(value.to_bytes(2, 'big'))

        # 2. Calcula o LRC
        lrc = calcular_lrc_byte_unico(payload_binario)
        
        # 3. Monta a string ASCII final
        payload_hex_str = payload_binario.hex().upper()
        msg_final_str = f":{payload_hex_str}{lrc:02X}\r\n"
        
        print(f"[PY->PICO] Enviando Write Register: {msg_final_str.strip()}")
        enviar_msg(msg_final_str.encode('ascii'))

    except Exception as e:
        print(f"[ERRO] Falha ao enviar comando Write Register: {e}")


def decode_register_value_ascii_hex(resposta):
    if len(resposta) < 15 or resposta[0] != ord(':'): # Resposta agora tem 15 chars: :010302[VALOR_4_HEX][LRC_2_HEX]\r\n
        print("Resposta inválida\n", resposta)
        return None

    # Pega os 4 bytes do valor do registrador (endereço 7 a 10)
    chars = "".join([chr(c) for c in resposta[7:11]])
    
    try:
        return int(chars, 16) # Converte string hex de 4 chars para int
    except ValueError:
        print("Erro na conversão ASCII→int")
        return None


    
def ler_resposta():
    print("[AVISO] ler_resposta() não é mais usada para leitura direta.")
    print("[AVISO] Verifique o console para a resposta da Pico.")
    # Vamos retornar um valor dummy por enquanto.
    # No futuro, isso pode ser implementado com uma Queue para comunicação inter-thread.
    time.sleep(0.5) # Simula o tempo de espera da resposta
    return 123 # Retorna um valor falso

class InterfaceGCode:
    def __init__(self, root):
        self.root = root
        self.root.title("Plotter G-code PI7")
        self.root.geometry("500x450")

        self.arquivo_path = None
        self.linhas = []
        self.linha_atual = 0
        self.pontos_enviados = False
        self.pausado = False

        self.status_label = tk.Label(root, text="Nenhum arquivo selecionado", fg="blue")
        self.status_label.pack(pady=10)

        self.selecionar_btn = tk.Button(root, text="Selecionar Arquivo G", command=self.selecionar_arquivo)
        self.selecionar_btn.pack(pady=5)

        self.enviar_btn = tk.Button(root, text="Enviar Pontos para Raspberry", command=self.enviar_pontos)
        self.enviar_btn.pack(pady=5)

        self.iniciar_btn = tk.Button(root, text="Iniciar Desenho", command=self.iniciar_desenho, bg="green", fg="white")
        self.iniciar_btn.pack(pady=5)

        self.pausar_btn = tk.Button(root, text="Pausar / Continuar", command=self.toggle_pausa, bg="orange")
        self.pausar_btn.pack(pady=5)

        self.abortar_btn = tk.Button(root, text="Abortar", command=self.abortar, bg="red", fg="white")
        self.abortar_btn.pack(pady=5)

        self.ler_posicao_atual_btn = tk.Button(root, text="Ler Posição Atual", command = self.ler_posicao_atual)
        self.ler_posicao_atual_btn.pack(pady=5)

        self.posicao_label = tk.Label(root, text="Posição atual: (x, y) = (?, ?)")
        self.posicao_label.pack(pady=15)

        self.stop_thread_event = threading.Event()
        self.reader_thread = threading.Thread(
            target=serial_reader_thread, 
            args=(self, self.stop_thread_event),
            daemon=True
        )
        self.reader_thread.start()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """Chamado quando a janela da interface é fechada."""
        print("Fechando a aplicação...")
        self.stop_thread_event.set()
        self.root.destroy()

    def selecionar_arquivo(self):
        self.arquivo_path = filedialog.askopenfilename(filetypes=[("Arquivos G-code", "*.gcode *.txt")])
        if self.arquivo_path:
            self.status_label.config(text="Arquivo selecionado. Gerando pontos...", fg="purple")
            try:
                subprocess.run([sys.executable, "main_interface.py", self.arquivo_path], check=True)
                self.status_label.config(text="Pontos gerados com sucesso.", fg="darkgreen")
                self.pontos_enviados = False
            except Exception as e:
                self.status_label.config(text="Erro ao gerar pontos.", fg="red")
                print(f"[ERRO main.py] {e}")
                self.pontos_enviados = False
        else:
            self.status_label.config(text="Nenhum arquivo selecionado", fg="blue")



    def enviar_pontos(self):
        try:
            # 1. LER OS PONTOS DO ARQUIVO E CONVERTER PARA BYTES
            program_data_bytes = bytearray()
            
            with open("saida_tratada.txt", "r") as f:
                for linha in f:
                    linha = linha.strip()
                    if not linha:
                        continue
                    
                    # Exemplo de linha: "X7.50 Y12.99"
                    try:
                        partes = linha.split() # Divide em ["X7.50", "Y12.99"]
                        coord_x_str = partes[0].replace('X', '')
                        coord_y_str = partes[1].replace('Y', '')

                        # Converte para inteiro * 100 (ex: 12.34 -> 1234)
                        # Usamos int16, então o valor deve estar entre -32768 e 32767
                        ponto_x_int = int(float(coord_x_str) * 100)
                        ponto_y_int = int(float(coord_y_str) * 100)
                        
                        # Converte para 2 bytes (big-endian, signed) e adiciona ao nosso array de bytes
                        program_data_bytes.extend(ponto_x_int.to_bytes(2, 'big', signed=True))
                        program_data_bytes.extend(ponto_y_int.to_bytes(2, 'big', signed=True))

                    except (ValueError, IndexError) as e:
                        print(f"AVISO: Linha ignorada no arquivo de pontos: '{linha}' | Erro: {e}")

            if not program_data_bytes:
                messagebox.showerror("Erro", "Nenhum ponto válido encontrado em saida_tratada.txt")
                return
                
            self.status_label.config(text=f"{len(program_data_bytes)//4} pontos prontos para desenho.", fg="green")
            
            # 2. MONTA O PAYLOAD BINÁRIO PARA O CÁLCULO DO LRC
            # Formato binário: [ADDR] [FUNC] [LEN_H] [LEN_L] [DADOS...]
            
            tamanho_dados = len(program_data_bytes)
            payload_binario = bytearray()
            payload_binario.append(0x01)  # Endereço do dispositivo
            payload_binario.append(0x15)  # Código da função: Write File
            payload_binario.extend(tamanho_dados.to_bytes(2, 'big')) # Tamanho dos dados (2 bytes)
            payload_binario.extend(program_data_bytes) # Os dados dos pontos
            
            # <<< ADICIONE ESTE BLOCO DE DEBUG AQUI >>>
            print(f"PYTHON DEBUG: Payload Binario para Envio (len={len(payload_binario)}): ", end="")
            for byte_val in payload_binario:
                print(f"{byte_val:02X} ", end="")
            print()
            # <<< FIM DO BLOCO DE DEBUG >>>

            # 3. CALCULA O LRC SOBRE O PAYLOAD BINÁRIO
            lrc = calcular_lrc_byte_unico(payload_binario)
            
            # 4. MONTA A STRING ASCII FINAL PARA ENVIO
            # Converte o payload binário para sua representação em string hexadecimal
            payload_hex_str = payload_binario.hex().upper()
            
            # Monta a mensagem final no formato Modbus ASCII
            msg_final_str = f":{payload_hex_str}{lrc:02X}\r\n"

            print(f"[PY->PICO] Enviando comando Write File ({len(msg_final_str)} chars): {msg_final_str.strip()}")
            ser.write(msg_final_str.encode('ascii'))
            
            self.pontos_enviados = True

        except FileNotFoundError:
            messagebox.showerror("Erro", "Arquivo 'saida_tratada.txt' não encontrado! Gere os pontos primeiro.")
            self.status_label.config(text="Erro: Arquivo de pontos não existe.", fg="red")
        except Exception as e:
            self.status_label.config(text="Erro ao enviar pontos.", fg="red")
            print(f"[ERRO envio pontos] {e}")
   


    def iniciar_desenho(self):
        if not self.pontos_enviados:
            messagebox.showwarning("Aviso", "Envie os pontos antes de iniciar.")
            return
        # Envia o comando para o registrador REG_START (1), com valor 0 (pode ser qualquer coisa)
        enviar_comando_write_register(register_addr=1, value=0)
        self.status_label.config(text="Comando de início enviado.", fg="blue")

    def toggle_pausa(self):
        if not self.pausado:
            # Envia comando para REG_SUSPEND (2)
            enviar_comando_write_register(register_addr=2, value=0)
            self.status_label.config(text="Comando: Pausar", fg="orange")
        else:
            # Envia comando para REG_RESUME (3)
            enviar_comando_write_register(register_addr=3, value=0)
            self.status_label.config(text="Comando: Continuar", fg="blue")
        self.pausado = not self.pausado

    def abortar(self):
        # Envia comando para REG_STOP (4)
        enviar_comando_write_register(register_addr=4, value=0)
        self.status_label.config(text="Desenho abortado.", fg="red")

    def ler_posicao_atual(self):
        try:
            # TESTE SIMPLES: Ler Registrador de Posição X (REG_X = 0x0009)
            
            # 1. Monta o payload binário para o cálculo do LRC
            # Formato binário: [ADDR] [FUNC] [REG_ADDR_H] [REG_ADDR_L] [COUNT_H] [COUNT_L]
            payload_binario = bytearray()
            payload_binario.append(0x01) # Endereço
            payload_binario.append(0x03) # Função Read Register
            payload_binario.append(0x00) # Endereço do Registrador (High)
            payload_binario.append(0x09) # Endereço do Registrador (Low) -> REG_X
            payload_binario.append(0x00) # Número de registradores a ler (High)
            payload_binario.append(0x01) # Número de registradores a ler (Low)

            # DEBUG: Imprime o payload binário
            print(f"PYTHON DEBUG (ReadReg): Payload Binario para Envio (len={len(payload_binario)}): ", end="")
            for byte_val in payload_binario:
                print(f"{byte_val:02X} ", end="")
            print()

            # 2. Calcula o LRC
            lrc = calcular_lrc_byte_unico(payload_binario)
            print(f"PYTHON DEBUG (ReadReg): LRC Calculado=0x{lrc:02X}")

            # 3. Monta a string ASCII final
            payload_hex_str = payload_binario.hex().upper()
            msg_final_str = f":{payload_hex_str}{lrc:02X}\r\n"

            print(f"[PY->PICO] Enviando comando Read Register: {msg_final_str.strip()}")
            ser.write(msg_final_str.encode('ascii'))

            x = ler_resposta()
            if x is None:
                self.posicao_label.config(text="Erro ao ler posição X.")
                return
            
            
            payload_binario = bytearray()
            payload_binario.append(0x01) # Endereço
            payload_binario.append(0x03) # Função Read Register
            payload_binario.append(0x00) # Endereço do Registrador (High)
            payload_binario.append(0x10) # Endereço do Registrador (Low) -> REG_X
            payload_binario.append(0x00) # Número de registradores a ler (High)
            payload_binario.append(0x01) # Número de registradores a ler (Low)

            # DEBUG: Imprime o payload binário
            print(f"PYTHON DEBUG (ReadReg): Payload Binario para Envio (len={len(payload_binario)}): ", end="")
            for byte_val in payload_binario:
                print(f"{byte_val:02X} ", end="")
            print()

            # 2. Calcula o LRC
            lrc = calcular_lrc_byte_unico(payload_binario)
            print(f"PYTHON DEBUG (ReadReg): LRC Calculado=0x{lrc:02X}")

            # 3. Monta a string ASCII final
            payload_hex_str = payload_binario.hex().upper()
            msg_final_str = f":{payload_hex_str}{lrc:02X}\r\n"

            print(f"[PY->PICO] Enviando comando Read Register: {msg_final_str.strip()}")
            ser.write(msg_final_str.encode('ascii'))

            y = ler_resposta()
            if y is None:
                self.posicao_label.config(text="Erro ao ler posição Y.")
                return

           
            self.posicao_label.config(text=f"Posição atual: (x, y) = ({x}, {y})")
            

        except Exception as e:
            print(f"[ERRO POSIÇÃO] {e}")
            self.posicao_label.config(text="Erro ao ler posição atual.")
   

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceGCode(root)
    root.mainloop()
