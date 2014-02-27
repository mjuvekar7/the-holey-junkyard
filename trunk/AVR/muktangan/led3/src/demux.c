#include <avr/io.h>
#include <util/delay.h>

int main (void)
{
    /*
     * set PORTA pins 0-4 as input
     * set PORTA pins 5-7 as output
     *     PORTB pins 0-7 as output
     *     PORTC pins 0-7 as output
     *     PORTD pins 0-5 as output
     * remaining PORTD pins 6, 7 -- use later
     */

    /*
     * forever:
     * delay some time (as per requirement)
     * get input
     * if input is 0: turn on A.5
     * if input is 1: turn on A.6
     * if input is 2: A.7
     * if input is 3: B.0
     *  ...
     * if input is 10: B.7
     * if input is 11: C.0
     *  ...
     * if input is 18: C.7
     * if input is 19: D.0
     *  ...
     * if input is 24: D.5
     */
    uint8_t input;

    DDRA &= 0x1F;
    DDRA |= 0xE0;
    DDRB |= 0xFF;
    DDRC |= 0xFF;
    DDRD |= 0x3F;

    PORTA |= 0x1F;

    while (1)
    {
	input = PORTA;
	input &= ~0xE0;

	//TODO -- delay

	if (input < 13)
            if (input < 7)
                if (input < 4)
                    if (input < 2)
                        if (input < 1)
                            PORTA |= _BV(PA5);
                        else
                            PORTA |= _BV(PA6);
                    else if (input < 3)
                        PORTA |= _BV(PA7);
                    else
                        PORTB |= _BV(PB0);
                else
                    if (input < 5)
                        PORTB |= _BV(PB1);
                    else if (input < 6)
                        PORTB |= _BV(PB2);
                    else
                        PORTB |= _BV(PB3);
            else
                if (input < 10)
                    if (input < 8)
                        PORTB |= _BV(PB4);
                    else if (input < 9)
                        PORTB |= _BV(PB5);
                    else
                        PORTB |= _BV(PB6);
                else
                    if (input < 12)
                        if (input < 11)
                            PORTB |= _BV(PB7);
                        else
                            PORTC |= _BV(PC0);
                    else if (input < 13)
                        PORTC |= _BV(PC1);
                    else
                        PORTC |= _BV(PC2);
        else
            if (input < 19)
                if (input < 16)
                    if (input < 14)
                        PORTC |= _BV(PC3);
                    else if (input < 15)
                        PORTC |= _BV(PC4);
                    else
                        PORTC |= _BV(PC5);
                else
                    if (input < 17)
                        PORTC |= _BV(PC6);
                    else if (input < 18)
                        PORTC |= _BV(PC7);
                    else
                        PORTD |= _BV(PD0);
            else
                if (input < 22)
                    if (input < 20)
                        PORTD |= _BV(PD1);
                    else if (input < 21)
                        PORTD |= _BV(PD2);
                    else
                        PORTD |= _BV(PD3);
                else
                    if (input < 23)
                        PORTD |= _BV(PD4);
                    else if (input < 24)
                        PORTD |= _BV(PD5);
                    else
                        PORTD |= _BV(PD6);
    }
}
