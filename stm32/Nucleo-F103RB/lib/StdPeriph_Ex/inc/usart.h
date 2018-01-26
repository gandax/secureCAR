#ifndef USART_H
#define USART_H


#include <stdlib.h>
#include "stm32f10x.h" 
#include "stm32f10x_usart.h"
#include "API_CAN.h"

void USART1_Init(void);
void USART1_IRQHandler(void);


extern short g_measured_angle;


#endif
 	