/*
 * muktangan.c
 *
 * Created: 2013-02-10 13:31:12
 * Revision: 2013-02-23 09:51:45
 * Primary Contributor: Mandar J.
 * Secondary Contributor: Shardul C.
 */

#define F_CPU 1000000UL

#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>

volatile short timersec;
short timerStarted;
void checkTimerStarted();

int main(void)
{

	//PB0 -- clock out
	//PB1 -- RTC MSD (hour)
	//PB2 -- RTC LSD1 (hour)
	//PB3 -- RTC LSD2 (hour)
	//PB4 -- required condition achieved
        //PB5 -- reset hour
	//PB6 -- clock for timer
	//PB7 -- up/down for timer
	//PD0 -- start button for timer
	//PD2 -- up button for timer
	//PD3 -- down button for timer

	//setting output pins
	DDRB = 0b11110001;
	DDRD = 0b00001101;
	
	//setting pull-up resistors
	PORTB = 0b00001110;
	PORTD = 0b00000001;

	GIMSK |= ((1<<INT0) | (1<<INT1));
	MCUCR |= (1<<ISC01);
	sei();		

	short i;
	short min = 0;
	short hour = 0;
	short reqmin = 30;
	short reqhour = 5;
	
	while(1)
	{
		//59 sec delay
		for (i = 0; i < 60; i++)
		{
			_delay_ms(900);
			checkTimerStarted();  
			if (timerStarted == 1)
			{
				PORTB ^= (1<<6);
				_delay_ms(50);
				PORTB ^= (1<<6);
				timersec--;
				if (timersec == 0)
				{
					PORTB &= ~(1<<6);
					PORTB |= (1<<4);
					_delay_ms(50);
					PORTB &= ~(1<<4);
					timerStarted = 0;
				}
				else
				{
					_delay_ms(50);
				}
			}
			else
			{
				_delay_ms(50);
			}
		}

		//pulse
		PORTB |= (1<<0);
		_delay_ms(900);
		PORTB &= ~(1<<0);
		min++;
		if (min == 60)
		{
			min = 0;
			hour++;
		}
		if (hour == 13)
		{
			hour = 0;
		}
		if ((min == reqmin) && (hour == reqhour))
		{
			PORTB |= (1<<4);
			_delay_ms(50);
			PORTB &= ~(1<<4);
		}
		else 
		{
			_delay_ms(50);
		}

		//clock should count only till 12:00
		if (PINB == (PINB | ((1<<1) | (1<<2) | (1<<3))))
		{
			PORTB |= (1<<5);
			_delay_ms(50);
			PORTB &= ~(1<<5);
		} 
		else 
		{
			_delay_ms(50);
		}
	}
}

ISR(INT0_vect)
{
	PORTB |= (1<<7);
	PORTB |= (1<<6);
	_delay_ms(20);
	PORTB &= ~(1<<6);
	PORTB &= ~(1<<7);
	timersec++;
}

ISR(INT1_vect)
{
	PORTB &= ~(1<<7);
	PORTB |= (1<<6);
	_delay_ms(20);
	PORTB &= ~(1<<6);
	timersec--;
}

void checkTimerStarted()
{
	if (PIND == (PIND | (1<<0)))
	{
		timerStarted = 1;
	}
	else 
	{
        	timerStarted = 0;  
	}
}