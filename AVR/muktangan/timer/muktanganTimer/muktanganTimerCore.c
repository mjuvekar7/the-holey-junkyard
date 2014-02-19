#define F_CPU 1000000UL
#define DONT_CARE 0
#define INCREMENT 1
#define DECREMENT 2
#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>
int readInput();
void resetCounter();
volatile short Counter;
int main(void)
{
	DDRB |= ((1<<2) | (1<<3) | (1<<4) | (1<<5));
        PORTB |= ((1<<0) | (1<<1));
	resetCounter();
	GIMSK |= (1<<INT0);
	MCUCR |= (1<<ISC01);
	sei();
	while(1)
	{
		int input = readInput();
		if (input == INCREMENT)
		{
			PORTB |= (1<<2);
			PORTB |= (1<<3);
			_delay_ms(100);
			PORTB &= ~(1<<3);
			Counter++;
		}
		if (input == DECREMENT)
		{
			PORTB &= ~(1<<2);
			PORTB |= (1<<3);
			_delay_ms(100);
			PORTB &= ~(1<<3);
			Counter--;
		}
		_delay_ms(500);
	} 		
}
int readInput() 
{
	if (PINB == (PINB & ~(1<<0)))
	{
		return INCREMENT;
	}
	else
	{
		if (PINB == (PINB & ~(1<<1)))
		{
			return DECREMENT;
		}
		else
		{
			return DONT_CARE;
		}
	}
}
void resetCounter()
{
	PORTB |= (1<<5);
	PORTB &= ~(1<<5);
	Counter =0;
	PORTB |= (1<<4);
}
ISR(INT0_vect)
{
	PORTB &= ~(1<<2);
	PORTB &= ~(1<<4);
	int i;
	for (i = 0; i < Counter; i++)
	{
		_delay_ms(900);
		PORTB |= (1<<3);
		_delay_ms(100);
		PORTB &= ~(1<<3);
	}
	resetCounter();
	sei();
}