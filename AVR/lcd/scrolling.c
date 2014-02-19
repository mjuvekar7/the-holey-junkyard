// define LCD ports, pins
#define DATA_DDR DDRA
#define CTRL_DDR DDRB

#define DATA_PORT PORTA
#define CTRL_PORT PORTB

#define DATA_PIN PINA

#define RS   0
#define R_W  1
#define CLK  2
#define BUSY 7

// include headers
#include <avr/io.h>
#include <util/delay.h>
#include "lcd.h"

// things to display
unsigned char one[] = "First message";
unsigned char two[] = "Second message";
unsigned char three[] = "Third message";
unsigned char four[] = "Fourth message";

int main (void)
{
    default_init();
    
    output(one);
    _delay_ms(500);
    _delay_ms(500);
    output(two);
    _delay_ms(500);
    _delay_ms(500);
    output(three);
    _delay_ms(500);
    _delay_ms(500);
    output(four);
    
    while (1);
}