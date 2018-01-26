/**
  ******************************************************************************
  * @file    main.c 
  * @author  Thomas Gandou
  * @version V1.1.1
  * @date    20-September-2012
  * @brief   Main file based on MCD Application Team work
	* @modif   Thomas Gandou
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; COPYRIGHT 2012 STMicroelectronics</center></h2>
  *
  ******************************************************************************
  */


/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "usart.h"

/**
  * @brief  Main program.
  * @param  None 
  * @retval None
  */
int main(void)
{  
	Quick_init();
  while (1){}
}



/**
  * @brief  Init functions
  * @param  None 
  * @retval None
  */
void Quick_init(void){		
	USART1_Init();
	GyroConfig();
	SystemTime_Init();
}


/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
