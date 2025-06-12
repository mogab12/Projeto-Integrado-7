import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import time
import subprocess
import serial  # Usando a biblioteca pyserial para comunicação serial
import struct

# Função para calcular o CRC-16 (utilizado no protocolo MODBUS)
def modbus_crc(data):
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return struct.pack('<H', crc)

# Função para enviar o comando via MODBUS manualmente
def send_modbus_command(client, slave_id, function_code, data, register_address):
    message = bytearray()
    message.append(slave_id)
    message.append(function_code)
    message.extend(struct.pack('>H', register_address))
    message.extend(data)

    crc = modbus_crc(message)
    message.extend(crc)

    client.write(message)
    time.sleep(0.5)

    response = client.read(client.in_waiting)
    if response:
        print(f"Resposta recebida: {response}")
    else:
        print("Nenhuma resposta recebida.")

# Função para enviar os comandos de controle para a Raspberry
def send_control_command(client, command, register_address):
    data = bytearray()
    if command == "START":
        data.extend(struct.pack('>H', 1))
        send_modbus_command(client, 1, 0x06, data, register_address)
    elif command == "PAUSE":
        data.extend(struct.pack('>H', 1))
        send_modbus_command(client, 1, 0x06, data, register_address)
    elif command == "RESUME":
        data.extend(struct.pack('>H', 0))
        send_modbus_command(client, 1, 0x06, data, register_address)
    elif command == "STOP":
        data.extend(struct.pack('>H', 0))
        send_modbus_command(client, 1, 0x06, data, register_address)

# Função para enviar as coordenadas via MODBUS
def send_coordinates_to_raspberry(client, pontos, register_base_x, register_base_y):
    try:
        for i, (x, y) in enumerate(pontos):
            reg_x = register_base_x + i
            reg_y = register_base_y + i

            data_x = bytearray()
            data_x.extend(struct.pack('>H', int(x * 100)))
            send_modbus_command(client, 1, 0x06, data_x, reg_x)

            data_y = bytearray()
            data_y.extend(struct.pack('>H', int(y * 100)))
            send_modbus_command(client, 1, 0x06, data_y, reg_y)

            time.sleep(0.0005)

        print(f"{len(pontos)} pontos enviados com sucesso.")

    except Exception as e:
        print(f"Erro ao enviar coordenadas: {e}")

