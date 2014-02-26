#ifndef _SHAPES_H
#define _SHAPES_H

#include <avr/io.h>
#include "common.h"

struct Point
{
    uint8_t x, y, z;
};

struct Line
{
    struct Point s, e;
};

struct Rect
{
    struct Point c, p0, p1;
};

struct Plane
{
    uint8_t loc;
};
/**
 * implement more shapes
 *  -- triangle
 *  -- circle
 *  -- sphere
 *  -- cuboid
 */

void pt_on (struct Point *p)
{
    full_buf[p->x][p->y] |= (1 << p->z);
}

void pt_off (struct Point *p)
{
    full_buf[p->x][p->y] &= ~(1 << p->z);
}

void ln_on (struct Line *l)
{
    uint8_t x, y, z;
    float t;
    for (t = 0; t <= 1; t += 0.05)
    {
        x = (l->s.x + l->e.x * t + 0.5);
        y = (l->s.y + l->e.y * t + 0.5);
        z = (l->s.z + l->e.z * t + 0.5);
        full_buf[x][y] |= (1 << z);
    }
}

void ln_off (struct Line *l)
{
    uint8_t x, y, z;
    float t;
    for (t = 0; t <= 1; t += 0.05)
    {
        x = (l->s.x + l->e.x * t + 0.5);
        y = (l->s.y + l->e.y * t + 0.5);
        z = (l->s.z + l->e.z * t + 0.5);
        full_buf[x][y] &= ~(1 << z);
    }
}

void r_on (struct Rect *r)
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

    ln_on(&s0);
    ln_on(&s1);
    ln_on(&s2);
    ln_on(&s3);
}

void r_off (struct Rect *r)
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

    ln_off(&s0);
    ln_off(&s1);
    ln_off(&s2);
    ln_off(&s3);
}

void pl_on (struct Plane *p)
{
    uint8_t pos = p->loc & 0x3F;
    switch(p->loc >> 6)
    {
        case 1:
            for (uint8_t i = 0; i < FULL_Y_SIZE; i++)
                full_buf[pos][i] |= 0xFF;
            break;
        case 2:
            for (uint8_t i = 0; i < FULL_X_SIZE; i++)
                full_buf[i][pos] |= 0xFF;
            break;
        case 3:
            for (uint8_t i = 0; i < FULL_X_SIZE; i++)
                for (uint8_t j = 0; j < FULL_Y_SIZE; j++)
                    full_buf[i][j] |= (1 << pos);
    }
}

void pl_off (struct Plane *p)
{
    uint8_t pos = p->loc & 0x3F;
    switch(p->loc >> 6)
    {
        case 1:
            for (uint8_t i = 0; i < FULL_Y_SIZE; i++)
                full_buf[pos][i] &= 0x00;
            break;
        case 2:
            for (uint8_t i = 0; i < FULL_X_SIZE; i++)
                full_buf[i][pos] &= 0x00;
            break;
        case 3:
            for (uint8_t i = 0; i < FULL_X_SIZE; i++)
                for (uint8_t j = 0; j < FULL_Y_SIZE; j++)
                    full_buf[i][j] &= ~(1 << pos);
    }
}

#endif

