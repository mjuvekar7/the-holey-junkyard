#include <avr/io.h>
#include "common.h"
#include "main.h"

int main (void)
{
    init();
    uint8_t x, y;
    for (x = 0; x < FULL_X_SIZE; x++)
        for (y = 0; y < FULL_Y_SIZE; y++)
            full_buf[x][y] = 0xFF;
    while (1);
    return 0;
}
