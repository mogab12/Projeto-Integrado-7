from svgpathtools import svg2paths
import numpy as np

# Carregar o arquivo SVG
file_name = "monalisa.svg"
paths, attributes = svg2paths(file_name)

# Inicializar lista para coordenadas
coordinates = []

# Iterar pelos elementos do SVG e extrair pontos
for path in paths:
    for segment in path:
        # Dividir segmentos em partes menores (ex.: curvas)
        points = [segment.point(t) for t in np.linspace(0, 1, num=1000)] 
        for point in points:
            coordinates.append((point.real, point.imag))  # Ponto real e imaginário representam X e Y

# Lista de pontos
# Convertendo para numpy array
coordinates = np.array(coordinates)
coordinates = coordinates/4
coordinates[:, 1] = coordinates[:, 1] * -1

coordinates[:,0] += 60
print("Coordenadas extraídas:")
print(coordinates)

# Reduzir o número de coordenadas em 5 vezes, calculando a média de 5 coordenadas consecutivas
reduced_coordinates = []
for i in range(0, len(coordinates), 100):
    # Pegar grupos de 5 coordenadas
    group = coordinates[i:i+5]
    
    # Calcular a média apenas se o grupo tiver 5 elementos
    if len(group) == 5:
        avg_x = np.mean(group[:, 0])
        avg_y = np.mean(group[:, 1])
        reduced_coordinates.append((avg_x, avg_y))

coordinates = np.array(reduced_coordinates)


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from math import sqrt

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

# Função para calcular a transformação linear de x, y para r1, r2
def calcular_transformacao_linear(x, y, A, B):
    r1 = sqrt(x**2 + (A[1] - y)**2)
    r2 = sqrt((B[0] - A[0] - x)**2 + (B[1] - y)**2)
    return r1, r2

# Função para discretizar uma circunferência
def discretizar_circunferencia(centro, raio, num_pontos=100):
    # Gerar os ângulos discretos (variando de 0 a 2*pi)
    angulos = np.linspace(0, 2 * np.pi, num_pontos)
    
    # Calcular as coordenadas (x, y) para cada ângulo
    pontos = [(centro[0] + raio * np.cos(angulo), centro[1] + raio * np.sin(angulo)) for angulo in angulos]
    
    return pontos

# Função de animação
def update(frame):
    # Limpar os gráficos a cada quadro
    ponto_C_plot.set_data([], [])
    linha_rastro.set_data([], [])
    segmento_AC.set_data([], [])
    segmento_BC.set_data([], [])
    
    # Obter o ponto C para a animação
    ponto_atual = coordinates[frame]
    x_C, y_C = ponto_atual
    
    # Calcular r1 e r2 para o ponto atual
    r1, r2 = calcular_transformacao_linear(x_C, y_C, A, B)
    
    # Retransformando o ponto C usando r1 e r2 para verificar a precisão do método
    x_C, y_C = calcular_interseccao(A,B,r1,r2)[0], calcular_interseccao(A,B,r1,r2)[1]

    # Atualizar os gráficos de r1 e r2
    r1_vals.append(r1)
    r2_vals.append(r2)
    
    # Traçar o ponto C (com rastro)
    
    rastro_x.append(x_C)
    rastro_y.append(y_C)
    linha_rastro.set_data(rastro_x, rastro_y)
    
    # Atualizar a posição do ponto C
    ponto_C_plot.set_data([x_C], [y_C])  # Passando listas com um único valor
    
    # Calcular os segmentos AC e BC
    segmento_AC.set_data([A[0], x_C], [A[1], y_C])
    segmento_BC.set_data([B[0], x_C], [B[1], y_C])
    
    # Calcular as distâncias AC e BC
    dist_AC = np.linalg.norm(np.array([A[0], A[1]]) - np.array([x_C, y_C]))
    dist_BC = np.linalg.norm(np.array([B[0], B[1]]) - np.array([x_C, y_C]))
    
    # Atualizar os textos com as distâncias AC e BC
    texto_AC.set_text(f"AC: {dist_AC:.2f}")
    texto_BC.set_text(f"BC: {dist_BC:.2f}")
    
    # Atualizar o gráfico dos raios r1 e r2
    ax_r1.clear()
    ax_r2.clear()
    
    # Plotando os raios r1 e r2 ao longo do tempo
    ax_r1.plot(range(len(r1_vals)), r1_vals, label="r1")
    ax_r2.plot(range(len(r2_vals)), r2_vals, label="r2")
    
    ax_r1.set_title("Comprimento r1")
    ax_r2.set_title("Comprimento r2")
    ax_r1.legend()
    ax_r2.legend()
    
    return ponto_C_plot, linha_rastro, segmento_AC, segmento_BC, texto_AC, texto_BC

# Definindo os pontos A e B
A = np.array([0, 0])
B = np.array([243.2, 0])

num_pontos = len(coordinates)  # Número de pontos a serem animados
# Inicializando as listas para o rastro e os gráficos de r1 e r2
rastro_x, rastro_y = [], []
r1_vals, r2_vals = [], []

# Inicializando a figura e os eixos
fig, (ax_main, ax_r1, ax_r2) = plt.subplots(1, 3, figsize=(15, 5))

# Configuração do gráfico principal
ax_main.set_xlim(-10, 260)
ax_main.set_ylim(-250, 10)
ax_main.set_aspect('equal', 'box')
ax_main.set_title("Trajetória Personalizada PI7")
ax_main.set_xlabel("X")
ax_main.set_ylabel("Y")
ax_main.grid(True)

# Plotando os pontos A e B
ax_main.plot(A[0], A[1], 'go', label='A (0, 0)')
ax_main.plot(B[0], B[1], 'bo', label='B (10, 0)')

# Inicializando o ponto C, o rastro e os segmentos AC e BC
ponto_C_plot, = ax_main.plot([], [], 'mo', label='Ponto C')
linha_rastro, = ax_main.plot([], [], 'r-', label='Rastro de C')
segmento_AC, = ax_main.plot([], [], 'g-', label='Segmento AC')
segmento_BC, = ax_main.plot([], [], 'b-', label='Segmento BC')

# Adicionando os textos de distâncias AC e BC
texto_AC = ax_main.text(0.05, 0.95, '', transform=ax_main.transAxes, fontsize=12, verticalalignment='top', color='green')
texto_BC = ax_main.text(0.05, 0.90, '', transform=ax_main.transAxes, fontsize=12, verticalalignment='top', color='blue')

# Configuração dos gráficos de r1 e r2
ax_r1.set_xlim(0, num_pontos)
ax_r1.set_ylim(0, 30)
ax_r2.set_xlim(0, num_pontos)
ax_r2.set_ylim(0, 30)

# Função de animação
ani = FuncAnimation(fig, update, frames=num_pontos, interval=30, blit=False)

# Exibindo o gráfico
plt.tight_layout()
plt.show()
