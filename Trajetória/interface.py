import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import time
import subprocess
from pymodbus.client.serial import ModbusSerialClient

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

        self.client = ModbusSerialClient(
            port='COM3',  # Ajuste para porta correta
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
                subprocess.run([
                    "python",
                    "C:/Users/angel/Codigosc/pi7/Projeto-Integrado-7-master/Projeto-Integrado-7-master/Trajetória/main.py",  # Caminho absoluto ajustado
                    self.arquivo_path
                ], check=True)
                self.status_label.config(text="Pontos gerados com sucesso.", fg="darkgreen")
                self.pontos_enviados = False
            except Exception as e:
                self.status_label.config(text="Erro ao gerar pontos.", fg="red")
                print(f"[ERRO main.py] {e}")
        else:
            self.status_label.config(text="Nenhum arquivo selecionado", fg="blue")

    def enviar_pontos(self):
        try:
            with open("saida_tratada.txt", "r") as f:
                self.linhas = f.readlines()
            self.linha_atual = 0
            self.status_label.config(text=f"{len(self.linhas)} pontos prontos para desenho.", fg="green")

            # Envia os pontos linha por linha para registradores (exemplo: registrador base 2000)
            for linha in self.linhas:
                texto = linha.strip()
                registradores = [ord(c) for c in texto]
                self.client.write_registers(address=2000, values=registradores, unit=1)
                time.sleep(0.05)  # pequena pausa entre envios

            self.pontos_enviados = True

        except Exception as e:
            self.status_label.config(text="Erro ao enviar pontos.", fg="red")
            print(f"[ERRO envio pontos] {e}")

    def iniciar_desenho(self):
        if not self.pontos_enviados:
            messagebox.showwarning("Aviso", "Envie os pontos antes de iniciar.")
            return

        try:
            self.client.write_register(address=1000, value=1, unit=1)  # Comando: iniciar
            self.status_label.config(text="Comando de início enviado.", fg="blue")
        except Exception as e:
            self.status_label.config(text="Erro ao iniciar desenho.", fg="red")
            print(f"[ERRO iniciar] {e}")

    def toggle_pausa(self):
        try:
            if not self.pausado:
                self.client.write_register(address=1000, value=2, unit=1)  # Pausar
                self.status_label.config(text="Comando: Pausar", fg="orange")
            else:
                self.client.write_register(address=1000, value=4, unit=1)  # Continuar
                self.status_label.config(text="Comando: Continuar", fg="blue")
            self.pausado = not self.pausado
        except Exception as e:
            self.status_label.config(text="Erro ao pausar/continuar.", fg="red")
            print(f"[ERRO pausa] {e}")

    def abortar(self):
        try:
            self.client.write_register(address=1000, value=3, unit=1)  # Comando: abortar
            self.status_label.config(text="Desenho abortado.", fg="red")
        except Exception as e:
            self.status_label.config(text="Erro ao abortar.", fg="red")
            print(f"[ERRO abortar] {e}")

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
