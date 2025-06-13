import tkinter as tk
from tkinter import filedialog, messagebox
import serial
import threading
import time
import subprocess

# Configuração da porta serial
ser = serial.Serial(port='COM3', baudrate=9600, timeout=1)

def calcular_lrc(msg_ascii_bytes):
    soma = 0
    for i in range(0, len(msg_ascii_bytes), 2):
        par = chr(msg_ascii_bytes[i]) + chr(msg_ascii_bytes[i+1])
        soma += int(par, 16)
    lrc = (-soma) & 0xFF
    lrc_str = f"{lrc:02X}"
    return [ord(c) for c in lrc_str]

def enviar_msg(msg):
    ser.write(bytearray(msg))

def ler_resposta():
    return ser.read(32)

class InterfaceGCode:
    def __init__(self, root):
        self.root = root
        self.root.title("Interface G-Code")
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

        self.posicao_label = tk.Label(root, text="Posição atual: (x, y) = (?, ?)")
        self.posicao_label.pack(pady=10)

    def selecionar_arquivo(self):
        self.arquivo_path = filedialog.askopenfilename(filetypes=[("Arquivos G-code", "*.g *.txt")])
        if self.arquivo_path:
            self.status_label.config(text="Arquivo selecionado. Gerando pontos...", fg="purple")
            try:
                subprocess.run(["python", "main.py", self.arquivo_path], check=True) #Não entendi aquele path anterior, mas é só mudar. 
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

            for linha in self.linhas:
                texto = linha.strip()
                dados_ascii = [ord(c) for c in texto]
                tamanho = len(dados_ascii)
                tamanho_str = f"{tamanho:02X}"
                msg = [ord(c) for c in ":01"] + [ord(c) for c in "15"] + [ord(c) for c in tamanho_str]
                msg += dados_ascii
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
            msg = [ord(c) for c in ":010600010100"]
            msg += calcular_lrc(msg[1:])
            msg += [0x0D, 0x0A]
            enviar_msg(msg)
            self.status_label.config(text="Comando de início enviado.", fg="blue")
        except Exception as e:
            self.status_label.config(text="Erro ao iniciar desenho.", fg="red")
            print(f"[ERRO iniciar] {e}")

    def toggle_pausa(self):
        try:
            if not self.pausado:
                msg = [ord(c) for c in ":010600020100"]
                self.status_label.config(text="Comando: Pausar", fg="orange")
            else:
                msg = [ord(c) for c in ":010600030100"]
                self.status_label.config(text="Comando: Continuar", fg="blue")
            msg += calcular_lrc(msg[1:])
            msg += [0x0D, 0x0A]
            enviar_msg(msg)
            self.pausado = not self.pausado
        except Exception as e:
            self.status_label.config(text="Erro ao pausar/continuar.", fg="red")
            print(f"[ERRO pausa] {e}")

    def abortar(self):
        try:
            msg = [ord(c) for c in ":010600040100"]
            msg += calcular_lrc(msg[1:])
            msg += [0x0D, 0x0A]
            enviar_msg(msg)
            self.status_label.config(text="Desenho abortado.", fg="red")
        except Exception as e:
            self.status_label.config(text="Erro ao abortar.", fg="red")
            print(f"[ERRO abortar] {e}")

    def ler_posicao_atual(self):
        try:
            msg = [ord(c) for c in ":01030009"] #Mudar depois do teste. 
            msg += calcular_lrc(msg[1:])
            msg += [0x0D, 0x0A]
            enviar_msg(msg)
            resposta = ler_resposta()
            if not resposta:
                self.posicao_label.config(text="Erro na leitura da posição.")
            else:
                #Mudar depois pois o formato da resposta é diferente
                dados = ' '.join([f"{b:02X}" for b in resposta])
                self.posicao_label.config(text=f"Resposta: {dados}")
        except Exception as e:
            print(f"[ERRO POSIÇÃO] {e}")
            self.posicao_label.config(text="Erro ao ler posição atual.")

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceGCode(root)
    root.mainloop()
