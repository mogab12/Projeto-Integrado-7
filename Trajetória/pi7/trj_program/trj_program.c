/*
 * Modulo: Programa Trajetoria
 * Armazena a lista de pontos (coordenadas cartesianas) da trajetória.
 */

#include "trj_program.h"
#include <stdio.h> // Para printf de debug

// Número máximo de pontos que podemos armazenar.
#define MAX_PROGRAM_POINTS 250 

// Estrutura para armazenar o programa
static tpr_Data tpr_program[MAX_PROGRAM_POINTS];
static int total_points_stored = 0; // Guarda quantos pontos temos


void tpr_init() {
  total_points_stored = 0;
  for (int i = 0; i < MAX_PROGRAM_POINTS; i++) {
	  tpr_program[i].x = 0;
	  tpr_program[i].y = 0;
  }
}

tpr_Data tpr_getLine(int line_num) {
	if (line_num >= 0 && line_num < total_points_stored) {
    return tpr_program[line_num];
  }
  // Retorna um ponto (0,0) se a linha for inválida
  tpr_Data empty = {0, 0};
  return empty;
}

bool tpr_storeProgram(uint8_t* data, uint16_t len) {
  // Cada ponto (X, Y) é representado por 4 bytes (2 para X, 2 para Y).
  // Verificamos se o tamanho dos dados é um múltiplo de 4.
  if ((len % 4) != 0) {
    printf("Erro: Tamanho dos dados do programa invalido (%d bytes).\n", len);
    return false;
  }

  int num_points = len / 4;
  if (num_points > MAX_PROGRAM_POINTS) {
    printf("Erro: O programa e muito grande (%d pontos).\n", num_points);
    return false;
  }

  // Zera o programa antigo antes de carregar o novo
  tpr_init();

  int data_idx = 0;
  for (int i = 0; i < num_points; i++) {
    // Lê a coordenada X (2 bytes, big-endian)
    int16_t x_val = (data[data_idx] << 8) | data[data_idx + 1];
    
    // Lê a coordenada Y (2 bytes, big-endian)
    int16_t y_val = (data[data_idx + 2] << 8) | data[data_idx + 3];

    tpr_program[i].x = x_val;
    tpr_program[i].y = y_val;

    // Avança o índice no array de dados para o próximo ponto
    data_idx += 4;
  }

  total_points_stored = num_points;
  printf("Programa carregado com sucesso: %d pontos armazenados.\n", total_points_stored);

  // Debug: Imprime os primeiros pontos para verificação
  for (int i=0; i < 5 && i < total_points_stored; i++) {
    printf("Ponto %d: (X=%ld, Y=%ld)\n", i, tpr_program[i].x, tpr_program[i].y);
  }

  return true;
}

int tpr_getProgramSize(void) {
    return total_points_stored;
}


