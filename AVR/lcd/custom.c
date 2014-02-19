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
char msg[] = "Battery levels:";
uint8_t batt0[] = {0x0E, 0x1B, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1F};
uint8_t batt1[] = {0x0E, 0x1b, 0x11, 0x11, 0x11, 0x11, 0x1f, 0x1f};
uint8_t batt2[] = {0x0E, 0x1B, 0x11, 0x11, 0x11, 0x1F, 0x1F, 0x1F};
uint8_t batt3[] = {0x0E, 0x1B, 0x11, 0x11, 0x1F, 0x1F, 0x1F, 0x1F};
uint8_t batt4[] = {0x0E, 0x1B, 0x11, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F};
uint8_t batt5[] = {0x0E, 0x1B, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F};
uint8_t batt6[] = {0x0E, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F};
uint8_t smiley[] = {0x00, 0x1B, 0x1B, 0x00, 0x11, 0x0A, 0x04, 0x00};

// main
int main (void)
{
    // initialize display
    default_init();
    
    // create custom characters
    custom_char(0, batt0);
    custom_char(1, batt1);
    custom_char(2, batt2);
    custom_char(3, batt3);
    custom_char(4, batt4);
    custom_char(5, batt5);
    custom_char(6, batt6);
    custom_char(7, smiley);
        
    uint8_t i;
    for (i = 0; msg[i] != '\0'; i++) send_char(msg[i]);
    
    set_addr_ddram(0x40);
    DATA_PORT = 0; // so that command is not repeated
    _delay_us(50);
    
    send_char(0);
    send_char(1);
    send_char(2);
    send_char(3);
    send_char(4);
    send_char(5);
    send_char(6);
    send_char(7);
    
    // do nothing forever
    while (1);
}