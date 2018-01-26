
#ifndef _SYSTEM_TIME_H
#define _SYSTEM_TIME_H


/* Includes ------------------------------------------------------------------*/
#include "stm32f30x.h"
#include "USART.h"
#include "gyroscope.h"
#include <tgmath.h>

void SystemTime_Init(void);
void SysTick_Callback(void);

#endif // _SYSTEM_TIME_H