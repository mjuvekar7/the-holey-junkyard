#define ON  0xB1
#define OFF 0x84

#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/sleep.h>

void init (void);

int main (void)
{    
    DDRB = _BV(DDB0);
    set_sleep_mode(SLEEP_MODE_IDLE);
    sei();
    init();
    
    while (1) sleep_mode();
}

void init (void)
{
    uint16_t UBBRValue = 0x19;  // 2400 baud
    UBRRH = (unsigned char) (UBBRValue >> 8);
    UBRRL = (unsigned char) UBBRValue;
    
    UCSRB |= _BV(RXEN) | _BV(RXCIE);
}

ISR (USART_RXC_vect)
{
    if (UDR == ON) PORTB |= _BV(PB0);
    if (UDR == OFF) PORTB &= ~_BV(PB0);
}