#define F_CPU 1000000L
#define ON  0x4E
#define OFF 0x9C

#include <avr/io.h>
#include <util/delay.h>

void init (void);
void transmit (unsigned char);

int main(void)
{
    DDRB = _BV(DDB0);
    PORTB = _BV(PB1);
    
    init();
    
    while (1)
    {
	PORTB &= ~_BV(PB0);
	transmit(OFF);
	while (bit_is_set(PINB, PB1)) asm volatile ("nop");
	
	PORTB |= _BV(PB0);
	transmit(ON);
	while (bit_is_clear(PINB, PB1)) asm volatile ("nop");
    }
}

void init (void)
{
    uint16_t UBBRValue = 0x19;
    UBRRH = (unsigned char) (UBBRValue >> 8);
    UBRRL = (unsigned char) UBBRValue;
    
    UCSRB |= _BV(TXEN);
}

void transmit (unsigned char data)
{
    loop_until_bit_is_set(UCSRA, UDRE);
    UDR = data;
}