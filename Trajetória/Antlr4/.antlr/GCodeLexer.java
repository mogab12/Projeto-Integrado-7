// Generated from c:/Users/haman/Projeto-Integrado-7/Trajetória/Antlr4/GCode.g4 by ANTLR 4.13.1
import org.antlr.v4.runtime.Lexer;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.TokenStream;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.misc.*;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast", "CheckReturnValue", "this-escape"})
public class GCodeLexer extends Lexer {
	static { RuntimeMetaData.checkVersion("4.13.1", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, T__1=2, T__2=3, T__3=4, T__4=5, T__5=6, T__6=7, T__7=8, T__8=9, 
		T__9=10, FLOAT=11, INT=12, WS=13, COMMENT=14, NEWLINE=15;
	public static String[] channelNames = {
		"DEFAULT_TOKEN_CHANNEL", "HIDDEN"
	};

	public static String[] modeNames = {
		"DEFAULT_MODE"
	};

	private static String[] makeRuleNames() {
		return new String[] {
			"T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", "T__7", "T__8", 
			"T__9", "FLOAT", "INT", "WS", "COMMENT", "NEWLINE"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'N'", "'G'", "'M'", "'X'", "'Y'", "'I'", "'J'", "'\\n'", "'+'", 
			"'-'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, null, null, null, null, null, null, null, null, null, null, "FLOAT", 
			"INT", "WS", "COMMENT", "NEWLINE"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}


	public GCodeLexer(CharStream input) {
		super(input);
		_interp = new LexerATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@Override
	public String getGrammarFileName() { return "GCode.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public String[] getChannelNames() { return channelNames; }

	@Override
	public String[] getModeNames() { return modeNames; }

	@Override
	public ATN getATN() { return _ATN; }

	public static final String _serializedATN =
		"\u0004\u0000\u000fS\u0006\uffff\uffff\u0002\u0000\u0007\u0000\u0002\u0001"+
		"\u0007\u0001\u0002\u0002\u0007\u0002\u0002\u0003\u0007\u0003\u0002\u0004"+
		"\u0007\u0004\u0002\u0005\u0007\u0005\u0002\u0006\u0007\u0006\u0002\u0007"+
		"\u0007\u0007\u0002\b\u0007\b\u0002\t\u0007\t\u0002\n\u0007\n\u0002\u000b"+
		"\u0007\u000b\u0002\f\u0007\f\u0002\r\u0007\r\u0002\u000e\u0007\u000e\u0001"+
		"\u0000\u0001\u0000\u0001\u0001\u0001\u0001\u0001\u0002\u0001\u0002\u0001"+
		"\u0003\u0001\u0003\u0001\u0004\u0001\u0004\u0001\u0005\u0001\u0005\u0001"+
		"\u0006\u0001\u0006\u0001\u0007\u0001\u0007\u0001\b\u0001\b\u0001\t\u0001"+
		"\t\u0001\n\u0001\n\u0001\n\u0001\n\u0001\u000b\u0004\u000b9\b\u000b\u000b"+
		"\u000b\f\u000b:\u0001\f\u0004\f>\b\f\u000b\f\f\f?\u0001\f\u0001\f\u0001"+
		"\r\u0001\r\u0005\rF\b\r\n\r\f\rI\t\r\u0001\r\u0001\r\u0001\u000e\u0003"+
		"\u000eN\b\u000e\u0001\u000e\u0001\u000e\u0001\u000e\u0001\u000e\u0000"+
		"\u0000\u000f\u0001\u0001\u0003\u0002\u0005\u0003\u0007\u0004\t\u0005\u000b"+
		"\u0006\r\u0007\u000f\b\u0011\t\u0013\n\u0015\u000b\u0017\f\u0019\r\u001b"+
		"\u000e\u001d\u000f\u0001\u0000\u0003\u0001\u000009\u0003\u0000\t\t\r\r"+
		"  \u0002\u0000\n\n\r\rV\u0000\u0001\u0001\u0000\u0000\u0000\u0000\u0003"+
		"\u0001\u0000\u0000\u0000\u0000\u0005\u0001\u0000\u0000\u0000\u0000\u0007"+
		"\u0001\u0000\u0000\u0000\u0000\t\u0001\u0000\u0000\u0000\u0000\u000b\u0001"+
		"\u0000\u0000\u0000\u0000\r\u0001\u0000\u0000\u0000\u0000\u000f\u0001\u0000"+
		"\u0000\u0000\u0000\u0011\u0001\u0000\u0000\u0000\u0000\u0013\u0001\u0000"+
		"\u0000\u0000\u0000\u0015\u0001\u0000\u0000\u0000\u0000\u0017\u0001\u0000"+
		"\u0000\u0000\u0000\u0019\u0001\u0000\u0000\u0000\u0000\u001b\u0001\u0000"+
		"\u0000\u0000\u0000\u001d\u0001\u0000\u0000\u0000\u0001\u001f\u0001\u0000"+
		"\u0000\u0000\u0003!\u0001\u0000\u0000\u0000\u0005#\u0001\u0000\u0000\u0000"+
		"\u0007%\u0001\u0000\u0000\u0000\t\'\u0001\u0000\u0000\u0000\u000b)\u0001"+
		"\u0000\u0000\u0000\r+\u0001\u0000\u0000\u0000\u000f-\u0001\u0000\u0000"+
		"\u0000\u0011/\u0001\u0000\u0000\u0000\u00131\u0001\u0000\u0000\u0000\u0015"+
		"3\u0001\u0000\u0000\u0000\u00178\u0001\u0000\u0000\u0000\u0019=\u0001"+
		"\u0000\u0000\u0000\u001bC\u0001\u0000\u0000\u0000\u001dM\u0001\u0000\u0000"+
		"\u0000\u001f \u0005N\u0000\u0000 \u0002\u0001\u0000\u0000\u0000!\"\u0005"+
		"G\u0000\u0000\"\u0004\u0001\u0000\u0000\u0000#$\u0005M\u0000\u0000$\u0006"+
		"\u0001\u0000\u0000\u0000%&\u0005X\u0000\u0000&\b\u0001\u0000\u0000\u0000"+
		"\'(\u0005Y\u0000\u0000(\n\u0001\u0000\u0000\u0000)*\u0005I\u0000\u0000"+
		"*\f\u0001\u0000\u0000\u0000+,\u0005J\u0000\u0000,\u000e\u0001\u0000\u0000"+
		"\u0000-.\u0005\n\u0000\u0000.\u0010\u0001\u0000\u0000\u0000/0\u0005+\u0000"+
		"\u00000\u0012\u0001\u0000\u0000\u000012\u0005-\u0000\u00002\u0014\u0001"+
		"\u0000\u0000\u000034\u0003\u0017\u000b\u000045\u0005.\u0000\u000056\u0003"+
		"\u0017\u000b\u00006\u0016\u0001\u0000\u0000\u000079\u0007\u0000\u0000"+
		"\u000087\u0001\u0000\u0000\u00009:\u0001\u0000\u0000\u0000:8\u0001\u0000"+
		"\u0000\u0000:;\u0001\u0000\u0000\u0000;\u0018\u0001\u0000\u0000\u0000"+
		"<>\u0007\u0001\u0000\u0000=<\u0001\u0000\u0000\u0000>?\u0001\u0000\u0000"+
		"\u0000?=\u0001\u0000\u0000\u0000?@\u0001\u0000\u0000\u0000@A\u0001\u0000"+
		"\u0000\u0000AB\u0006\f\u0000\u0000B\u001a\u0001\u0000\u0000\u0000CG\u0005"+
		";\u0000\u0000DF\b\u0002\u0000\u0000ED\u0001\u0000\u0000\u0000FI\u0001"+
		"\u0000\u0000\u0000GE\u0001\u0000\u0000\u0000GH\u0001\u0000\u0000\u0000"+
		"HJ\u0001\u0000\u0000\u0000IG\u0001\u0000\u0000\u0000JK\u0006\r\u0000\u0000"+
		"K\u001c\u0001\u0000\u0000\u0000LN\u0005\r\u0000\u0000ML\u0001\u0000\u0000"+
		"\u0000MN\u0001\u0000\u0000\u0000NO\u0001\u0000\u0000\u0000OP\u0005\n\u0000"+
		"\u0000PQ\u0001\u0000\u0000\u0000QR\u0006\u000e\u0000\u0000R\u001e\u0001"+
		"\u0000\u0000\u0000\u0005\u0000:?GM\u0001\u0006\u0000\u0000";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}