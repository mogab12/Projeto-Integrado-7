import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def calculate_f(P2):
    C = np.array([0, 0])
    D = np.array([240, 0])

    c = (C - P2) / np.linalg.norm(C - P2)
    d = (D - P2) / np.linalg.norm(D - P2)

    f = (c + d) / np.linalg.norm(c + d)
    return f, c, d

def is_valid_point(P1, f):
    A = np.array([0, 200])
    B = np.array([240, 200])

    if np.linalg.norm(P1 - A) > 350 or np.linalg.norm(P1 - B) > 350:
        return False

    if np.dot(A - P1, f) >= 0 or np.dot(B - P1, f) >= 0:
        return False

    return True

def update(val):
    P1_x = slider_x.val
    P1_y = slider_y.val
    P1 = np.array([P1_x, P1_y])

    P2 = P1
    for _ in range(100):
        f, c, d = calculate_f(P2)
        P2 = P1 + 30 * f
    
    if is_valid_point(P1, f):
        P1_color = 'blue'
    else:
        P1_color = 'red'

    P1_point.set_color(P1_color)
    P1_point.set_data([P1[0]], [P1[1]])
    P2_point.set_data([P2[0]], [P2[1]])
    vector_AP1.set_data([A[0], P1[0]], [A[1], P1[1]])
    vector_BP1.set_data([B[0], P1[0]], [B[1], P1[1]])
    vector_f.set_data([P2[0], P2[0] + 10*f[0]], [P2[1], P2[1] + 10*f[1]])
    vector_c.set_data([P2[0], P2[0] + 50*c[0]], [P2[1], P2[1] + 50*c[1]])
    vector_d.set_data([P2[0], P2[0] + 50*d[0]], [P2[1], P2[1] + 50*d[1]])

    fig.canvas.draw_idle()

A = np.array([0, 200])
B = np.array([240, 200])

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)
ax.set_xlim(-50, 290)
ax.set_ylim(-50, 250)
ax.grid(True)

ax.plot(A[0], A[1], 'ro', label='A')
ax.plot(B[0], B[1], 'ro', label='B')
ax.plot(0, 0, 'go', label='C')
ax.plot(240, 0, 'go', label='D')

P1_point, = ax.plot([0], [0], 'bo', label='P1')
P2_point, = ax.plot([0], [0], 'ko', label='P2')
vector_AP1, = ax.plot([], [], 'r-', label='A-P1')
vector_BP1, = ax.plot([], [], 'b-', label='B-P1')
vector_f, = ax.plot([], [], 'g-', label='f')
vector_c, = ax.plot([], [], 'm-', label='c')
vector_d, = ax.plot([], [], 'y-', label='d')

ax_x = plt.axes([0.25, 0.1, 0.65, 0.03])
ax_y = plt.axes([0.25, 0.15, 0.65, 0.03])

slider_x = Slider(ax_x, 'P1 x', 0, 240, valinit=120)
slider_y = Slider(ax_y, 'P1 y', 0, 200, valinit=100)

slider_x.on_changed(update)
slider_y.on_changed(update)

ax.legend(loc='upper right')
update(None)
plt.show()