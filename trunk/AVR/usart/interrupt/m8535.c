#define SIG 0xB1
#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/sleep.h>

void init (void);

int main (void)
{
    DDRB = _BV(DDB0);
    set_sleep_mode(SLEEP_MODE_PWR_DOWN);
    MCUCSR |= _BV(ISC2);
    GICR = _BV(INT2);
    sei();
    init();
    
    while (1) sleep_mode();
}

void init (void)
{
    uint16_t UBBRValue = 0x0C;  // 4800 baud
    UBRRH = (unsigned char) (UBBRValue >> 8);
    UBRRL = (unsigned char) UBBRValue;
    
    UCSRB |= _BV(TXEN);
}

ISR (INT2_vect)
{
    PORTB ^= _BV(PB0);
    UCSRA |= _BV(TXC);
    UDR = SIG;
    loop_until_bit_is_set(UCSRA, TXC);
    MCUCSR ^= _BV(ISC2);
}