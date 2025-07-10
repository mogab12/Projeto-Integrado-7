/**
 * Modulo: Comunicacao MODBUS
 * Usa a Serial0 (USB) para comunicar-se
 */
// O código base foi bastante alterado devido a erros na implementação real
#include "FreeRTOS.h"
#include "queue.h"
#include "pico/stdio.h"
#include <stdint.h>
#include <stdio.h>
#include <stdbool.h>

#include "modbus.h"
#include "../command_interpreter/command_interpreter.h"

#define byte uint8_t

#define MAX_RX_SIZE 2048 
#define MAX_TX_SIZE 64   

// Endereço deste nó e Function Codes
#define MY_ADDRESS 0x01
#define READ_REGISTER 0x03
#define WRITE_REGISTER 0x06
#define WRITE_FILE 0x15

// Estados da máquina de recepção
#define HUNTING_FOR_START_OF_MESSAGE 0
#define HUNTING_FOR_END_OF_MESSAGE 1
#define MESSAGE_READY 2

static int _state;
static byte rxBuffer[MAX_RX_SIZE];
static int idxRxBuffer;
static byte txBuffer[MAX_TX_SIZE];

// Declaração de funções internas
static byte decode(byte high, byte low);
static byte encodeLow(byte value);
static byte encodeHigh(byte value);
static byte calculateLRC(byte* frame, int len);
static bool checkLRC(void);
static void processMessage(void);

void com_init() {
  _state = HUNTING_FOR_START_OF_MESSAGE;
}

void sendTxBufferToSerialUSB(void) {
  // Envia a string terminada em nulo para a serial USB
  printf("%s\r\n", txBuffer); 
}

byte decode(byte high, byte low) {
  byte x = (low <= '9') ? (low - '0') : (low - 'A' + 10);
  byte y = (high <= '9') ? (high - '0') : (high - 'A' + 10);
  return (y << 4) | x;
}

byte encodeLow(byte value) {
  byte x = value & 0x0F;
  return (x < 10) ? ('0' + x) : ('A' + (x - 10));
}

byte encodeHigh(byte value) {
  byte x = (value >> 4) & 0x0F;
  return (x < 10) ? ('0' + x) : ('A' + (x - 10));
}

byte calculateLRC(byte* frame, int len) {
  byte accum = 0;
  for (int i = 0; i < len; i++) {
    accum += frame[i];
  }
  // Retorna o complemento de dois da soma
  return (byte)(-accum);
}
static bool checkLRC(void) {
    byte accum = 0;
    byte decoded_byte;

    // O loop agora vai do primeiro caractere do payload (índice 1)
    // até o último caractere ANTES do LRC (índice idxRxBuffer - 4).
    for (int i = 1; i < idxRxBuffer - 4; i += 2) {
        decoded_byte = decode(rxBuffer[i], rxBuffer[i+1]);
        accum += decoded_byte;
    }

    // Finaliza o cálculo do LRC
    byte calculatedLRC = (byte)(-accum);

    // Decodifica o LRC que foi recebido na mensagem
    byte receivedLRC = decode(rxBuffer[idxRxBuffer - 4], rxBuffer[idxRxBuffer - 3]);

    // Imprime para a depuração final
    printf("DEBUG: LRC Recebido=0x%02X, LRC Calculado=0x%02X\n", receivedLRC, calculatedLRC);

    return (receivedLRC == calculatedLRC);
}
void processReadRegister() {
  // Endereço do registrador: 2 bytes (4 chars hex), ex: 0009 para X
  byte addr_reg_h = decode(rxBuffer[5], rxBuffer[6]);
  byte addr_reg_l = decode(rxBuffer[7], rxBuffer[8]);
  uint16_t registerToRead = (addr_reg_h << 8) | addr_reg_l;

  // Assume que ctl_ReadRegister retorna um valor de 16 bits
  uint16_t registerValue = ctl_ReadRegister(registerToRead);

  // --- Monta frame de resposta binário para calcular o LRC ---
  byte resp_binary[5];
  resp_binary[0] = MY_ADDRESS;
  resp_binary[1] = READ_REGISTER;
  resp_binary[2] = 2; // Byte Count = 2 bytes de dados
  resp_binary[3] = (registerValue >> 8) & 0xFF; // High byte do valor
  resp_binary[4] = registerValue & 0xFF;        // Low byte do valor
  byte lrc = calculateLRC(resp_binary, 5);

  // --- Monta frame de resposta ASCII para enviar ---
  sprintf((char*)txBuffer, ":%02X%02X%02X%04X%02X",
          resp_binary[0], resp_binary[1], resp_binary[2], registerValue, lrc);

  sendTxBufferToSerialUSB();
}

