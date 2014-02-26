#ifndef _SHAPES_H
#define _SHAPES_H

#include <avr/io.h>
#include "common.h"

struct Point
{
    uint8_t x, y, z;
}

struct Line
{
    struct Point s, e;
}

struct Rect
{
    struct Point c, p0, p1;
}

/**
 * implement more shapes
 *  -- triangle
 *  -- circle
 *  -- sphere
 *  -- cuboid
 */

void toggle_p (struct Point *p)
{
    full_buf[p->x][p->y] ^= (1 << p->z);
}

void toggle_l (struct Line *l)
{
    uint8_t x, y, z;
    float t;
    for (t = 0; t <= 1; t += 0.05)
    {
        x = (l->s.x + l->e.x * t + 0.5);
        y = (l->s.y + l->e.y * t + 0.5);
        z = (l->s.z + l->e.z * t + 0.5);
        full_buf[x][y] ^= (1 << z);
    }
}

void toggle_r (struct Rect *r)
{
    struct Line s0, s1, s3, s4;

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

    toggle_l(&s0);
    toggle_l(&s1);
    toggle_l(&s2);
    toggle_l(&s3);
}

#endif

