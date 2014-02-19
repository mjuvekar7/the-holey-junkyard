// define statements
#define SIG 0xffcc0001

#define START_ON  4500
#define START_OFF 4500
#define MARK_ON   560
#define MARK_OFF  1690
#define SPACE_ON  560
#define SPACE_OFF 560

// standard includes
#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/sleep.h>
#include <util/delay.h>

// function declarations
void init_timer (void);
void transmit (uint32_t data);
void transmit_mark (void);
void transmit_space (void);

// main
int main (void)
{
    // init i/o
    DDRC |= _BV(DDC0) | _BV(DDC1);
    
    // init timer
    init_timer();
    
    // set sleep mode
    set_sleep_mode(SLEEP_MODE_IDLE);
    
    // enable interrupts
    MCUCSR |= _BV(ISC2);
    GICR = _BV(INT2);
    sei();
    
    // sleep forever
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

void transmit (uint32_t data)
{
    // transmit start bit
    PORTC |= _BV(PC0);
    _delay_ms(START_ON / 1000);
    PORTC &= ~_BV(PC0);
    _delay_ms(START_OFF / 1000);
            
    // transmit data
    uint8_t i;
    for (i = 0; i < 32; i++) (bit_is_set(data, i))? transmit_mark(): transmit_space();
    
    // transmit stop bit
    transmit_space();
}

void transmit_mark (void)
{
    // transmit mark
    PORTC |= _BV(PC0);
    _delay_us(MARK_ON);
    PORTC &= ~_BV(PC0);
    _delay_ms(MARK_OFF / 1000);
}

void transmit_space (void)
{
    // transmit space
    PORTC |= _BV(PC0);
    _delay_us(SPACE_ON);
    PORTC &= ~_BV(PC0);
    _delay_us(SPACE_OFF);
}

ISR (INT2_vect)
{
    // disable interrupts
    cli();
    
    // LED on
    PORTC |= _BV(PC1);
    
    // transmit SIG
    transmit(SIG);
    
    // LED off
    PORTC &= ~_BV(PC1);
    
    // enable interrupts
    sei();
}