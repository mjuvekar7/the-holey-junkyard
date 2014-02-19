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
    struct Line l0, l1;
}

struct Cuboid
{

}

#endif

