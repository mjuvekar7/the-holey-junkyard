#include <avr/io.h>
#include "common.h"

uint8_t x_off, y_off;

void redraw (void)
{
    for (int i = 0; i < DISP_X_SIZE; i++)
        for (int j = 0; j < DISP_Y_SIZE; j++)
            disp_buf[i][j] = full_buf[i+x_off][j+y_off];
}
