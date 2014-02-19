#define F_CPU 1000000L
#define ON  0x4E
#define OFF 0x9C

#include <avr/io.h>
#include <util/delay.h>

void init (void);
unsigned char receive (void);

int main(void)
{
    DDRB |= (1<<PB0);
    
    unsigned char data;
    init();
    
    while (1)
    {
	data = receive();
	
	if (data == ON)
	{
	    PORTB |= _BV(PB0);
	}
	else if (data == OFF)
	{
	    PORTB &= ~_BV(PB0);
	}
    }
}

void init (void)
{
    uint16_t UBBRValue = 0x19;
    UBRRH = (unsigned char) (UBBRValue >> 8);
    UBRRL = (unsigned char) UBBRValue;
    
    UCSRB |= (1<<RXEN);
}

unsigned char receive (void)
{
    loop_until_bit_is_set(UCSRA, RXC);
    return UDR;
}