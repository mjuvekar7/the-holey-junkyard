/*
 * common frame buffer code
 * other common utils
 */
#ifndef _COMMON_H
#define _COMMON_H

#define FULL_X_SIZE 8
#define DISP_X_SIZE 5
#define FULL_Y_SIZE 8
#define DISP_Y_SIZE 5
#define F_CPU 1000000L

#include <avr/io.h>

extern uint8_t full_buf[][FULL_Y_SIZE];
extern uint8_t disp_buf[][DISP_Y_SIZE];

#endif

