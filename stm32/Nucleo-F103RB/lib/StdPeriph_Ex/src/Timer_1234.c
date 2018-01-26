/**
 * @file    Timer1234.c
 * @author  Corentin Egreteau
 * @brief   Init the timer 1, 2, 3 and 4
 */

#include "stm32f10x.h"
#include "Timer_1234.h"
#include "clock.h"


float Timer_1234_Init (TIM_TypeDef* Num, float duree_us) //Initialisation du Timer
{
	float freq_desir;
	int res;
	float freq_return;
	
	if (Num == TIM1) {
		RCC -> APB2ENR |= RCC_APB2ENR_TIM1EN;
		TIM1->CR1 |= TIM_CR1_CEN;
	}
	else if (Num == TIM2) {
		RCC -> APB1ENR |= RCC_APB1ENR_TIM2EN;
		TIM2->CR1 |= TIM_CR1_CEN;
	}
	else if (Num == TIM3) {
		RCC -> APB1ENR |= RCC_APB1ENR_TIM3EN;
		TIM3->CR1 |= TIM_CR1_CEN;
	}
	else if (Num == TIM4) {
		RCC -> APB1ENR |= RCC_APB1ENR_TIM4EN;
		TIM4->CR1 |= TIM_CR1_CEN;
	}
	
	freq_desir = 1/duree_us*1000000 ;
	res = CLOCK_GetTIMCLK(Num)/freq_desir;
	
	Num->PSC = (res>>0x10);
	Num->ARR = res/(Num->PSC + 1);
	
	freq_return = CLOCK_GetTIMCLK(Num) / ((Num->PSC + 1) * Num->ARR);
 
return freq_return;	
}










