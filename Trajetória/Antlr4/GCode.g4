grammar GCode;

program: statement+ EOF;

statement: lineNumber codFunc paramList? lineEnd;

paramList: parameter+ ;

parameter: coordX | coordY | coordI | coordJ ;

lineNumber: 'N' INT+;
codFunc: 'G' INT | 'M' INT;
coordX: 'X' number;
coordY: 'Y' number;
coordI: 'I' number;
coordJ: 'J' number;
number: sign? (INT | FLOAT);
lineEnd: (COMMENT | '\n')?;

sign: '+' | '-' ;

FLOAT: INT '.' INT;
INT: [0-9]+;

WS: [ \t\r]+ -> skip;
COMMENT: ';' ~[\n\r]* -> skip;
NEWLINE: '\r'? '\n' -> skip;
