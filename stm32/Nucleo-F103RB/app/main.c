/**
  ******************************************************************************
  * @file    gyroscope.c 
  * @author  Trenton Team
  * @brief   Main file
  ******************************************************************************
  */



/*Includes-----------------------------------------------------------------------*/
#include <stm32f10x.h>
#include "manager.h"
#include "usart.h"



int main(void) {

	Manager_Init();
	USART1_Init();
	while (1){}
}

