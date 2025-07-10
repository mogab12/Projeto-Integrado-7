// #ifndef __trj_program_h
// #define __trj_program_h
// #include <math.h>

// typedef struct {
// 	float x;
// 	float y;
// 	float z;
// } tpr_Data;

// extern void tpr_storeProgram(char* texto);
// extern tpr_Data tpr_getLine(int line);
// extern void tpr_init();
// #endif
#ifndef __TRJ_PROGRAM_H
#define __TRJ_PROGRAM_H

#include <stdint.h>
#include <stdbool.h>

// Estrutura para armazenar um ponto da trajetória.
// Usamos inteiros para representar as coordenadas com 2 casas decimais.
// Ex: 12.34 se torna 1234.
typedef struct {
	int32_t x;
	int32_t y;
	// int32_t z; // Não usado no plotter 2D
} tpr_Data;

/**
 * @brief Inicializa a memória do programa, zerando todos os pontos.
 */
extern void tpr_init(void);

/**
 * @brief Armazena um programa de trajetória a partir de um array de bytes.
 *        A função decodifica o array e armazena os pontos (X, Y) na memória.
 * @param data Ponteiro para o array de bytes recebido via comunicação.
 * @param len O número de bytes no array 'data'.
 * @return true se o programa foi armazenado com sucesso, false caso contrário.
 */
extern bool tpr_storeProgram(uint8_t* data, uint16_t len);

/**
 * @brief Retorna um ponto (linha) específico do programa armazenado.
 * @param line O índice do ponto a ser recuperado.
 * @return A estrutura tpr_Data contendo as coordenadas (X, Y) do ponto.
 */
extern tpr_Data tpr_getLine(int line);

/**
 * @brief Retorna o número total de pontos carregados no programa.
 */
extern int tpr_getProgramSize(void);


#endif // __TRJ_PROGRAM_H
