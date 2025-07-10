/*
 * Modulo: Estado Trajetoria
 * Contem as variaveis de estado da trajetoria de forma segura para multitarefa (thread-safe).
 */

#include "trj_state.h"
#include "FreeRTOS.h"
#include "semphr.h" 

static int tst_line;
static int32_t tst_x;
static int32_t tst_y;

// Mutex para proteger o acesso às variáveis de estado
static SemaphoreHandle_t state_mutex;

void tst_init() {
  // Cria o mutex
  state_mutex = xSemaphoreCreateMutex();
  
  if (state_mutex != NULL) {
    // Inicializa as variáveis com valores padrão
    tst_line = 0;
    tst_x = 0;
    tst_y = 0;
  }
}

void tst_setCurrentLine(int line) {
  // Pega o mutex, bloqueando se outra tarefa o estiver usando.
  if (xSemaphoreTake(state_mutex, portMAX_DELAY) == pdTRUE) {
    tst_line = line;
    // Libera o mutex para que outras tarefas possam usá-lo.
    xSemaphoreGive(state_mutex);
  }
}

int tst_getCurrentLine() {
  int line;
  if (xSemaphoreTake(state_mutex, portMAX_DELAY) == pdTRUE) {
    line = tst_line;
    xSemaphoreGive(state_mutex);
  }
  return line;
}

void tst_setX(int32_t x) {
  if (xSemaphoreTake(state_mutex, portMAX_DELAY) == pdTRUE) {
    tst_x = x;
    xSemaphoreGive(state_mutex);
  }
}

int32_t tst_getX() {
  int32_t x;
  if (xSemaphoreTake(state_mutex, portMAX_DELAY) == pdTRUE) {
    x = tst_x;
    xSemaphoreGive(state_mutex);
  }
  return x;
}

void tst_setY(int32_t y) {
  if (xSemaphoreTake(state_mutex, portMAX_DELAY) == pdTRUE) {
    tst_y = y;
    xSemaphoreGive(state_mutex);
  }
}

int32_t tst_getY() {
  int32_t y;
  if (xSemaphoreTake(state_mutex, portMAX_DELAY) == pdTRUE) {
    y = tst_y;
    xSemaphoreGive(state_mutex);
  }
  return y;
}