/**
 * @file    front_motor.h
 * @author  Curtis Team
 * @brief   Headers of functions to handle front motor  
 */
 
/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef _FRONT_MOTOR_H
#define _FRONT_MOTOR_H

/* Includes ------------------------------------------------------------------*/
#include <stdint.h>
#include <stddef.h>
#include "stm32f10x.h"
#include "common_constants.h"

/* Exported functions ------------------------------------------------------- */
void FrontMotor_QuickInit(void);
void FrontMotor_Callback(void);
float ComputeMotorCommand_F (int16_t angle_cmd, int16_t car_angle);
void FrontMotor_control(int16_t angle_cmd);
float FrontMotor_P_regulator(int32_t in_P);

extern volatile int16_t angle_cmd;

#endif // _FRONT_MOTOR_H
