/**
 * Modulo: Comunicação com os Controladores PIC via duas UARTs separadas.
 *          (Modo de envio sem handshake/feedback)
 */

#include "comm_pic.h"
#include "hardware/uart.h"
#include "hardware/gpio.h"
#include "pico/stdlib.h"
#include "FreeRTOS.h"
#include "task.h"
#include <stdio.h>

// Configuração para a PIC do Motor 'a'
#define UART_A_ID       uart0
#define UART_A_BAUD     115200
#define UART_A_TX_PIN   0
#define UART_A_RX_PIN   1

// Configuração para a PIC do Motor 'b'
#define UART_B_ID       uart1
#define UART_B_BAUD     115200
#define UART_B_TX_PIN   4
#define UART_B_RX_PIN   5

void pic_comm_init(void) {
    // Inicializa a UART para o Motor 'a'
    uart_init(UART_A_ID, UART_A_BAUD);
    gpio_set_function(UART_A_TX_PIN, GPIO_FUNC_UART);
    gpio_set_function(UART_A_RX_PIN, GPIO_FUNC_UART); // Mesmo sem ler, é boa prática configurar
    printf("UART0 (Motor 'a') nos pinos GP%d/GP%d inicializada.\n", UART_A_TX_PIN, UART_A_RX_PIN);

    // Inicializa a UART para o Motor 'b'
    uart_init(UART_B_ID, UART_B_BAUD);
    gpio_set_function(UART_B_TX_PIN, GPIO_FUNC_UART);
    gpio_set_function(UART_B_RX_PIN, GPIO_FUNC_UART);
    printf("UART1 (Motor 'b') nos pinos GP%d/GP%d inicializada.\n", UART_B_TX_PIN, UART_B_RX_PIN);
}

void pic_send_position_setpoint(char motor_addr, double angle_deg) {
    char command_buffer[32];
    uart_inst_t* target_uart;

    // 1. Determina qual instância de UART usar
    if (motor_addr == 'a') {
        target_uart = UART_A_ID;
    } else if (motor_addr == 'b') {
        target_uart = UART_B_ID;
    } else {
        return; // Endereço de motor desconhecido
    }

    // 2. Formata a string de comando
    sprintf(command_buffer, ":%cp%.2f;", motor_addr, angle_deg);
    
    // 3. Envia para a UART correta, caractere por caractere
    printf("Enviando para PIC (Addr %c via UART%d): %s\n", motor_addr, uart_get_index(target_uart), command_buffer); // Opcional para debug
    
    for (int i = 0; command_buffer[i] != '\0'; i++) {
        uart_putc_raw(target_uart, command_buffer[i]);
        vTaskDelay(pdMS_TO_TICKS(4)); // Delay crítico de 2ms para garantir
    }
}
void pic_send_simple_command(char motor_addr, char command) {
    char command_buffer[8];
    uart_inst_t* target_uart;

    if (motor_addr == 'a') {
        target_uart = UART_A_ID;
    } else if (motor_addr == 'b') {
        target_uart = UART_B_ID;
    } else {
        return;
    }

    // Formata a string de comando simples: :<addr><cmd>;
    sprintf(command_buffer, ":%c%c;", motor_addr, command);
    
    for (int i = 0; command_buffer[i] != '\0'; i++) {
        uart_putc_raw(target_uart, command_buffer[i]);
        vTaskDelay(pdMS_TO_TICKS(5));
    }
}
