import sys
from antlr4 import *
from GCodeLexer import GCodeLexer
from GCodeParser import GCodeParser

class GCodeInterpreter:
    def __init__(self):
        self.commands = []
        self.current_line = 0

    def parse(self, file_path):
        try:
            input_stream = FileStream(file_path)
            lexer = GCodeLexer(input_stream)
            stream = CommonTokenStream(lexer)
            parser = GCodeParser(stream)
            tree = parser.program()

            # Aqui imprimimos a árvore de parsing:
            print(tree.toStringTree(recog=parser))

            self._extract_commands(tree)
            return self.commands

        except FileNotFoundError:
            print(f"Erro: Arquivo '{file_path}' não encontrado!")
            return None
        except Exception as e:
            print(f"Erro ao analisar G-code: {str(e)}")
            return None


    def _extract_commands(self, node):
        from GCodeParser import GCodeParser

        if isinstance(node, TerminalNode):
            return

        if isinstance(node, GCodeParser.LineNumberContext):
            self.current_line = int(node.INT(0).getText())
            return

        if isinstance(node, GCodeParser.CodFuncContext):
            self.current_type = node.getText()
            return

        if isinstance(node, GCodeParser.StatementContext):
            command = {
                'line': self.current_line,
                'type': None,
                'coords': {}
            }

            cmd_func = node.codFunc()
            if cmd_func:
                command['type'] = cmd_func.getText()

            param_list = node.paramList()
            if param_list:
                for param in param_list.parameter():
                    if param.coordX():
                        x_val = self._extract_number(param.coordX().number())
                        command['coords']['X'] = float(x_val)
                    elif param.coordY():
                        y_val = self._extract_number(param.coordY().number())
                        command['coords']['Y'] = float(y_val)
                    elif param.coordI():
                        i_val = self._extract_number(param.coordI().number())
                        command['coords']['I'] = float(i_val)
                    elif param.coordJ():
                        j_val = self._extract_number(param.coordJ().number())
                        command['coords']['J'] = float(j_val)

            if command['type']:
                self.commands.append(command)
            return

        for child in node.getChildren():
            self._extract_commands(child)

    def _extract_number(self, number_ctx):
        sign = number_ctx.sign().getText() if number_ctx.sign() else ''
        if number_ctx.INT():
            return f"{sign}{number_ctx.INT().getText()}"
        return f"{sign}{number_ctx.FLOAT().getText()}"

def print_commands(commands):
    if not commands:
        print("Nenhum comando encontrado.")
        return

    print("\nComandos G-code analisados:")
    print("-" * 50)
    for cmd in commands:
        line_info = f"Linha {cmd['line']}: {cmd['type']}"
        coords_info = ", ".join([f"{axis}{value}" for axis, value in cmd['coords'].items()])
        print(f"{line_info.ljust(15)} | Coordenadas: {coords_info}")
    print("-" * 50)
    print(f"Total de comandos: {len(commands)}")

def main():
    if len(sys.argv) < 2:
        print("Uso: python parse_code.py <arquivo.gcode>")
        return

    interpreter = GCodeInterpreter()
    commands = interpreter.parse(sys.argv[1])

    if commands:
        print_commands(commands)

if __name__ == "__main__":
    main()
