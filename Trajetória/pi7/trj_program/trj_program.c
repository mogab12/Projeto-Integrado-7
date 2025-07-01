/*
 * Modulo: Programa Trajetoria
 * Armazena o programa da trajetoria a ser executada
 */

// max NC program size
#define MAX_PROGRAM_LINES 50

#define AX 0
#define AY 0

#define BX 250
#define BY 0

#include "trj_program.h"


// structure to store NC program
tpr_Data tpr_program[MAX_PROGRAM_LINES];

void tpr_storeProgram(char* texto) {
    int i = 0;
    while (*texto != '\0' && i < MAX_PROGRAM_LINES) {
        
        while (*texto && *texto != 'X') texto++;
        if (!*texto) break;
        texto++;  
        tpr_program[i].x = atof(texto);

        
        while (*texto && *texto != 'Y') texto++;
        if (!*texto) break;
        texto++;  
        tpr_program[i].y = atof(texto);

        float theta1 = sqrt(pow(tpr_program[i].x,2) + pow((AY - tpr_program[i].y),2));
        float theta2 = sqrt(pow((BX - AX - tpr_program[i].x),2) + pow((BY - tpr_program[i].y),2));

        tpr_program[i].x = theta1;
        tpr_program[i].y = theta2;

        i++;
    }
} // tpr_storeProgram

tpr_Data tpr_getLine(int line) {
	return tpr_program[line];
} // tpr_getLine

void tpr_init() {
  int i;

  for (i=0; i<MAX_PROGRAM_LINES;i++) {
	  tpr_program[i].x = 0;
	  tpr_program[i].y = 0;
	  tpr_program[i].z = 0;
  }
} //tpr_init
