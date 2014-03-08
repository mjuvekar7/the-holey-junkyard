#include <avr/io.h>
#include <util/delay.h>
#include "common.h"
#include "main.h"

uint8_t col = 0;

uint8_t mux (uint8_t x, uint8_t y)
{
    uint8_t x_num = 0, y_num = 0, i;
    for (i = 0; i < 5; i++)
    {
        if (x & (1 << i)) x_num = i;
        if (y & (1 << i)) y_num = i;
    }
    return x_num * 5 + y_num;
}

void light (uint8_t x, uint8_t y)
{
    // PORTA -> Z port
    // PORTB -> input for demuxer
    PORTA = disp_buf[x][y];
    // PORTB = mux(x, y);
    PORTB = col++;
    if (col > 24) col = 0;
}

int main (void)
{
    init();
    uint8_t x, y;
    for (x = 0; x < DISP_X_SIZE; x++)
        for (y = 0; y < DISP_Y_SIZE; y++)
            disp_buf[x][y] = 0xFF;
    while (1)
    {
        for (x = 0; x < DISP_X_SIZE; x++)
            for (y = 0; y < DISP_Y_SIZE; y++)
            {
                light(x, y);
                _delay_ms(1000);
            }
    }
    return 0;
}

