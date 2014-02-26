#ifndef _TRANSFORM_H
#define _TRANSFORM_H

#include <avr/io.h>
#include "shapes.h"

void shift_disp (int8_t dir, uint8_t mag)
{
    static uint8_t i, j;
    
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

void shift_pt (struct Point *p, int8_t dir, uint8_t mag)
{
    pt_off(p);
    if (dir < 0)
        if (dir == -1)
            p->x = p->x - mag;
        else if (dir == -2)
            p->y = p->y - mag;
        else
            p->z = p->z - mag;
    else
        if (dir == 1)
            p->x = p->x + mag;
        else if (dir == 2)
            p->y = p->y + mag;
        else
            p->z = p->z + mag;
    pt_on(p);
}

void shift_ln (struct Line *l, int8_t dir, uint8_t mag)
{
    ln_off(l);
    shift_pt(&(l->s), dir, mag);
    shift_pt(&(l->e), dir, mag);
    ln_on(l);
}

void shift_r (struct Rect *r, int8_t dir, uint8_t mag)
{
    r_off(r);
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

    shift_ln(&s0, dir, mag);
    shift_ln(&s1, dir, mag);
    shift_ln(&s2, dir, mag);
    shift_ln(&s3, dir, mag);
    r_on(r);
}

void shift_pl (struct Plane *p, int8_t mag)
{
    pl_off(p);
    p->loc = (p->loc >> 6) | ((p->loc & 0x3F) + mag);
    pl_on(p);
}

#endif
