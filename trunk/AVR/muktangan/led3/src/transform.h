#include <avr/io.h>
#include "shapes.h"

void shift (int8_t dir, uint8_t mag)
{
    static int i, j;
    
    if (dir > 0)
        if (dir == 1)
        {
            for (i = FULL_X_SIZE - 1; i >= mag; i--)
                for (j = 0; j < FULL_Y_SIZE; j++)
                    full_buf[i][j] = full_buf[i-mag][j];
            for (i = 0; i < mag; i++)
                for (j = 0; j < FULL_Y_SIZE; j++)
                    full_buf[i][j] = 0x00;
        }
        else if (dir == 2)
        {
            for (i = 0; i < FULL_X_SIZE; i++)
                for (j = FULL_Y_SIZE; j >= mag; j--)
                    full_buf[i][j] = full_buf[i][j-mag];
            for (i = 0; i < FULL_X_SIZE; i++)
                for (j = 0; j < mag; j++)
                    full_buf[i][j] = 0x00;
        }
        else
            for (i = 0; i < FULL_X_SIZE; i++)
                for (j = 0; j < FULL_Y_SIZE; j++)
                    full_buf[i][j] = full_buf[i][j] << mag;
    else
        if (dir == -1)
            for (j = 0; j < FULL_Y_SIZE; j++)
            {
                for (i = 0; i < FULL_X_SIZE - mag; i++)
                    full_buf[i][j] = full_buf[i+mag][j];
                for (i = FULL_X_SIZE - mag; i < FULL_X_SIZE; i++)
                    full_buf[i][j] = 0x00;
            }
        else if (dir == -2)
            for (i = 0; i < FULL_X_SIZE; i++)
            {
                for (j = 0; j < FULL_Y_SIZE - mag; j++)
                    full_buf[i][j] = full_buf[i][j+mag];
                for (j = FULL_Y_SIZE - mag; j < FULL_Y_SIZE; j++)
                    full_buf[i][j] = 0x00;
            }
        else
            for (i = 0; i < FULL_X_SIZE; i++)
                for (j = 0; j < FULL_Y_SIZE; j++)
                    full_buf[i][j] = full_buf[i][j] >> mag;
}

