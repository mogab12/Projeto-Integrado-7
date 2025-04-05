import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# Função para calcular a interseção das duas circunferências
def calcular_interseccao(A, B, r1, r2):
    # Distância entre A e B
    d = np.linalg.norm(B - A)

    # Caso as circunferências se toquem
    if d > r1 + r2 or d < abs(r1 - r2):
        return None  # Não há interseção
    
    # Ponto de interseção (considerando uma solução simplificada)
    a = (r1**2 - r2**2 + d**2) / (2 * d)
    h = np.sqrt(r1**2 - a**2)
    
    # Ponto C (única interseção simplificada)
    Px = A[0] + a * (B[0] - A[0]) / d
    Py = A[1] + a * (B[1] - A[1]) / d
    
    # O ponto de interseção será perpendiculamente ao segmento AB
    Cx = Px + h * (B[1] - A[1]) / d
    Cy = Py - h * (B[0] - A[0]) / d
    
    return np.array([Cx, Cy])

# Função de atualização do gráfico com base nos sliders
def update(val):
    r1 = slider_r1.val
    r2 = slider_r2.val
    
    C = calcular_interseccao(A, B, r1, r2)
    
    if C is not None:
        Cx, Cy = C
        # Adicionando o ponto C à lista de rastros
        rastros.append([Cx, Cy])
        
        # Atualizando a posição do ponto C
        ponto_C.set_data([Cx], [Cy])  # Passando como lista

        # Atualizando os segmentos AC e BC
        linha_AC.set_data([A[0], Cx], [A[1], Cy])
        linha_BC.set_data([B[0], Cx], [B[1], Cy])
        
        # Atualizando o rastro
        rastros_linha.set_data(*zip(*rastros))  # Convertendo a lista de rastros para x e y
        
        # Atualizando o gráfico
        fig.canvas.draw_idle()

# Função para apagar o desenho
def apagar_desenho(event):
    # Limpar os rastros
    rastros.clear()
    
    # Limpar o ponto C
    ponto_C.set_data([], [])
    
    # Limpar os segmentos
    linha_AC.set_data([], [])
    linha_BC.set_data([], [])
    
    # Limpar a linha do rastro
    rastros_linha.set_data([], [])
    
    # Atualizando o gráfico
    fig.canvas.draw_idle()

# Definindo os pontos A e B
A = np.array([0, 0])
B = np.array([100, 0])

# Inicializando a figura e os eixos
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(-10, 110)
ax.set_ylim(-80, 10)  # Limite do eixo Y ajustado
ax.set_aspect('equal', 'box')
ax.set_title("Simulação Trajetória PI7")

# Adicionando a grade ao gráfico
ax.grid(True)

# Plotando os pontos A e B
ax.plot(A[0], A[1], 'go', label='A (0, 0)')
ax.plot(B[0], B[1], 'bo', label='B (100, 0)')

# Inicializando os segmentos AC e BC
linha_AC, = ax.plot([], [], 'r-', label='Segmento AC')
linha_BC, = ax.plot([], [], 'g-', label='Segmento BC')

# Inicializando o ponto C
ponto_C, = ax.plot([], [], 'mo', label='Ponto C')

# Inicializando a linha do rastro
rastros_linha, = ax.plot([], [], 'b--', label='Rastro de C')

# Lista para armazenar os rastros
rastros = []

# Adicionando os sliders para r1 e r2
ax_r1 = plt.axes([0.15, 0.02, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slider_r1 = Slider(ax_r1, 'Tamanho L1', 1.0, 100.0, valinit=50.0)
slider_r1.on_changed(update)

ax_r2 = plt.axes([0.15, 0.06, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slider_r2 = Slider(ax_r2, 'Tamanho L2', 1.0, 100.0, valinit=50.0)
slider_r2.on_changed(update)

# Adicionando o botão para apagar o desenho
ax_apagar = plt.axes([0.8, 0.02, 0.15, 0.04])  # Ajustando a posição do botão
botao_apagar = Button(ax_apagar, 'Apagar Desenho')
botao_apagar.on_clicked(apagar_desenho)

# Chamando a função de atualização inicial para definir C, AC e BC
update(None)

# Exibindo o gráfico
plt.legend()
plt.show()
