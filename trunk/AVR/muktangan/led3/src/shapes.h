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
    struct Point p0, p1;
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
        x = (l->p0.x + l->p1.x * t + 0.5);
        y = (l->p0.y + l->p1.y * t + 0.5);
        z = (l->p0.z + l->p1.z * t + 0.5);
        full_buf[x][y] ^= (1 << z);
    }
}

void toggle_r (struct Rect *r)
{
    struct Line s0, s1, s3, s4;

    s0.p0 = r->c;
    s0.p1 = r->p0;

    s1.p0 = r->c;
    s1.p1 = r->p1;

    struct Point d;
    d.x = r->p0.x - r->c.x + r->p1.x;
    d.y = r->p0.y - r->c.y + r->p1.y;
    d.z = r->p0.z - r->c.z + r->p1.z;
    
    s2.p0 = r->p0;
    s2.p1 = d;

    s3.p0 = r->p1;
    s3.p1 = d;

    toggle_l(s0);
    toggle_l(s1);
    toggle_l(s2);
    toggle_l(s3);
}

#endif

