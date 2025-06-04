# Generated from GCode.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .GCodeParser import GCodeParser
else:
    from GCodeParser import GCodeParser

# This class defines a complete listener for a parse tree produced by GCodeParser.
class GCodeListener(ParseTreeListener):

    # Enter a parse tree produced by GCodeParser#program.
    def enterProgram(self, ctx:GCodeParser.ProgramContext):
        pass

    # Exit a parse tree produced by GCodeParser#program.
    def exitProgram(self, ctx:GCodeParser.ProgramContext):
        pass


    # Enter a parse tree produced by GCodeParser#statement.
    def enterStatement(self, ctx:GCodeParser.StatementContext):
        pass

    # Exit a parse tree produced by GCodeParser#statement.
    def exitStatement(self, ctx:GCodeParser.StatementContext):
        pass


    # Enter a parse tree produced by GCodeParser#paramList.
    def enterParamList(self, ctx:GCodeParser.ParamListContext):
        pass

    # Exit a parse tree produced by GCodeParser#paramList.
    def exitParamList(self, ctx:GCodeParser.ParamListContext):
        pass


    # Enter a parse tree produced by GCodeParser#parameter.
    def enterParameter(self, ctx:GCodeParser.ParameterContext):
        pass

    # Exit a parse tree produced by GCodeParser#parameter.
    def exitParameter(self, ctx:GCodeParser.ParameterContext):
        pass


    # Enter a parse tree produced by GCodeParser#lineNumber.
    def enterLineNumber(self, ctx:GCodeParser.LineNumberContext):
        pass

    # Exit a parse tree produced by GCodeParser#lineNumber.
    def exitLineNumber(self, ctx:GCodeParser.LineNumberContext):
        pass


    # Enter a parse tree produced by GCodeParser#codFunc.
    def enterCodFunc(self, ctx:GCodeParser.CodFuncContext):
        pass

    # Exit a parse tree produced by GCodeParser#codFunc.
    def exitCodFunc(self, ctx:GCodeParser.CodFuncContext):
        pass


    # Enter a parse tree produced by GCodeParser#coordX.
    def enterCoordX(self, ctx:GCodeParser.CoordXContext):
        pass

    # Exit a parse tree produced by GCodeParser#coordX.
    def exitCoordX(self, ctx:GCodeParser.CoordXContext):
        pass


    # Enter a parse tree produced by GCodeParser#coordY.
    def enterCoordY(self, ctx:GCodeParser.CoordYContext):
        pass

    # Exit a parse tree produced by GCodeParser#coordY.
    def exitCoordY(self, ctx:GCodeParser.CoordYContext):
        pass


    # Enter a parse tree produced by GCodeParser#coordI.
    def enterCoordI(self, ctx:GCodeParser.CoordIContext):
        pass

    # Exit a parse tree produced by GCodeParser#coordI.
    def exitCoordI(self, ctx:GCodeParser.CoordIContext):
        pass


    # Enter a parse tree produced by GCodeParser#coordJ.
    def enterCoordJ(self, ctx:GCodeParser.CoordJContext):
        pass

    # Exit a parse tree produced by GCodeParser#coordJ.
    def exitCoordJ(self, ctx:GCodeParser.CoordJContext):
        pass


    # Enter a parse tree produced by GCodeParser#number.
    def enterNumber(self, ctx:GCodeParser.NumberContext):
        pass

    # Exit a parse tree produced by GCodeParser#number.
    def exitNumber(self, ctx:GCodeParser.NumberContext):
        pass


    # Enter a parse tree produced by GCodeParser#lineEnd.
    def enterLineEnd(self, ctx:GCodeParser.LineEndContext):
        pass

    # Exit a parse tree produced by GCodeParser#lineEnd.
    def exitLineEnd(self, ctx:GCodeParser.LineEndContext):
        pass


    # Enter a parse tree produced by GCodeParser#sign.
    def enterSign(self, ctx:GCodeParser.SignContext):
        pass

    # Exit a parse tree produced by GCodeParser#sign.
    def exitSign(self, ctx:GCodeParser.SignContext):
        pass



del GCodeParser