void processWriteRegister() {
  byte addr_reg_h = decode(rxBuffer[5], rxBuffer[6]);
  byte addr_reg_l = decode(rxBuffer[7], rxBuffer[8]);
  uint16_t registerToWrite = (addr_reg_h << 8) | addr_reg_l;

  byte val_reg_h = decode(rxBuffer[9], rxBuffer[10]);
  byte val_reg_l = decode(rxBuffer[11], rxBuffer[12]);
  uint16_t registerValue = (val_reg_h << 8) | val_reg_l;

  ctl_WriteRegister(registerToWrite, registerValue);

  // --- Monta resposta (eco do comando) ---
  byte resp_binary[6];
  resp_binary[0] = MY_ADDRESS;
  resp_binary[1] = WRITE_REGISTER;
  resp_binary[2] = addr_reg_h;
  resp_binary[3] = addr_reg_l;
  resp_binary[4] = val_reg_h;
  resp_binary[5] = val_reg_l;
  byte lrc = calculateLRC(resp_binary, 6);

  sprintf((char*)txBuffer, ":%02X%02X%04X%04X%02X",
          resp_binary[0], resp_binary[1], registerToWrite, registerValue, lrc);

  sendTxBufferToSerialUSB();
}

void processWriteFile() {
  // Tamanho dos dados: 2 bytes (4 chars hex)
  byte len_h = decode(rxBuffer[5], rxBuffer[6]);
  byte len_l = decode(rxBuffer[7], rxBuffer[8]);
  uint16_t total_len_data = (len_h << 8) | len_l;

  // Verifica se o tamanho cabe no buffer do programa (a ser definido em ctl)
  // e se corresponde ao payload recebido.
  int payload_ascii_len = idxRxBuffer - 3 - 9; // Tamanho do payload de dados em chars ASCII
  if ((payload_ascii_len / 2) != total_len_data) {
    printf("Erro: tamanho do payload nao corresponde ao declarado.\n");
    return;
  }
  
  // Decodifica os dados do programa
  byte program_data[total_len_data];
  int rx_idx = 9; // Início do payload de dados no rxBuffer
  for (int i = 0; i < total_len_data; i++) {
    program_data[i] = decode(rxBuffer[rx_idx], rxBuffer[rx_idx + 1]);
    rx_idx += 2;
  }
  
  // Passa os dados para o controller
  bool result = ctl_WriteProgram(program_data, total_len_data);
  
  // --- Monta resposta de confirmação (ACK) ---
  // Apenas um eco simples do endereço e função
  byte resp_binary[2];
  resp_binary[0] = MY_ADDRESS;
  resp_binary[1] = WRITE_FILE;
  byte lrc = calculateLRC(resp_binary, 2);
  
  sprintf((char*)txBuffer, ":%02X%02X%02X", resp_binary[0], resp_binary[1], lrc);
  
  sendTxBufferToSerialUSB();
}

void processMessage() {
  // O debug agora está aqui para garantir que vemos o buffer antes de qualquer coisa.
  printf("DEBUG: Processando buffer (len=%d): ", idxRxBuffer);
  for(int i = 0; i < idxRxBuffer; i++) {
    if (rxBuffer[i] >= ' ' && rxBuffer[i] <= '~') {
      putchar(rxBuffer[i]);
    } else {
      printf("[%02X]", rxBuffer[i]);
    }
  }
  printf("\n");

  if (!checkLRC()) {
    printf("Erro de LRC!\n");
    return; // Apenas retorna, o reset do estado será feito fora.
  }

  int functionCode = decode(rxBuffer[3], rxBuffer[4]);
  switch (functionCode) {
    case READ_REGISTER:  processReadRegister(); break;
    case WRITE_REGISTER: processWriteRegister(); break;
    case WRITE_FILE:     processWriteFile(); break;
    default: printf("Funcao desconhecida: 0x%02X\n", functionCode); break;
  }
}

void receiveMessage() {
  int ch;
  // Não usamos um loop while aqui. A tarefa já faz o loop.
  // Lemos apenas um caractere por vez que a tarefa roda.
  if ((ch = getchar_timeout_us(0)) != PICO_ERROR_TIMEOUT) {
    if (_state == HUNTING_FOR_START_OF_MESSAGE) {
      if (ch == ':') {
        idxRxBuffer = 0;
        rxBuffer[idxRxBuffer++] = ch;
        _state = HUNTING_FOR_END_OF_MESSAGE;
      }
    } else if (_state == HUNTING_FOR_END_OF_MESSAGE) {
      if (idxRxBuffer >= MAX_RX_SIZE) {
        // Buffer estourou, reseta.
        _state = HUNTING_FOR_START_OF_MESSAGE;
        return;
      }
      
      rxBuffer[idxRxBuffer] = ch; // Adiciona o char no índice atual

      // A detecção do fim da mensagem é a chave.
      // Verificamos se o char atual é '\n' e o anterior era '\r'.
      if (rxBuffer[idxRxBuffer] == '\n' && idxRxBuffer > 0 && rxBuffer[idxRxBuffer - 1] == '\r') {
        _state = MESSAGE_READY;
      }
      
      idxRxBuffer++; // Incrementa o índice para a próxima posição
    }
  }
}

void com_executeCommunication() {
    receiveMessage();

    if (_state == MESSAGE_READY) {
        processMessage();

        // Imediatamente reseta o estado para a próxima mensagem.
        _state = HUNTING_FOR_START_OF_MESSAGE;
        idxRxBuffer = 0;
    }
}