/**
  ******************************************************************************
  * @file    System_Time.c 
  * @author  Thomas Gandou
  * @version V1.1.1
  * @date    20-September-2012
  * @brief   Systick functions used for timing based on MCD Application Team work
	* @modif   Thomas Gandou
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; COPYRIGHT 2012 STMicroelectronics</center></h2>
  *
  ******************************************************************************
  */


/* Includes ------------------------------------------------------------------*/
#include "System_Time.h"

/*----------------------------------------------------------------------------*/

uint64_t time_millis;
RCC_ClocksTypeDef RCC_Clocks;


float  Buffer[3] = {0.0f};
static float angle = 0.0f;
short old_angle = -1;


/*
We use an union to convert our angle that is in short to a char*
letting us transmit it through the USART bus                       */
union {
	short num_angle;
	char byte_angle[2];
}u_angle;



/**
  * @brief  Initialization of the system time
  * @param  None
  * @retval None
  */
void SystemTime_Init(void){
	/* SysTick end of count event each 1ms */
  RCC_GetClocksFreq(&RCC_Clocks);
  SysTick_Config(RCC_Clocks.HCLK_Frequency / 1000);
	time_millis = 0;
}

/**
  * @brief  Function called every millisecond
  * @param  None
  * @retval None
  */
void SysTick_Callback(void){
	
	char numToSend[5];
	float inc = 0;
	time_millis++;
	
	GyroReadAngRate(Buffer);
	/* GyroReadAngRate return an angular speed. We are computing the speed every ms
	So as the speed is in °.s^-1, if we ultiply by our sample time in s we obtain ° */
	inc = Buffer[2]*0.001f; 
	
	/*We filter the small increments that are related to the offset of the measure 
	  to avoid angle to increase indefinitely */
	if ( inc > 0.001 || inc < -0.001){
		angle = (float)fmod(angle + inc,360);
		u_angle.num_angle = (short)angle;
		}

	//Every 50ms if the angle changed we send it through the USART bus 
	if (time_millis %50 == 0 && u_angle.num_angle != old_angle ){
		USART1_write(u_angle.byte_angle,2);
		old_angle = u_angle.num_angle;
	}
	
}