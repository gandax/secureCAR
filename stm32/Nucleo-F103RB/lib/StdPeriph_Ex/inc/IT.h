#include "stm32f10x.h"


void TIM1_UP_IRQHandler ( void );

void TIM2_IRQHandler ( void );

void TIM3_IRQHandler ( void );

void TIM4_IRQHandler ( void );

void Timer_Active_IT(TIM_TypeDef *Timer, u8 Priority, void (*IT_function) (void));


