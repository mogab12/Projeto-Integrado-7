# Generated from GCode.g4 by ANTLR 4.13.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,15,86,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,1,0,4,0,
        28,8,0,11,0,12,0,29,1,0,1,0,1,1,1,1,1,1,3,1,37,8,1,1,1,1,1,1,2,4,
        2,42,8,2,11,2,12,2,43,1,3,1,3,1,3,1,3,3,3,50,8,3,1,4,1,4,4,4,54,
        8,4,11,4,12,4,55,1,5,1,5,1,5,1,5,3,5,62,8,5,1,6,1,6,1,6,1,7,1,7,
        1,7,1,8,1,8,1,8,1,9,1,9,1,9,1,10,3,10,77,8,10,1,10,1,10,1,11,3,11,
        82,8,11,1,12,1,12,1,12,0,0,13,0,2,4,6,8,10,12,14,16,18,20,22,24,
        0,3,1,0,11,12,2,0,8,8,14,14,1,0,9,10,82,0,27,1,0,0,0,2,33,1,0,0,
        0,4,41,1,0,0,0,6,49,1,0,0,0,8,51,1,0,0,0,10,61,1,0,0,0,12,63,1,0,
        0,0,14,66,1,0,0,0,16,69,1,0,0,0,18,72,1,0,0,0,20,76,1,0,0,0,22,81,
        1,0,0,0,24,83,1,0,0,0,26,28,3,2,1,0,27,26,1,0,0,0,28,29,1,0,0,0,
        29,27,1,0,0,0,29,30,1,0,0,0,30,31,1,0,0,0,31,32,5,0,0,1,32,1,1,0,
        0,0,33,34,3,8,4,0,34,36,3,10,5,0,35,37,3,4,2,0,36,35,1,0,0,0,36,
        37,1,0,0,0,37,38,1,0,0,0,38,39,3,22,11,0,39,3,1,0,0,0,40,42,3,6,
        3,0,41,40,1,0,0,0,42,43,1,0,0,0,43,41,1,0,0,0,43,44,1,0,0,0,44,5,
        1,0,0,0,45,50,3,12,6,0,46,50,3,14,7,0,47,50,3,16,8,0,48,50,3,18,
        9,0,49,45,1,0,0,0,49,46,1,0,0,0,49,47,1,0,0,0,49,48,1,0,0,0,50,7,
        1,0,0,0,51,53,5,1,0,0,52,54,5,12,0,0,53,52,1,0,0,0,54,55,1,0,0,0,
        55,53,1,0,0,0,55,56,1,0,0,0,56,9,1,0,0,0,57,58,5,2,0,0,58,62,5,12,
        0,0,59,60,5,3,0,0,60,62,5,12,0,0,61,57,1,0,0,0,61,59,1,0,0,0,62,
        11,1,0,0,0,63,64,5,4,0,0,64,65,3,20,10,0,65,13,1,0,0,0,66,67,5,5,
        0,0,67,68,3,20,10,0,68,15,1,0,0,0,69,70,5,6,0,0,70,71,3,20,10,0,
        71,17,1,0,0,0,72,73,5,7,0,0,73,74,3,20,10,0,74,19,1,0,0,0,75,77,
        3,24,12,0,76,75,1,0,0,0,76,77,1,0,0,0,77,78,1,0,0,0,78,79,7,0,0,
        0,79,21,1,0,0,0,80,82,7,1,0,0,81,80,1,0,0,0,81,82,1,0,0,0,82,23,
        1,0,0,0,83,84,7,2,0,0,84,25,1,0,0,0,8,29,36,43,49,55,61,76,81
    ]

