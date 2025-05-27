rec = "{{0.000000, 0}, {0.025600, 41}, {0.051201, 52}, {0.076800, 96}, {0.102400, 136}, {0.127998, 138}, {0.153600, 173}, {0.179200, 182}, {0.204800, 187}, {0.230400, 210}, {0.255996, 210}, {0.281600, 216}, {0.307200, 230}, {0.332800, 232}, {0.358400, 231}, {0.384000, 239}, {0.409600, 244}, {0.435192, 242}, {0.460800, 249}, {0.486400, 252}, {0.511992, 251}, {0.537600, 254}, {0.563200, 258}, {0.588800, 259}, {0.614400, 257}, {0.640000, 260}, {0.665600, 264}, {0.691200, 265}, {0.716800, 262}, {0.742400, 265}, {0.768000, 268}, {0.793600, 268}, {0.819200, 266}, {0.844800, 268}, {0.870384, 271}, {0.896000, 271}, {0.921600, 270}, {0.947200, 272}, {0.972800, 273}, {0.998400, 270}}"

# Remover as chaves externas e substituir chaves internas por colchetes
rec = rec.replace("{{", "[").replace("}}", "]").replace("{", "[").replace("}", "]")

# Avaliar a string como uma lista Python
lista = eval(rec)

print(lista)

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Separar os dados
tempo = np.array([item[0] for item in lista])
valor = np.array([item[1] for item in lista])

# Definir a função de primeira ordem
def resposta_1ordem(t, A, tau):
    return A * (1 - np.exp(-t / tau))

# Chute inicial para A e tau
p0 = [max(valor), 0.1]

# Ajustar os parâmetros
parametros, _ = curve_fit(resposta_1ordem, tempo, valor, p0=p0)
A_fit, tau_fit = parametros

# Gerar curva ajustada
tempo_fit = np.linspace(tempo.min(), tempo.max(), 500)
valor_fit = resposta_1ordem(tempo_fit, A_fit, tau_fit)

# Plotar os dados e o ajuste
plt.figure(figsize=(10, 5))
plt.plot(tempo, valor, 'o', label='Dados originais')
plt.plot(tempo_fit, valor_fit, '-', label=f'Ajuste 1ª ordem\nK={A_fit:.2f}, τ={tau_fit:.3f}', color='red')
plt.title('Resposta Excitação Motor')
plt.xlabel('Tempo (s)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
