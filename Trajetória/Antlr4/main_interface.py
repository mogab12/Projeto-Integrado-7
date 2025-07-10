import sys
import os
from parse_code import GCodeInterpreter

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
    current_pos = (0.0, 0.0)  # Começa em (0, 0)

    for cmd in commands:
        type_cmd = cmd['type']
        coords = cmd['coords']

        # Pega as coordenadas X e Y ou usa a posição atual
        x = coords.get('X', current_pos[0])
        y = coords.get('Y', current_pos[1])

        # Comando G00 (movimento rápido)
        if type_cmd == "G00":
            # Atualiza a posição atual com as novas coordenadas
            current_pos = (x, y)
            points.append(current_pos)

        # Comando G01 (movimento linear)
        elif type_cmd == "G01":
            current_pos = (x, y)
            points.append(current_pos)

        # Comando G02 (movimento circular horário)
        elif type_cmd == "G02":
            # Para G02, esperamos as coordenadas X, Y e os parâmetros I, J
            I = coords.get('I', 0.0)
            J = coords.get('J', 0.0)
            current_pos = (x, y)
            points.append(current_pos)

    if not points:
        print("Nenhum ponto encontrado no G-code.")
        return

    # Caminho absoluto da pasta onde a interface está
    saida_path = os.path.join(os.path.dirname(__file__), "saida_tratada.txt")

    # Gravar os pontos no arquivo de saída
    with open(saida_path, "w") as f:
        for x, y in points:
            f.write(f"X{x:.2f} Y{y:.2f}\n")

    print(f"{len(points)} pontos salvos em {saida_path}")

if __name__ == "__main__":
    main()