# Classe da Interface Gráfica
class InterfaceGCode:
    def __init__(self, root):
        self.root = root
        self.root.title("Interface G-Code")
        self.root.geometry("500x450")

        self.arquivo_path = None
        self.linhas = []
        self.linha_atual = 0
        self.pontos_enviados = False
        self.enviando = False
        self.abortado = False
        self.pausado = False
        self.terminou = False  # Sinalizador para indicar se o desenho terminou
        self.lendo_posicao = False  # Controle de leitura da posição

        # Conexão Serial via COM (ajuste conforme necessário)
        self.client = serial.Serial('COM1', 115200, timeout=1)
        self.client.flush()

        # Elementos da interface
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

        self.posicao_label = tk.Label(root, text="Posição atual: (x, y) = (?, ?)")
        self.posicao_label.pack(pady=10)

    def selecionar_arquivo(self):
        self.arquivo_path = filedialog.askopenfilename(filetypes=[("Arquivos G-code", "*.g *.txt")])
        if self.arquivo_path:
            self.status_label.config(text="Arquivo selecionado. Gerando pontos...", fg="purple")
            try:
                subprocess.run([  # Chama o main.py para gerar pontos
                    "python",
                    "mainang.py",  # Caminho absoluto
                    self.arquivo_path
                ], check=True)
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
            self.linha_atual = 0
            self.status_label.config(text=f"{len(self.linhas)} pontos prontos para desenho.", fg="green")

            # Defina os registradores de controle
            reg_control = 1000  # Registrador de controle START/PAUSE/RESUME/STOP
            reg_x = 2000  # Registrador para coordenada X
            reg_y = 2001  # Registrador para coordenada Y

            # Envia os pontos linha por linha para a Raspberry
            for linha in self.linhas:
                texto = linha.strip()
                send_modbus_command(self.client, 1, 0x10, texto.encode(), reg_control)  # Envia a linha via serial (ASCII)
                time.sleep(0.0005)  # pequena pausa entre envios

            self.pontos_enviados = True

        except Exception as e:
            self.status_label.config(text="Erro ao enviar pontos.", fg="red")
            print(f"[ERRO envio pontos] {e}")

    def iniciar_desenho(self):
        if not self.pontos_enviados:
            messagebox.showwarning("Aviso", "Envie os pontos antes de iniciar.")
            return

        try:
            send_control_command(self.client, "START", 1000)  # Envia o comando para iniciar o desenho
            self.status_label.config(text="Comando de início enviado.", fg="blue")
            self.terminou = False  # Resetando a flag de término
            self.lendo_posicao = True  # Ativando a leitura contínua da posição
            # Inicia a thread de leitura das coordenadas
            threading.Thread(target=self.ler_posicao_continuamente, daemon=True).start()
        except Exception as e:
            self.status_label.config(text="Erro ao iniciar desenho.", fg="red")
            print(f"[ERRO iniciar] {e}")

    def toggle_pausa(self):
        try:
            if not self.pausado:
                send_control_command(self.client, "PAUSE", 1001)  # Envia comando para pausar
                self.status_label.config(text="Comando: Pausar", fg="orange")
            else:
                send_control_command(self.client, "RESUME", 1001)  # Envia comando para continuar
                self.status_label.config(text="Comando: Continuar", fg="blue")
            self.pausado = not self.pausado
        except Exception as e:
            self.status_label.config(text="Erro ao pausar/continuar.", fg="red")
            print(f"[ERRO pausa] {e}")

    def abortar(self):
        try:
            send_control_command(self.client, "STOP", 1002)  # Envia comando para abortar
            self.status_label.config(text="Desenho abortado.", fg="red")
            self.terminou = True  # Marcando que o desenho terminou
            self.lendo_posicao = False  # Parando a leitura contínua de coordenadas
        except Exception as e:
            self.status_label.config(text="Erro ao abortar.", fg="red")
            print(f"[ERRO abortar] {e}")

    def ler_posicao_continuamente(self):
        while not self.terminou:
            if self.lendo_posicao:
                # Lê os registradores X e Y
                self.ler_posicao_atual(2000, 2001)
                time.sleep(1)

    def ler_posicao_atual(self, register_x, register_y):
        try:
            # Lê o registrador X
            message = bytearray()
            message.append(1)  # Endereço do escravo
            message.append(0x03)  # Função 0x03 - Leitura de registradores
            message.extend(struct.pack('>H', register_x))  # Endereço do registrador de X
            message.extend(struct.pack('>H', 1))  # Número de registradores
            crc = modbus_crc(message)
            message.extend(crc)
            self.client.write(message)
            time.sleep(1)  # Aguarda resposta
            resposta = self.client.read(5)
            if resposta:
                x_val = struct.unpack('>H', resposta[3:5])[0]
                x_coord = x_val / 100.0  # Ajuste para coordenada
            # Lê o registrador Y
            message = bytearray()
            message.append(1)  # Endereço do escravo
            message.append(0x03)  # Função 0x03
            message.extend(struct.pack('>H', register_y))
            message.extend(struct.pack('>H', 1))
            crc = modbus_crc(message)
            message.extend(crc)
            self.client.write(message)
            time.sleep(1)
            resposta = self.client.read(5)
            if resposta:
                y_val = struct.unpack('>H', resposta[3:5])[0]
                y_coord = y_val / 100.0

            self.posicao_label.config(text=f"Posição atual: (x, y) = ({x_coord}, {y_coord})")

        except Exception as e:
            print(f"[ERRO POSIÇÃO] {e}")
            self.posicao_label.config(text="Erro ao ler posição atual.")

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceGCode(root)
    root.mainloop()
