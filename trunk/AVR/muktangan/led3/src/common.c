#include <avr/io.h>
#include "common.h"

uint8_t full_buf[FULL_X_SIZE][FULL_Y_SIZE];
uint8_t disp_buf[DISP_X_SIZE][DISP_Y_SIZE];

uint8_t x_off = 0, y_off = 0;