class GCodeParser ( Parser ):

    grammarFileName = "GCode.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'N'", "'G'", "'M'", "'X'", "'Y'", "'I'", 
                     "'J'", "'\\n'", "'+'", "'-'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "FLOAT", "INT", 
                      "WS", "COMMENT", "NEWLINE" ]

    RULE_program = 0
    RULE_statement = 1
    RULE_paramList = 2
    RULE_parameter = 3
    RULE_lineNumber = 4
    RULE_codFunc = 5
    RULE_coordX = 6
    RULE_coordY = 7
    RULE_coordI = 8
    RULE_coordJ = 9
    RULE_number = 10
    RULE_lineEnd = 11
    RULE_sign = 12

    ruleNames =  [ "program", "statement", "paramList", "parameter", "lineNumber", 
                   "codFunc", "coordX", "coordY", "coordI", "coordJ", "number", 
                   "lineEnd", "sign" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    FLOAT=11
    INT=12
    WS=13
    COMMENT=14
    NEWLINE=15

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(GCodeParser.EOF, 0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GCodeParser.StatementContext)
            else:
                return self.getTypedRuleContext(GCodeParser.StatementContext,i)


        def getRuleIndex(self):
            return GCodeParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)




    def program(self):

        localctx = GCodeParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 27 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 26
                self.statement()
                self.state = 29 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==1):
                    break

            self.state = 31
            self.match(GCodeParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def lineNumber(self):
            return self.getTypedRuleContext(GCodeParser.LineNumberContext,0)


        def codFunc(self):
            return self.getTypedRuleContext(GCodeParser.CodFuncContext,0)


        def lineEnd(self):
            return self.getTypedRuleContext(GCodeParser.LineEndContext,0)


        def paramList(self):
            return self.getTypedRuleContext(GCodeParser.ParamListContext,0)


        def getRuleIndex(self):
            return GCodeParser.RULE_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatement" ):
                listener.enterStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatement" ):
                listener.exitStatement(self)




    def statement(self):

        localctx = GCodeParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_statement)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 33
            self.lineNumber()
            self.state = 34
            self.codFunc()
            self.state = 36
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 240) != 0):
                self.state = 35
                self.paramList()


            self.state = 38
            self.lineEnd()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParamListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def parameter(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(GCodeParser.ParameterContext)
            else:
                return self.getTypedRuleContext(GCodeParser.ParameterContext,i)


        def getRuleIndex(self):
            return GCodeParser.RULE_paramList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParamList" ):
                listener.enterParamList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParamList" ):
                listener.exitParamList(self)




    def paramList(self):

        localctx = GCodeParser.ParamListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_paramList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 41 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 40
                self.parameter()
                self.state = 43 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 240) != 0)):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParameterContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def coordX(self):
            return self.getTypedRuleContext(GCodeParser.CoordXContext,0)


        def coordY(self):
            return self.getTypedRuleContext(GCodeParser.CoordYContext,0)


        def coordI(self):
            return self.getTypedRuleContext(GCodeParser.CoordIContext,0)


        def coordJ(self):
            return self.getTypedRuleContext(GCodeParser.CoordJContext,0)


        def getRuleIndex(self):
            return GCodeParser.RULE_parameter

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParameter" ):
                listener.enterParameter(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParameter" ):
                listener.exitParameter(self)




    def parameter(self):

        localctx = GCodeParser.ParameterContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_parameter)
        try:
            self.state = 49
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [4]:
                self.enterOuterAlt(localctx, 1)
                self.state = 45
                self.coordX()
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 2)
                self.state = 46
                self.coordY()
                pass
            elif token in [6]:
                self.enterOuterAlt(localctx, 3)
                self.state = 47
                self.coordI()
                pass
            elif token in [7]:
                self.enterOuterAlt(localctx, 4)
                self.state = 48
                self.coordJ()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LineNumberContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self, i:int=None):
            if i is None:
                return self.getTokens(GCodeParser.INT)
            else:
                return self.getToken(GCodeParser.INT, i)

        def getRuleIndex(self):
            return GCodeParser.RULE_lineNumber

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLineNumber" ):
                listener.enterLineNumber(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLineNumber" ):
                listener.exitLineNumber(self)




    def lineNumber(self):

        localctx = GCodeParser.LineNumberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_lineNumber)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 51
            self.match(GCodeParser.T__0)
            self.state = 53 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 52
                self.match(GCodeParser.INT)
                self.state = 55 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==12):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CodFuncContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(GCodeParser.INT, 0)

        def getRuleIndex(self):
            return GCodeParser.RULE_codFunc

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCodFunc" ):
                listener.enterCodFunc(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCodFunc" ):
                listener.exitCodFunc(self)




    def codFunc(self):

        localctx = GCodeParser.CodFuncContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_codFunc)
        try:
            self.state = 61
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [2]:
                self.enterOuterAlt(localctx, 1)
                self.state = 57
                self.match(GCodeParser.T__1)
                self.state = 58
                self.match(GCodeParser.INT)
                pass
            elif token in [3]:
                self.enterOuterAlt(localctx, 2)
                self.state = 59
                self.match(GCodeParser.T__2)
                self.state = 60
                self.match(GCodeParser.INT)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CoordXContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def number(self):
            return self.getTypedRuleContext(GCodeParser.NumberContext,0)


        def getRuleIndex(self):
            return GCodeParser.RULE_coordX

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCoordX" ):
                listener.enterCoordX(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCoordX" ):
                listener.exitCoordX(self)




    def coordX(self):

        localctx = GCodeParser.CoordXContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_coordX)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 63
            self.match(GCodeParser.T__3)
            self.state = 64
            self.number()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CoordYContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def number(self):
            return self.getTypedRuleContext(GCodeParser.NumberContext,0)


        def getRuleIndex(self):
            return GCodeParser.RULE_coordY

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCoordY" ):
                listener.enterCoordY(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCoordY" ):
                listener.exitCoordY(self)




    def coordY(self):

        localctx = GCodeParser.CoordYContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_coordY)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 66
            self.match(GCodeParser.T__4)
            self.state = 67
            self.number()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CoordIContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def number(self):
            return self.getTypedRuleContext(GCodeParser.NumberContext,0)


        def getRuleIndex(self):
            return GCodeParser.RULE_coordI

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCoordI" ):
                listener.enterCoordI(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCoordI" ):
                listener.exitCoordI(self)




    def coordI(self):

        localctx = GCodeParser.CoordIContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_coordI)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 69
            self.match(GCodeParser.T__5)
            self.state = 70
            self.number()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class CoordJContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def number(self):
            return self.getTypedRuleContext(GCodeParser.NumberContext,0)


        def getRuleIndex(self):
            return GCodeParser.RULE_coordJ

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCoordJ" ):
                listener.enterCoordJ(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCoordJ" ):
                listener.exitCoordJ(self)




    def coordJ(self):

        localctx = GCodeParser.CoordJContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_coordJ)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 72
            self.match(GCodeParser.T__6)
            self.state = 73
            self.number()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NumberContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(GCodeParser.INT, 0)

        def FLOAT(self):
            return self.getToken(GCodeParser.FLOAT, 0)

        def sign(self):
            return self.getTypedRuleContext(GCodeParser.SignContext,0)


        def getRuleIndex(self):
            return GCodeParser.RULE_number

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumber" ):
                listener.enterNumber(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumber" ):
                listener.exitNumber(self)




    def number(self):

        localctx = GCodeParser.NumberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_number)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 76
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==9 or _la==10:
                self.state = 75
                self.sign()


            self.state = 78
            _la = self._input.LA(1)
            if not(_la==11 or _la==12):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LineEndContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COMMENT(self):
            return self.getToken(GCodeParser.COMMENT, 0)

        def getRuleIndex(self):
            return GCodeParser.RULE_lineEnd

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLineEnd" ):
                listener.enterLineEnd(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLineEnd" ):
                listener.exitLineEnd(self)




    def lineEnd(self):

        localctx = GCodeParser.LineEndContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_lineEnd)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 81
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==8 or _la==14:
                self.state = 80
                _la = self._input.LA(1)
                if not(_la==8 or _la==14):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SignContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return GCodeParser.RULE_sign

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSign" ):
                listener.enterSign(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSign" ):
                listener.exitSign(self)




    def sign(self):

        localctx = GCodeParser.SignContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_sign)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 83
            _la = self._input.LA(1)
            if not(_la==9 or _la==10):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





