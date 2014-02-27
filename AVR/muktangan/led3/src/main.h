#ifndef _MAIN_H
#define _MAIN_H

#include <avr/io.h>
#include <avr/interrupt.h>
#include "repr.h"
#include "shapes.h"
#include "transform.h"

// must call before anything else
void init (void)
{
    DDRA |= 0xFF;
    DDRB |= 0xFF;
    // for physical layer
    TCCR0 |= _BV(WGM01) | _BV(CS02);
    OCR0 = 0x61;
    TIMSK |= _BV(OCIE0);

    // for representative layer
    x_off = 0;
    y_off = 0;

    // enable interrupts
    sei();
}

#endif

