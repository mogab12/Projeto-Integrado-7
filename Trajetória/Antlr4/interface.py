import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import time
import subprocess
import serial  # Usando a biblioteca pyserial para comunicação serial

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

        # Conexão Serial via COM (substitua conforme necessário)
        self.client = serial.Serial('COM1', 9600, timeout=1)  # Ajuste a porta serial
        self.client.flush()  # Limpa o buffer serial

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
                    'mainang.py',  # Caminho relativo
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

            # Envia os pontos linha por linha para a Raspberry
            for linha in self.linhas:
                texto = linha.strip()
                self.client.write(texto.encode())  # Envia a linha via serial (ASCII)
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
            self.client.write(b"START")  # Envia o comando de iniciar desenho
            self.status_label.config(text="Comando de início enviado.", fg="blue")
        except Exception as e:
            self.status_label.config(text="Erro ao iniciar desenho.", fg="red")
            print(f"[ERRO iniciar] {e}")

    def toggle_pausa(self):
        try:
            if not self.pausado:
                self.client.write(b"PAUSE")  # Pausar
                self.status_label.config(text="Comando: Pausar", fg="orange")
            else:
                self.client.write(b"RESUME")  # Continuar
                self.status_label.config(text="Comando: Continuar", fg="blue")
            self.pausado = not self.pausado
        except Exception as e:
            self.status_label.config(text="Erro ao pausar/continuar.", fg="red")
            print(f"[ERRO pausa] {e}")

    def abortar(self):
        try:
            self.client.write(b"STOP")  # Envia o comando de abortar
            self.status_label.config(text="Desenho abortado.", fg="red")
        except Exception as e:
            self.status_label.config(text="Erro ao abortar.", fg="red")
            print(f"[ERRO abortar] {e}")

    def ler_posicao_atual(self):
        try:
            self.client.write(b"GET_POSITION")
            time.sleep(1)  # Espera resposta
            resposta = self.client.readline().decode()  # Lê a resposta do robô (caso tenha implementação)
            self.posicao_label.config(text=f"Posição atual: {resposta}")
        except Exception as e:
            print(f"[ERRO POSIÇÃO] {e}")
            self.posicao_label.config(text="Erro ao ler posição atual.")

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceGCode(root)
    root.mainloop()
