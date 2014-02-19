// define protocol timings
#define START_ON  4500
#define START_OFF 4500
#define MARK_ON   560
#define MARK_OFF  1690
#define SPACE_ON  560 // not used: MARK_ON used instead
#define SPACE_OFF 560
#define OFFSET    500

// define LCD ports, pins
#define DATA_DDR DDRA
#define CTRL_DDR DDRB

#define DATA_PORT PORTA
#define CTRL_PORT PORTB

#define RS   0
#define R_W  1
#define CLK  2
#define BUSY 7

// headers
#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/sleep.h>
// #include <avr/wdt.h>
#include <util/delay.h>
#include <stdlib.h>
#include "lcd.h"

// variables
volatile uint16_t time;
uint32_t data;
char data_msg[16];

// function declarations
void init_timer (void);
void receive (uint32_t *);

int main (void)
{    
    // timer init
    init_timer();
    
    // display init
    default_init();
    
    // sleep mode set
    set_sleep_mode(SLEEP_MODE_IDLE);
    
    // enable interrupts
    sei();
    
    _delay_ms(200);
    
    while (1)
    {
        sleep_mode();
        
        receive(&data);        
        ultoa(data, data_msg, 16);
        output(data_msg);
    }
}

void init_timer (void)
{
    TCCR1B = _BV(ICES1) | _BV(CS10);
    TIMSK = _BV(TICIE1);
}

void receive (uint32_t *data)
{
    /*
     * receive header
     * wait for low -> high
     * t/c = 0
     * wait for high -> low
     * if t/c = ~4500
     * t/c = 0
     * wait for low -> high
     * if t/c = ~4500
     * 32 times: 
     * t/c = 0
     * wait for high -> low
     * if t/c = ~560 then
     * t/c = 0
     * wait for low -> high
     * if t/c = ~560 then
     * record space
     * else if t/c = ~1690 then
     * record mark
     * end if
     * end if
     * end 32 times
     * wait for high -> low
     */
    
    uint8_t i;    
    TCNT1 = 0;
    sleep_mode();
    if ((time >= (START_ON - OFFSET)) && (time <= (START_ON + OFFSET)))
    {
        TCNT1 = 0;
        sleep_mode();
        if ((time >= (START_OFF - OFFSET)) && (time <= (START_OFF + OFFSET))) i = 1;
    }
            
    if (i == 1)
    {
        // wdt_enable(WDTO_30MS);
        for (i = 0; i < 32; i++)
        {
            TCNT1 = 0;
            sleep_mode();
            // wdt_reset();
            if ((time >= (MARK_ON - OFFSET)) && (time <= (MARK_ON + OFFSET)))
            {
                TCNT1 = 0;
                sleep_mode();
                if ((time >= (SPACE_OFF - OFFSET)) && (time <= (SPACE_OFF + OFFSET))) *data &= ~_BV(i);
                else if ((time >= (MARK_OFF - OFFSET)) && (time <= (MARK_OFF + OFFSET))) *data |= _BV(i);
            }
        }       
        sleep_mode();
        // wdt_disable();
    }
}

ISR (TIMER1_CAPT_vect)
{
    time = ICR1;
    TCCR1B ^= _BV(ICES1);
}
