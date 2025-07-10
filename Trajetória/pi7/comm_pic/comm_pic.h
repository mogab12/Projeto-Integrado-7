#ifndef __COMM_PIC_H
#define __COMM_PIC_H

#include <stdint.h>
#include <stdbool.h>

/**
 * @brief Inicializa AMBAS as UARTs (UART0 e UART1) para comunicação com as PICs.
 */
void pic_comm_init(void);

/**
 * @brief Envia um comando de setpoint de posição para uma PIC específica
 *        através da sua UART dedicada, com o delay necessário entre caracteres.
 * @param motor_addr O endereço do motor ('a' ou 'b') para selecionar a UART correta.
 * @param angle_deg O ângulo de setpoint desejado em graus.
 */
void pic_send_position_setpoint(char motor_addr, double angle_deg);

/**
 * @brief Envia um comando simples (sem valor) para uma PIC específica.
 *        Usado para comandos como 'home' (h).
 * @param motor_addr O endereço do motor ('a' ou 'b').
 * @param command O caractere do comando (ex: 'h').
 */
void pic_send_simple_command(char motor_addr, char command);

#endif // __COMM_PIC_H
