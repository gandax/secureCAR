#include "IT.h"
#include "stm32f10x.h"

void (* pFnc2) (void) ; 
void (* pFnc3) (void) ; 
void (* pFnc4) (void) ; 
void (* pFnc1) (void) ;


void TIM2_IRQHandler ( void )
{
	if (pFnc2 != 0)
		(*pFnc2) (); /* appel indirect de la fonction */
	TIM2->SR &= 0xFE;
}



void Timer_Active_IT(TIM_TypeDef *Timer, u8 Priority, void (*IT_function) (void))
{
	
  if (Timer == TIM2) {
		NVIC->ISER[0] |= (0x01 << 28);
		NVIC->IP[28] = (Priority<<4);
		TIM2->DIER |= TIM_DIER_UIE;
		pFnc2 = IT_function;
	}

}
