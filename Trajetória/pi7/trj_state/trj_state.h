#ifndef __TRJ_STATE_H
#define __TRJ_STATE_H

#include <stdint.h>

/**
 * @brief Inicializa as variáveis de estado e o mutex de proteção.
 */
extern void tst_init(void);

/**
 * @brief Define o índice da linha/ponto atual do programa. (Thread-safe)
 */
extern void tst_setCurrentLine(int line);

/**
 * @brief Obtém o índice da linha/ponto atual do programa. (Thread-safe)
 */
extern int tst_getCurrentLine(void);

/**
 * @brief Define a coordenada X atual. (Thread-safe)
 * @param x Coordenada X (valor * 100).
 */
extern void tst_setX(int32_t x);

/**
 * @brief Obtém a coordenada X atual. (Thread-safe)
 * @return Coordenada X (valor * 100).
 */
extern int32_t tst_getX(void);

/**
 * @brief Define a coordenada Y atual. (Thread-safe)
 * @param y Coordenada Y (valor * 100).
 */
extern void tst_setY(int32_t y);

/**
 * @brief Obtém a coordenada Y atual. (Thread-safe)
 * @return Coordenada Y (valor * 100).
 */
extern int32_t tst_getY(void);

#endif // __TRJ_STATE_H