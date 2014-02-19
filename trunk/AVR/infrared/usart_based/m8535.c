#define ON  0xB1
#define OFF 0x84

#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/sleep.h>

void init_timer (void);
void init_usart (void);

int main (void)
{
    DDRB = _BV(DDB0);
    DDRD = _BV(DDD5);
    set_sleep_mode(SLEEP_MODE_IDLE);
    MCUCSR |= _BV(ISC2);
    GICR = _BV(INT2);
    sei();
    init_timer();
    init_usart();
    
    while (1) sleep_mode();
}

void init_timer (void)
{
    // continuous PWM output at 38 kHz, 50% duty
    TCCR1A = _BV(WGM11) | _BV(COM1A1);
    TCCR1B = _BV(CS10) | _BV(WGM12) | _BV(WGM13);
    ICR1 = 25;
    OCR1A = 12;
}

void init_usart (void)
{
    uint16_t UBBRValue = 0x19;  // 2400 baud
    UBRRH = (unsigned char) (UBBRValue >> 8);
    UBRRL = (unsigned char) UBBRValue;
    
    UCSRB |= _BV(TXEN);
}

ISR (INT2_vect)
{
    PORTB ^= _BV(PB0);
    uint8_t i;
    for (i = 0; i < 10; i++)
    {
	UCSRA |= _BV(TXC);
	UDR = ((bit_is_set(MCUCSR, ISC2))? ON: OFF);
	loop_until_bit_is_set(UCSRA, TXC);
    }
    MCUCSR ^= _BV(ISC2);
}