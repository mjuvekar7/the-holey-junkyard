/*
 * LCD utilities
 * 
 * contains useful functions for LCD screens.
 * please read comments in code to understand wht's going on.
 * currently in development.
 * 
 * author Shardul Chiplunkar
 */

#ifndef LCD_LIB
#define LCD_LIB

// define standard LCD commands
#define CLEAR      0x01
#define HOME       0x02
#define SET_CURSOR 0x06
#define NO_CURSOR  0x0C
#define NO_BLINK   0x0E
#define BLINK      0x0F
#define SHIFT_L    0x18
#define SHIFT_R    0x1C

// check for defines
#if !defined(DATA_DDR) || !defined(CTRL_DDR) || \
!defined(DATA_PORT) || !defined(CTRL_PORT) || \
!defined(RS) || !defined(R_W) || !defined(CLK) || !defined(BUSY)
#error "LCD ports and pins not defined correctly (some may be missing)"
#endif

#ifndef _20x4
#define _16x2
#endif

// standard includes
#include <avr/io.h>
#include <util/delay.h>

// variables (for scrolling output, 16 by 2)
#ifdef _16x2
unsigned char top[0x28];
unsigned char bottom[0x28];
#endif

// function declarations

// wait till ready
void busy_loop (void);

// clock pulse
void clk (void);

// create custom character
void custom_char (uint8_t, uint8_t[]);

// initialize with default settings
void default_init (void);

// initialization options
void options (uint8_t, uint8_t, uint8_t);

// primary output
void output (unsigned char[]);

// send single character
void send_char (unsigned char);

// send command
void send_cmd (uint8_t);

// switch to CGRAM, set CGRAM address
void set_addr_cgram (uint8_t);

// switch to DDRAM (display), set DDRAM (display) address
void set_addr_ddram (uint8_t);


void busy_loop (void)
{
    // set data port as input
    DATA_DDR = 0;
    
    // enter command read mode
    CTRL_PORT &= ~_BV(RS);
    CTRL_PORT |= _BV(R_W);
    
    // wait while LCD is busy
    while (bit_is_set(DATA_PORT, BUSY)) clk();
    
    // set data port as output
    DATA_DDR = 0xFF;
}

void clk (void)
{
    // pulse on clock pin
    CTRL_PORT |= _BV(CLK);
    asm volatile ("nop");
    asm volatile ("nop");
    asm volatile ("nop");
    CTRL_PORT &= ~_BV(CLK);
}

void custom_char (uint8_t addr, uint8_t pixels[])
{
    set_addr_cgram(addr * 8);
    uint8_t i;
    for (i = 0; i < 8; i++) send_char(pixels[i]);
    set_addr_ddram(0);
}

void default_init (void)
{
    // initialize i/o pins
    DATA_DDR = 0xFF;
    CTRL_DDR = 0xFF;
    
    send_cmd(CLEAR);
    _delay_ms(2);
    
    options(8, 2, 7);
    _delay_us(50);
    
    send_cmd(BLINK);
    _delay_us(50);
}

void options (uint8_t data_mode, uint8_t rows, uint8_t font)
{
    if (data_mode == 4)
    {
        if (rows == 1)
        {
            if (font == 7) send_cmd(0x20);
            else if (font == 10) send_cmd(0x24);
        }
        else if (rows == 2)
        {
            if (font == 7) send_cmd(0x28);
            else if (font == 10) send_cmd(0x2C);
        }
    }
    else if (data_mode == 8)
    {
        if (rows == 1)
        {
            if (font == 7) send_cmd(0x30);
            else if (font == 10) send_cmd(0x34);
        }
        else if (rows == 2)
        {
            if (font == 7) send_cmd(0x38);
            else if (font == 10) send_cmd(0x3C);
        }
    }
}

void output (unsigned char next[])
{
    #ifdef _16x2
    /*
     * copy bottom[] to top[]
     * copy next[] to bottom[]
     * display top[] on top row
     * display bottom[] on bottom row
     */
    
    uint8_t i;
    for (i = 0; i < 0x28; i++)
    {
        top[i] = bottom[i];
        bottom[i] = next[i];
    }
    send_cmd(CLEAR);
    _delay_ms(2);
    
    set_addr_ddram(0);
    for (i = 0; top[i] != '\0'; i++) send_char(top[i]);
    set_addr_ddram(0x40);
    for (i = 0; bottom[i] != '\0'; i++) send_char(bottom[i]);
    #endif
}

void send_char (unsigned char _char)
{
    // loop until ready
    busy_loop();
    
    // output character
    DATA_PORT = _char;
    
    // data write mode
    CTRL_PORT |= _BV(RS);
    CTRL_PORT &= ~_BV(R_W);
    
    // clock pulse
    clk();
}

void send_cmd (uint8_t cmd)
{
    // loop until ready
    busy_loop();
    
    // output command
    DATA_PORT = cmd;
    
    // command write mode
    CTRL_PORT &= ~_BV(RS);
    CTRL_PORT &= ~_BV(R_W);
    
    // clock pulse
    clk();
    
    DATA_PORT = 0;
}

void set_addr_cgram (uint8_t addr)
{
    send_cmd(addr + 0x40);
}

void set_addr_ddram (uint8_t addr)
{
    send_cmd(addr + 0x80);
}

#endif