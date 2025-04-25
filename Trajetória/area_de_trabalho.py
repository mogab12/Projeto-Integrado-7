import numpy as np
import matplotlib.pyplot as plt
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

# Definindo A e B
A = np.array([0, 0])
B = np.array([243.2, 0])

# Gerar uma série de valores para r1 e r2
r1_values = np.linspace(0, 260, 1000)
r2_values = np.linspace(0, 260, 1000) 

# Lista para armazenar os pontos de interseção
pontos_interseccao = []

# Para cada combinação de r1 e r2, calcular a interseção
for r1 in r1_values:
    for r2 in r2_values:
        C = calcular_interseccao(A, B, r1, r2)
        if C is not None:
            pontos_interseccao.append(C)

# Convertendo a lista de pontos em um array numpy
pontos_interseccao = np.array(pontos_interseccao)

# Plotando os pontos de interseção
plt.figure(figsize=(8, 8))
plt.scatter(pontos_interseccao[:, 0], pontos_interseccao[:, 1], color='red', s=0.5, label="Pontos de Interseção")

# Adicionando os pontos A e B ao gráfico
plt.scatter(A[0], A[1], color='blue', s=100, label="Ponto A", edgecolors='black', zorder=5)
plt.scatter(B[0], B[1], color='green', s=100, label="Ponto B", edgecolors='black', zorder=5)

# Adicionando a circunferência
centro = (243.2/2, -100)  # Centro da circunferência
raio = 80  # Raio da circunferência
angulos = np.linspace(0, 2 * np.pi, 500)
circunferencia_x = centro[0] + raio * np.cos(angulos)
circunferencia_y = centro[1] + raio * np.sin(angulos)
plt.plot(circunferencia_x, circunferencia_y, color='purple', label="Circunferência")

# Triângulo equilátero com lado 150
lado = 150
R = lado / np.sqrt(3)  # Raio do círculo circunscrito ao triângulo

# Ângulos dos vértices do triângulo
angulo_base = np.pi / 2  # Orientação "em pé"
angulos_triangulo = angulo_base + np.array([0, 2*np.pi/3, 4*np.pi/3])

# Cálculo dos vértices (mantendo os nomes t1, t2, t3)
t1 = np.array([centro[0] + R * np.cos(angulos_triangulo[0]), centro[1] + R * np.sin(angulos_triangulo[0])])
t2 = np.array([centro[0] + R * np.cos(angulos_triangulo[1]), centro[1] + R * np.sin(angulos_triangulo[1])])
t3 = np.array([centro[0] + R * np.cos(angulos_triangulo[2]), centro[1] + R * np.sin(angulos_triangulo[2])])

# Plotando as linhas do triângulo
triangulo_x = [t1[0], t2[0], t3[0], t1[0]]
triangulo_y = [t1[1], t2[1], t3[1], t1[1]]
plt.plot(triangulo_x, triangulo_y, color='orange', label="Triângulo")

# Adicionando título e rótulos
plt.title("Área de Trabalho do Sistema")
plt.xlabel('X')
plt.ylabel('Y')

# Ajustando limites do gráfico
plt.xlim(-10, 260)
plt.ylim(-270, 10)

# Exibindo o gráfico
plt.legend()
plt.gca().set_aspect('equal', adjustable='box')
plt.grid(True)
plt.show()
