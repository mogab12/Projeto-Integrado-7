import math
import sys
import os
from parse_code import GCodeInterpreter

# Parâmetro: distância entre pontos interpolados (em mm)
STEP = 1.0

def interpolate_linear(start, end):
    x0, y0 = start
    x1, y1 = end
    dist = math.hypot(x1 - x0, y1 - y0)
    num_steps = max(int(dist / STEP), 1)

    points = []
    for i in range(num_steps + 1):
        t = i / num_steps
        x = x0 + t * (x1 - x0)
        y = y0 + t * (y1 - y0)
        points.append((x, y))
    return points

def interpolate_arc(start, end, I, J, cw=True):
    x0, y0 = start
    x1, y1 = end
    cx = x0 + I
    cy = y0 + J
    r = math.hypot(I, J)

    start_angle = math.atan2(y0 - cy, x0 - cx)
    end_angle = math.atan2(y1 - cy, x1 - cx)

    if math.isclose(x0, x1, abs_tol=1e-6) and math.isclose(y0, y1, abs_tol=1e-6):
        end_angle = start_angle + 2 * math.pi
    else:
        if cw:
            if end_angle > start_angle:
                end_angle -= 2 * math.pi
        else:
            if end_angle < start_angle:
                end_angle += 2 * math.pi

    total_angle = abs(end_angle - start_angle)
    arc_length = r * total_angle
    num_steps = max(int(arc_length / STEP), 1)

    points = []
    for i in range(num_steps + 1):
        t = i / num_steps
        theta = start_angle + t * (end_angle - start_angle)
        x = cx + r * math.cos(theta)
        y = cy + r * math.sin(theta)
        points.append((x, y))

    return points

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo.gcode>")
        return

    arquivo_gcode = sys.argv[1]
    interpreter = GCodeInterpreter()
    commands = interpreter.parse(arquivo_gcode)

    if not commands:
        print("Nenhum comando válido encontrado.")
        return

    points = []
    current_pos = (0.0, 0.0)

    for cmd in commands:
        type_cmd = cmd['type']
        coords = cmd['coords']

        x = coords.get('X', current_pos[0])
        y = coords.get('Y', current_pos[1])

        if type_cmd == "G00":
            current_pos = (x, y)
        elif type_cmd == "G01":
            segment = interpolate_linear(current_pos, (x, y))
            points.extend(segment)
            current_pos = (x, y)
        elif type_cmd.startswith("G02"):
            I = coords.get('I', 0.0)
            J = coords.get('J', 0.0)
            segment = interpolate_arc(current_pos, (x, y), I, J, cw=True)
            points.extend(segment)
            current_pos = (x, y)

    if not points:
        print("Nenhum ponto interpolado encontrado.")
        return

    # Caminho absoluto da pasta onde a interface está
    saida_path = os.path.join(os.path.dirname(__file__), "saida_tratada.txt")

    with open(saida_path, "w") as f:
        for x, y in points:
            f.write(f"X{x:.2f} Y{y:.2f}\n")

    print(f"{len(points)} pontos salvos em {saida_path}")

if __name__ == "__main__":
    main()
