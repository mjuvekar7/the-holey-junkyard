#ifndef _TRANSFORM_H
#define _TRANSFORM_H

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

void shift_p (struct Point *p, int8_t dir, uint8_t mag)
{
    if (dir < 0)
    {
	if (dir > -3)
	    if (dir > -2)
		p.x = p.x - mag;
	    else
		p.y = p.y - mag;
	else
	    if (dir > -4)
		p.z = p.z - mag;
	    else
#               warning "Arguement value outside required range"
    }
    else if (dir > 0)
    {
	if (dir < 3)
	    if (dir < 2)
		p.x = p.x + mag;
	    else
		p.y = p.y + mag;
	else
	    if (dir < 4)
		p.z  = p.z + mag;
	    else
#               warning "Arguement value outside required range"
    }
    else
#               warning "Arguement value outside required range"
}

void shift_l (struct Line *l, int8_t dir, uint8_t mag)
{
    shift_p (&l.s, dir, mag);
    shift_p (&l.e, dir, mag);
}

void shift_r (struct Rect *r, int8_t dir, uint8_t mag)
{
    struct Line s0, s1, s2, s3;
   
    s0.s = r->c;
    s0.e = r->p0;

    s1.s = r->c;
    s1.e = r->p1;

    struct Point d;
    d.x = r->p0.x - r->c.x + r->p1.x;
    d.y = r->p0.y - r->c.y + r->p1.y;
    d.z = r->p0.z - r->c.z + r->p1.z;
    
    s2.s = r->p0;
    s2.e = d;

    s3.s = r->p1;
    s3.e = d;

    shift_l(&s0, dir, mag);
    shift_l(&s1, dir, mag);
    shift_l(&s2, dir, mag);
    shift_l(&s3, dir, mag);
}

#endif
