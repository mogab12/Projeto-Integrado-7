import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def calculate_f(P2):
    C = np.array([0, 0])
    D = np.array([246, 0])
    
    def safe_norm(v):
        norm = np.linalg.norm(v)
        return v if norm == 0 else v / norm
    
    c = safe_norm(C - P2)
    d = safe_norm(D - P2)

    f = safe_norm(c + d)
    return f

def is_valid_point(P1, tolerance=1e-5, max_iterations=100):
    A = np.array([8, 260])
    B = np.array([238, 260])

    if np.linalg.norm(P1 - A) > 280 or np.linalg.norm(P1 - B) > 280:
        return False

    L = 50
    f_prev = np.zeros(2)
    P2 = P1 

    for _ in range(max_iterations):
        f = calculate_f(P2)
        P2 = P1 + L * f
        
        if np.linalg.norm(f - f_prev) < tolerance:
            break
        f_prev = f
    
    # Verifica se os ângulos são maiores que 90 graus
    if np.dot(A - P1, f) >= 0 or np.dot(B - P1, f) >= 0:
        return False

    return True

def create_mesh():
    x = np.arange(0, 247, 1)
    y = np.arange(0, 241, 1)

    valid_points_x = []
    valid_points_y = []

    for x_val in x:
        for y_val in y:
            P1 = np.array([x_val, y_val])
            if is_valid_point(P1):
                valid_points_x.append(x_val)
                valid_points_y.append(y_val)

    return valid_points_x, valid_points_y

# Gerando e plotando a malha de pontos válidos
valid_points_x, valid_points_y = create_mesh()

fig, ax = plt.subplots(figsize=(7, 7))
ax.scatter(valid_points_x, valid_points_y, color='blue', s=1)

# Plota os pontos A, B, C, D
A = np.array([8, 260])
B = np.array([238, 260])
C = np.array([0, 0])
D = np.array([246, 0])

ax.plot(A[0], A[1], 'ro', label='A')
ax.plot(B[0], B[1], 'ro', label='B')
ax.plot(C[0], C[1], 'go', label='C')
ax.plot(D[0], D[1], 'go', label='D')

# Círculo de raio 80
circle_radius = 80
circle = patches.Circle((120, 145), circle_radius, fill=False, edgecolor='red', linewidth = 2)
ax.add_patch(circle)

# Triângulo equilátero
triangle_side = 150
height = np.sqrt(triangle_side**2 - (triangle_side/2)**2)
triangle = patches.Polygon([
    (120 - triangle_side/2, 145 - height/3),
    (120 + triangle_side/2, 145 - height/3),
    (120, 130 + 2*height/3)
], fill=False, edgecolor='orange', linewidth = 2)
ax.add_patch(triangle)

# Marca os centros
ax.plot(A[0], A[1], 'ro')
ax.plot(B[0], B[1], 'ro')

plt.title('Pontos Válidos no Sistema')
plt.xlabel('x')
plt.ylabel('y')
plt.xlim(-10, 250)
plt.ylim(-10, 270)
plt.grid(True)
ax.legend(loc='upper right')
plt.show()