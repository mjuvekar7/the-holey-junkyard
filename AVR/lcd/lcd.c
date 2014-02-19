// define LCD ports, pins
#define DATA_DDR DDRA
#define CTRL_DDR DDRB

#define DATA_PORT PORTA
#define CTRL_PORT PORTB

#define RS   0
#define R_W  1
#define CLK  2
#define BUSY 7

// standard includes
#include <avr/io.h>
#include <util/delay.h>
#include "lcd.h"

// variables and function declarations
char msg_one[] = "First line -- addresses 0x00 to 0x28";
char msg_two[] = "Second line -- addresses 0x40 to 0x68";

// main
int main (void)
{
    // initialize display
    default_init();
    
    uint8_t i;
    for (i = 0; msg_one[i] != '\0'; i++) send_char(msg_one[i]);
    
    set_addr_ddram(0x40);
    DATA_PORT = 0; // so that command is not repeated
    _delay_us(50);
    
    for (i = 0; msg_two[i] != '\0'; i++) send_char(msg_two[i]);
    
    // forever
    while (1)
    {
        _delay_ms(500);
        send_cmd(SHIFT_L);        
    }
}