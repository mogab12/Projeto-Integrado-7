import tkinter as tk
from tkinter import filedialog, messagebox
import serial 
import time
import subprocess
import sys



ser = None
if "--mock" in sys.argv: #para testar localnent python interce_piffer.py --mock
    class MockSerial:
        def __init__(self, *args, **kwargs):
            print("[MOCK] Porta serial simulada inicializada")

        def write(self, data):
            print("[MOCK] Dados enviados:", data)

        def read(self, n=1):
            print(f"[MOCK] Lendo {n} bytes")
            return bytes([0x00] * n)

        def close(self):
            print("[MOCK] Porta serial fechada")

    ser = MockSerial()
else: #para testar no hardware (por hora usarei a COM5, verificar depois qual é a da picoW quando conectada)
    ser = serial.Serial(port='COM5', baudrate=115200, timeout=1)



    
#lrc é calculado para colocar no final da msg e conferir depois
def calcular_lrc(data_bytes):

    soma = sum(data_bytes)
    lrc = (-soma) & 0xFF
    return [ord(f"{lrc:02X}"[0]), ord(f"{lrc:02X}"[1])]

def enviar_msg(msg):
    ser.write(bytearray(msg))

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

#função usada para decodificar a resposta da picow quando pede para ler registrador. Nesse caso traduz só os bytes 7,8 que contem 
#o valor do registrador lido.
def decode_register_value_ascii_hex(resposta):
    
    if len(resposta) < 11 or resposta[0] != ord(':'): #se a resposta não começar com o padrao definido no codigo da picow
        print("Resposta inválida")
        return None

    #aqui ta pegando só os bytes do valor do registrador    
    char_high = chr(resposta[7])
    char_low  = chr(resposta[8])

    #concatena
    hex_str = char_high + char_low

    #converte de hex para int
    try:
        return int(hex_str, 16)
    except ValueError:
        print("Erro na conversão ASCII→int")
        return None

def ler_resposta():
    resposta_bruta = ser.read(13)#sao 13 bytes de resposta da processreadregister (depois posso generalizar para todas as respostas)
    return decode_register_value_ascii_hex(resposta_bruta)
    


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

    def selecionar_arquivo(self):
        self.arquivo_path = filedialog.askopenfilename(filetypes=[("Arquivos G-code", "*.gcode *.txt")])
        if self.arquivo_path:
            self.status_label.config(text="Arquivo selecionado. Gerando pontos...", fg="purple")
            try:
                subprocess.run([sys.executable, "mainang.py", self.arquivo_path], check=True)
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
            with open("saida_tratada.txt", "r") as f:
                self.linhas = f.readlines()

            self.status_label.config(text=f"{len(self.linhas)} pontos prontos para desenho.", fg="green")

            #esse join deixa tudo na mesma linha, o strip tira os espaços, o replace remove o primeiro argumento e coloca o segundo no lugar
            texto = "".join(self.linhas).replace("\n", "").strip()
                    
            #aqui é deixada no formato correto a parte importante da mensgaem
            data_ascii_hex = ascii_hex_encode(texto)
            #tem que dividir por dois pq a função de cima dobrou o numero de bytes apos o encoding
            tamanho = len(data_ascii_hex) // 2 
            tamanho_hex = f"{tamanho:02X}"

            #esse ord(c) o valor em decimal que representa o char c pela tabea Ascii, por exemplo ord('A') = 65 = 0x41
            msg = [ord(c) for c in ":01"] + [ord(c) for c in "15"] + [ord(c) for c in tamanho_hex]
            msg += data_ascii_hex
            msg += calcular_lrc(msg[1:])
            msg += [0x0D, 0x0A]
            
            enviar_msg(msg)
            time.sleep(0.05)
            self.pontos_enviados = True

        except Exception as e:
            self.status_label.config(text="Erro ao enviar pontos.", fg="red")
            print(f"[ERRO envio pontos] {e}")



    def iniciar_desenho(self):
        if not self.pontos_enviados:
            messagebox.showwarning("Aviso", "Envie os pontos antes de iniciar.")
            return
        try:
            base_str = ":010600010100"
            msg = [ord(c) for c in base_str]
            lrc = calcular_lrc(msg[1:]) #pulando o :
            msg += lrc + [0x0D, 0x0A]
            enviar_msg(msg)
            self.status_label.config(text="Comando de início enviado.", fg="blue")
        except Exception as e:
            self.status_label.config(text="Erro ao iniciar desenho.", fg="red")
            print(f"[ERRO iniciar] {e}")

    def toggle_pausa(self):
        try:
            if not self.pausado:
                base_str = ":010600020100"
                self.status_label.config(text="Comando: Pausar", fg="orange")
            else:
                base_str = ":010600030100"
                self.status_label.config(text="Comando: Continuar", fg="blue")
            msg =[ord(C) for c in base_str]
            lrc = calcular_lrc(msg[1:])
            msg += lrc + [0x0D, 0x0A]
            enviar_msg(msg)
            self.pausado = not self.pausado
        except Exception as e:
            self.status_label.config(text="Erro ao pausar/continuar.", fg="red")
            print(f"[ERRO pausa] {e}")

    def abortar(self):
        try:
            base_str = ":010600040100"
            msg = [ord(c) for c in base_str]
            lrc = calcular_lrc([ord(c) for c in base_str])
            msg += lrc + [0x0D, 0x0A]
            enviar_msg(msg)
            self.status_label.config(text="Desenho abortado.", fg="red")
        except Exception as e:
            self.status_label.config(text="Erro ao abortar.", fg="red")
            print(f"[ERRO abortar] {e}")

    def ler_posicao_atual(self):
        try:
            #primeiro consulta x
            base_str = ":01030009"
            msg = [ord(c) for c in base_str]
            lrc = calcular_lrc([ord(c) for c in base_str])
            msg += lrc + [0x0D, 0x0A]
            enviar_msg(msg)
            resposta = ler_resposta()
            if not resposta:
                self.posicao_label.config(text="Erro na leitura da posição.")
            else:
                #por hora não vou usar
                #dados = ' '.join([f"{b:02X}" for b in resposta])
                self.posicao_label.config(text=f"x: {resposta}")
            #agora consulta y
            base_str = ":01030010"
            msg = [ord(c) for c in base_str]
            lrc = calcular_lrc([ord(c) for c in base_str])
            msg += lrc + [0x0D, 0x0A]
            enviar_msg(msg)
            resposta = ler_resposta()
            if not resposta:
                self.posicao_label.config(text="Erro na leitura da posição.")
            else:
                #por hora não vou usar
                #dados = ' '.join([f"{b:02X}" for b in resposta])
          
                
                self.posicao_label.config(text=f"y: {resposta}")

        except Exception as e:
            print(f"[ERRO POSIÇÃO] {e}")
            self.posicao_label.config(text="Erro ao ler posição atual.")

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceGCode(root)
    root.mainloop()
