#ifndef __MODBUS_H
#define __MODBUS_H

/**
 * @brief Inicializa a camada de comunicação.
 */
void com_init(void);

/**
 * @brief Executa um ciclo da máquina de estados de comunicação.
 *        Deve ser chamado repetidamente no loop principal de uma tarefa.
 */
void com_executeCommunication(void);

#endif // __MODBUS_H