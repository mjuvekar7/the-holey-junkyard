/*
 * function to receive frame from upper layer:
 * blocks till buffer contains full frame
 *
 * then display frame (later:check for optimizations)
 * for every voxel in frame:
 *   turn on led for appropriate time
 *   achieve refresh rate ~40 Hz
 */

#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>
#include "common.h"
#include "repr.h"

volatile uint8_t x, y, i, j;

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

/*int main (void)
{
  while(1)
  {
    for (int i = 0; i < DISP_X_SIZE; i++)
        for (int j = 0; j < DISP_Y_SIZE; j++)
            disp_buf[i][j] = full_buf[i+x_off][j+y_off];
    // PORTA -> Z port
    // PORTB -> input for demuxer
    PORTA |= disp_buf[x][y];
    PORTB |= mux(x, y);
    if (y++ == DISP_Y_SIZE - 1)
    {
        y = 0;
        if (x++ == DISP_X_SIZE - 1)
            x = 0;
    }
    _delay_us(3);
  }
}
*/

ISR(TIMER0_COMP_vect)
{
    cli();
    for (i = 0; i < DISP_X_SIZE; i++)
        for (j = 0; j < DISP_Y_SIZE; j++)
            disp_buf[i][j] = full_buf[i+x_off][j+y_off];
    // PORTA -> Z port
    // PORTB -> input for demuxer
    PORTA |= disp_buf[x][y];
    PORTB |= mux(x, y);
    y++;
    if (y == DISP_Y_SIZE)
    {
        y = 0;
        x++;
        if (x == DISP_X_SIZE)
            x = 0;
    }
    sei();
}
