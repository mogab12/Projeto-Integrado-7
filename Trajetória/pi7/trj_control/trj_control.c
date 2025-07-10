#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"
#include <stdio.h>
#include <math.h>
#include <stdbool.h>

#include "trj_control.h"
#include "../trj_program/trj_program.h"
#include "../trj_state/trj_state.h"
#include "../comm_pic/comm_pic.h"

/* =========================================================================
 *                      DEFINIÇÕES E VARIÁVEIS GLOBAIS
 * ========================================================================= */

extern QueueHandle_t qControlCommands;

// Parâmetros da cinemática do plotter
#define MOTOR_A_X 0
#define MOTOR_A_Y 0
#define MOTOR_B_X 29500 
#define MOTOR_B_Y 0
#define PULLEY_RADIUS 1200.0
#define HOME_CABLE_LENGTH 15500.0 // Comprimento do cabo na posição home (155.00mm)
#define PI 3.14159265

#define DELAY_BETWEEN_POINTS_MS 500

typedef enum {
    STATE_IDLE,
    STATE_RUNNING
} TaskState;

static TaskState current_state = STATE_IDLE;

/* =========================================================================
 *                      FUNÇÕES DE LÓGICA INTERNA
 * ========================================================================= */

static void inverse_kinematics_to_angles_deg(tpr_Data cart_point, double* angle_a, double* angle_b) {
    // Passo 1: Calcular o novo comprimento do cabo para o ponto (x,y)
    int64_t dx_a = cart_point.x - MOTOR_A_X;
    int64_t dy_a = cart_point.y - MOTOR_A_Y;
    double new_cable_len_a = sqrt((double)(dx_a * dx_a) + (double)(dy_a * dy_a));

    int64_t dx_b = cart_point.x - MOTOR_B_X;
    int64_t dy_b = cart_point.y - MOTOR_B_Y;
    double new_cable_len_b = sqrt((double)(dx_b * dx_b) + (double)(dy_b * dy_b));

    // Passo 2: Calcular a VARIAÇÃO de comprimento
    double delta_len_a = new_cable_len_a - HOME_CABLE_LENGTH;
    double delta_len_b = new_cable_len_b - HOME_CABLE_LENGTH;
    
    // Passo 3: Converter a variação de comprimento em variação de ângulo
    // delta_theta = delta_L / R
    double delta_angle_a_rad = delta_len_a / PULLEY_RADIUS; // aqui um dos ângulos deveria ser negativo por serem inversos
    double delta_angle_b_rad = delta_len_b / PULLEY_RADIUS; // mas em vez disso trocamos o sinal no controlador
    
    // Passo 4: Converter de radianos para graus
    *angle_a = delta_angle_a_rad * (180.0 / PI);
    *angle_b = delta_angle_b_rad * (180.0 / PI);
}
/**
 * @brief Função principal que orquestra todo o processo de desenho.
 */
static void execute_drawing_loop() {
    int total_lines = tpr_getProgramSize();
    if (total_lines <= 0) {
        printf("Nenhum ponto para desenhar. Operacao cancelada.\n");
        current_state = STATE_IDLE;
        return;
    }
    
printf("Iniciando desenho de %d pontos...\n", total_lines);

    for (int i = 0; i < total_lines; i++) {
        // ... (código de abortar, calcular cinemática e enviar pontos) ...
        tpr_Data cartesian_point = tpr_getLine(i);
        double angle_motor_a, angle_motor_b;
        inverse_kinematics_to_angles_deg(cartesian_point, &angle_motor_a, &angle_motor_b);
        
        pic_send_position_setpoint('a', angle_motor_a);
        pic_send_position_setpoint('b', angle_motor_b);

        vTaskDelay(pdMS_TO_TICKS(DELAY_BETWEEN_POINTS_MS));
    }
    vTaskDelay(pdMS_TO_TICKS(1000));
    printf("Desenho concluído. Retornando para a posicao inicial...\n");
    pic_send_position_setpoint('a', 0.0);
    pic_send_position_setpoint('b', 0.0);

    current_state = STATE_IDLE;
}

/* =========================================================================
 *                      TAREFA PRINCIPAL DO MÓDULO
 * ========================================================================= */

void TrajectoryControlTask(void *pvParameters) {
    printf("Tarefa de Controle de Trajetoria pronta.\n");
    current_state = STATE_IDLE;
    
    while(1) {
        tcl_Data received_cmd;
        if (xQueueReceive(qControlCommands, &received_cmd, portMAX_DELAY) == pdPASS) {
            
            if (current_state == STATE_IDLE && received_cmd.command == CMD_START) {
                current_state = STATE_RUNNING;
                
                // 1. Espera um segundo para garantir que as PICs processaram
                printf("Aguardando 1 segundo...\n");
                vTaskDelay(pdMS_TO_TICKS(1000));
                
                // 2. Inicia o loop de desenho
                execute_drawing_loop();
            }
        }
    }
}

void tcl_CreateTask(void) {
    xTaskCreate(
        TrajectoryControlTask,
        "TrjControl",
        configMINIMAL_STACK_SIZE * 4,
        NULL,
        tskIDLE_PRIORITY + 2,
        NULL
    );
}

