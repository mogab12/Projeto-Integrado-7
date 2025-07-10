#ifndef __TRJ_CONTROL_H
#define __TRJ_CONTROL_H

#include <stdint.h>

#define CMD_NO_CMD      0
#define CMD_START       1
#define CMD_SUSPEND     2
#define CMD_RESUME      3
#define CMD_STOP        4

typedef struct {
	uint8_t command;
} tcl_Data;

extern void tcl_CreateTask(void);

#endif // __TRJ_CONTROL_H