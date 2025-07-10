/*
 * Modulo: Interpretador de Comandos
 * Interpreta os comandos recebidos da IHM e processa-os
 */

#include "FreeRTOS.h"
#include "queue.h"
#include <stdbool.h>
#include <stdio.h>
#include <stdint.h>

// Includes da aplicação
#include "command_interpreter.h"
#include "../trj_state/trj_state.h"
#include "../trj_control/trj_control.h"
#include "../trj_program/trj_program.h"

// Fila de comunicação com a tarefa de controle de trajetória
extern QueueHandle_t qControlCommands;

void ctl_init() {
  // Inicializa o módulo que gerencia o armazenamento do programa de trajetória
  tpr_init();
}

int ctl_ReadRegister(uint16_t registerToRead) { 
   switch (registerToRead) {
      case REG_X:
         return (int)tst_getX();
      case REG_Y:
         return (int)tst_getY();
      case REG_LINHA:
         return tst_getCurrentLine();
   } // switch
   return CTL_ERR;
}

bool ctl_WriteRegister(uint16_t registerToWrite, uint16_t value) { 
  tcl_Data command;
  (void)value;

  // printf("Register %d Value %d\n", registerToWrite, value); // Para debug
  switch(registerToWrite) {
    case REG_START:
      printf("start program\n");
      command.command = CMD_START;
      xQueueSend(qControlCommands, &command, portMAX_DELAY);
      break;
   
    case REG_SUSPEND:
      printf("suspending program\n");
      command.command = CMD_SUSPEND;
      xQueueSend(qControlCommands, &command, portMAX_DELAY);
      break;  
   
    case REG_STOP:
      printf("stoping program\n");
      command.command = CMD_STOP;
      xQueueSend(qControlCommands, &command, portMAX_DELAY);
      break; 
   
    case REG_RESUME:
      printf("resuming program\n");
      command.command = CMD_RESUME;
      xQueueSend(qControlCommands, &command, portMAX_DELAY);
      break; 
   
    default:
      return false; // Retorna erro
  }
  return true; // Retorna sucesso
}

bool ctl_WriteProgram(uint8_t* program_bytes, uint16_t len) { 
  // printf("Controller: Recebido programa de %d bytes para armazenar.\n", len);
  
  bool success = tpr_storeProgram(program_bytes, len);
  
  return success;
}