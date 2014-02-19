#include <avr/io.h>
#include "common.h"
#include "main.h"

int main (void)
{
    init();
    uint8_t x, y;
    for (x = 0; x < DISP_X_SIZE; x++)
        for (y = 0; y < DISP_Y_SIZE; y++)
            disp_buf[x][y] = 0x1F;
    while (1);
    return 0;
}
