#ifndef __command_interpreter_h
#define __command_interpreter_h

#include <stdint.h>

//Esses defines foram feitos com base na tabela da "Memória" do Raspberry Pi presente na aula de modbus. 
// identification of registers to read 
#define REG_X 9
#define REG_Y 10
#define REG_Z -1 //não usado
#define REG_LINHA 11 //

// identification of register to write
#define REG_START 1
#define REG_SUSPEND 2 
#define REG_RESUME  3
#define REG_STOP    4




// error
#define CTL_ERR -1

extern int ctl_ReadRegister(int registerToRead);
extern int ctl_WriteRegister(int registerToWrite, int value);
extern int ctl_WriteProgram(uint8_t* programBytes);
extern void ctl_init();

#endif
