/*
 * muktanganRTC.c
 *
 * Created: 2/10/2013 13:31:12 
 * Revision: 2013-02-22 09:50:33 
 * Primary Contributor: Mandar J.
 * Secondary Contributor: Shardul C.
 */

#define F_CPU 1000000UL

#include <avr/io.h>
#include <util/delay.h>

int main(void)
{

	//PB0 -- clock out
	//PB1 -- RTC MSD (hour)
	//PB2 -- RTC LSD1 (hour)
	//PB3 -- RTC LSD2 (hour)
	//PB4 -- required condition achieved
        //PB5 -- reset hour

	//setting output pins
	DDRB = 0b00110001;
	
	//setting pull-up resistors
	PORTB = 0b00001110;

	short min = 0;
	short hour = 0;
	short reqmin = 30;
	short reqhour = 5;
	
	while(1)
	{
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