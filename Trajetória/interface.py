import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import time
import subprocess
from pymodbus.client.serial import ModbusSerialClient



# Os registradores vamos precisar mudar para os que vamos usar
class InterfaceGCode:
    def __init__(self, root):
        self.root = root
        self.root.title("Interface G-Code")
        self.root.geometry("500x400")

        self.arquivo_path = None
        self.linhas = []
        self.linha_atual = 0
        self.enviando = False
        self.abortado = False

        # Conexão Modbus via porta serial
        self.client = ModbusSerialClient(
            port='COM3',         # Se alguem quiser testar no linux, tem que mudar essa linha
            baudrate=9600,
            timeout=1,
            stopbits=1,
            bytesize=8,
            parity='N'
        )
        self.client.connect()

        self.status_label = tk.Label(root, text="Nenhum arquivo selecionado", fg="blue")
        self.status_label.pack(pady=10)

        self.selecionar_btn = tk.Button(root, text="Selecionar Arquivo G", command=self.selecionar_arquivo)
        self.selecionar_btn.pack(pady=5)

        self.enviar_parser_btn = tk.Button(root, text="Enviar para ANTLR", command=self.enviar_para_antlr)
        self.enviar_parser_btn.pack(pady=5)

        self.iniciar_btn = tk.Button(root, text="Iniciar", command=self.iniciar_envio, bg="green", fg="white")
        self.iniciar_btn.pack(pady=5)

        self.parar_btn = tk.Button(root, text="Parar", command=self.parar_envio, bg="orange")
        self.parar_btn.pack(pady=5)

        self.abortar_btn = tk.Button(root, text="Abortar", command=self.abortar_envio, bg="red", fg="white")
        self.abortar_btn.pack(pady=5)

        self.posicao_label = tk.Label(root, text="Posição atual: (x, y) = (?, ?)")
        self.posicao_label.pack(pady=10)

    def selecionar_arquivo(self):
        self.arquivo_path = filedialog.askopenfilename(filetypes=[("Arquivos G-code", "*.g *.txt")])
        if self.arquivo_path:
            self.status_label.config(text=f"Arquivo selecionado: {self.arquivo_path}", fg="green")
            self.abortado = False
        else:
            self.status_label.config(text="Nenhum arquivo selecionado", fg="blue")

    def enviar_para_antlr(self):
        if not self.arquivo_path:
            messagebox.showwarning("Aviso", "Selecione um arquivo primeiro.")
            return

        self.status_label.config(text="Executando parser ANTLR...", fg="purple")

        try:
            # Temos que substituir a linha abaixo pelo parser gerado pelo ANTLR
            # subprocess.run(["java", "-jar", "antlr_parser.jar", self.arquivo_path], check=True)
            subprocess.run(["python", "parser.py", self.arquivo_path], check=True)

            with open("saida_tratada.txt", "r") as f:
                self.linhas = f.readlines()
            self.linha_atual = 0
            self.status_label.config(text=f"Parser OK! {len(self.linhas)} linhas carregadas.", fg="darkgreen")
        except Exception as e:
            self.status_label.config(text="Erro ao executar parser.", fg="red")
            print(f"[ERRO ANTLR] {e}")

    def iniciar_envio(self):
        if not self.linhas:
            messagebox.showwarning("Aviso", "Use o parser antes de iniciar.")
            return

        if self.linha_atual >= len(self.linhas):
            self.status_label.config(text="Arquivo já finalizado.", fg="gray")
            return

        if not self.enviando:
            self.enviando = True
            threading.Thread(target=self.enviar_linhas).start()
            self.status_label.config(text="Enviando via MODBUS...", fg="blue")

            # Envia comando "iniciar" para registrador de controle
            self.client.write_register(address=1000, value=1, unit=1)

    def enviar_linhas(self):
        while self.enviando and self.linha_atual < len(self.linhas):
            if self.abortado:
                break

            linha = self.linhas[self.linha_atual].strip()
            print(f"Enviando linha {self.linha_atual + 1}: {linha}")

            # Converte string para códigos ASCII (16 bits por registrador)
            registradores = [ord(c) for c in linha]
            self.client.write_registers(address=2000, values=registradores, unit=1)

            self.linha_atual += 1

            self.ler_posicao_atual()  # FC03

            time.sleep(0.5)  # simula tempo entre linhas

        if self.linha_atual >= len(self.linhas):
            self.status_label.config(text="Envio finalizado.", fg="blue")
            self.enviando = False
            self.client.write_register(address=1000, value=0, unit=1)  # "encerrar"

    def parar_envio(self):
        if self.enviando:
            self.enviando = False
            self.status_label.config(text=f"Parado na linha {self.linha_atual + 1}", fg="orange")
            self.client.write_register(address=1000, value=2, unit=1)  # comando de pausa

    def abortar_envio(self):
        self.enviando = False
        self.abortado = True
        self.linha_atual = 0
        self.status_label.config(text="Envio abortado.", fg="red")
        self.client.write_register(address=1000, value=3, unit=1)  # comando de abortar

    def ler_posicao_atual(self):
        try:
            result = self.client.read_holding_registers(address=3000, count=2, unit=1)
            if result.isError():
                self.posicao_label.config(text="Erro na leitura da posição.")
            else:
                x = result.registers[0]
                y = result.registers[1]
                self.posicao_label.config(text=f"Posição atual: (x, y) = ({x}, {y})")
        except Exception as e:
            print(f"[ERRO POSIÇÃO] {e}")
            self.posicao_label.config(text="Erro ao ler posição atual.")

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceGCode(root)
    root.mainloop()
