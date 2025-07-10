#ifndef __COMMAND_INTERPRETER_H
#define __COMMAND_INTERPRETER_H

#include <stdint.h>
#include <stdbool.h> // Incluir para usar o tipo 'bool'

/*
 * Registradores do dispositivo (mapeamento de memória Modbus)
 * Os valores correspondem aos endereços de registrador de 16 bits.
 */

// Registradores de Leitura (Read-Only)
#define REG_X       0x0009  // Posição X atual
#define REG_Y       0x000A  // Posição Y atual (10 decimal)
#define REG_LINHA   0x000B  // Índice da linha/ponto atual

// Registradores de Controle (Write-Only)
// A escrita de qualquer valor nestes registradores dispara uma ação.
#define REG_START   0x0001
#define REG_SUSPEND 0x0002  // Pausar
#define REG_RESUME  0x0003  // Continuar
#define REG_STOP    0x0004  // Abortar

// Código de erro
#define CTL_ERR -1 // Pode ser usado para indicar erro na leitura

/*
 * ===================================================================
 *                    Declarações das Funções
 * ===================================================================
 */

/**
 * @brief Inicializa o módulo interpretador de comandos.
 */
extern void ctl_init(void);

/**
 * @brief Lê o valor de um registrador de 16 bits.
 * @param registerToRead O endereço do registrador (ex: REG_X).
 * @return O valor do registrador.
 */
extern int ctl_ReadRegister(uint16_t registerToRead);

/**
 * @brief Escreve em um registrador de controle para disparar uma ação.
 * @param registerToWrite O endereço do registrador (ex: REG_START).
 * @param value O valor a ser escrito (geralmente ignorado para comandos).
 * @return true se o comando foi aceito, false caso contrário.
 */
extern bool ctl_WriteRegister(uint16_t registerToWrite, uint16_t value);

/**
 * @brief <<< CORREÇÃO APLICADA AQUI >>>
 * @brief Grava o programa de trajetória (sequência de pontos) na memória.
 * @param program_bytes Ponteiro para o array de bytes contendo os dados do programa.
 * @param len O número de bytes no array 'program_bytes'.
 * @return true se o programa foi armazenado com sucesso, false caso contrário.
 */
extern bool ctl_WriteProgram(uint8_t* program_bytes, uint16_t len);

#endif // __COMMAND_INTERPRETER_H