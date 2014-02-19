/*
 * muktanganTimer.c
 *
 * Created: 2/10/2013 1:31:12 PM
 * Revision: 2/23/2013 5:12:24 PM
 * Primary Contributor: Mandar J.
 * Secondary Contributor: Shardul C.
 */

//CPU speed -- 1 MHz
#define F_CPU 1000000UL

//define values for input
#define DONT_CARE 0
#define INCREMENT 1
#define DECREMENT 2

//include standard libraries
#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>

//declare functions to read input and to reset the counter
int readInput();
void resetCounter();

//the variable 'Counter' keeps track of the desired time (in seconds)
volatile short Counter;

/* Pin Usage (uC Pins are going to be used as follows):
 * PB0 (INPUT) -- Low = Increment, High = don't care
 * PB1 (INPUT) -- Low = Decrement, High = don't care
 * PB2 (OUTPUT) -- contorls couter to count up or count down.
 * PB3 (OUTPUT) -- gives pulses to counter
 * PB4 (OUTPUT) -- gives pulse when timeout is achieved (currently implemented to drive LED) 
 * PB5 (OUTPUT) -- resets counter
 * INT0 (INTERRUPT) -- when triggered, timer starts count-down 
 */

//the main executing code
int main(void)
{
	//Init PB2, PB3, PB4 and PB5 as output pins
	DDRB |= ((1<<2) | (1<<3) | (1<<4) | (1<<5));

	//Init PB0 and PB1 as input pins
        PORTB |= ((1<<0) | (1<<1));

	//reset counter initially
	resetCounter();
	
	//Set INT0 to be triggered on falling edge
	GIMSK |= (1<<INT0);
	MCUCR |= (1<<ISC01);	

	//check continuously for user input
	while(1)
	{
		//Enable all interrupts
		sei();		

		//read input
		int input = readInput();

		//if input is the 'increment' button, then --
		if (input == INCREMENT)
		{
			//prepare counter to count up 
			PORTB |= (1<<2);

			//give clock pulse to counter
			PORTB |= (1<<3);
			_delay_ms(100);
			PORTB &= ~(1<<3);

			//increment variable 'counter' and wrap-around
			Counter = ((Counter == 99)? 0: (Counter+1));
		}

		//if input is the 'decrement' button, then --
		if (input == DECREMENT)
		{
			//prepare counter to count down 
			PORTB &= ~(1<<2);

			//give clock pulse to counter
			PORTB |= (1<<3);
			_delay_ms(100);
			PORTB &= ~(1<<3);

			//decrement variable 'counter' and wrap-around
			Counter = ((Counter == 0) ? 99 : (Counter-1));
		}

		//wait for a while before reading input again
		_delay_ms(350);
	} 		
}

//read user input
int readInput() 
{
	//if 'increment' button is pressed, then say 'INCREMENT'
	if (PINB == (PINB & ~(1<<0)))
	{
		return INCREMENT;
	}
	else
	{
		//else if 'decrement' button is pressed, then say 'DECREMENT'
		if (PINB == (PINB & ~(1<<1)))
		{
			return DECREMENT;
		}

		//if nothing is pressed, then say 'DONT_CARE'
		else
		{
			return DONT_CARE;
		}
	}
}

//reset counter
void resetCounter()
{
	//give short pulse to reset counter
	PORTB |= (1<<5);
	PORTB &= ~(1<<5);

	//reset variable 'Counter' as well
	Counter =0;

	//turn LED on
	PORTB |= (1<<4);
}

//if timer started (i.e interrupt is trigerred), then --
ISR(INT0_vect)
{
	//disable all interrupts
	cli();

	//prepare the counter to count down
	PORTB &= ~(1<<2);

	//turn LED off
	PORTB &= ~(1<<4);

	//wait for the desired time (the 'Counter' variable)
	int i;
	for (i = 0; i < Counter; i++)
	{
		//wait for 0.9 seconds 
		_delay_ms(900);

		//give clock pulse to counter
		PORTB |= (1<<3);
		_delay_ms(100);
		PORTB &= ~(1<<3);
	}
	
	//reset counter
	resetCounter();
}