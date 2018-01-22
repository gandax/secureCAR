/**
 * @file    front_motor.c
 * @author  Curtis Team
 * @brief   Functions to handle front motor  
 * @modif   Team Trenton
 */
 
/* Includes ------------------------------------------------------------------*/
#include <stdlib.h>
#include "front_motor.h"
#include "modules_definitions.h"
#include "motors.h"
#include "exti.h"
#include "modules_definitions.h"
#include "direction.h"
#include "API_CAN.h"

/* Private typedef -----------------------------------------------------------*/
/* Private define ------------------------------------------------------------*/
/* Private macro -------------------------------------------------------------*/
/**
 * @brief   Front motor speed when turning left
*/
#define FRONT_MOTOR_SPEED_L               0.7

/**
 * @brief   Front motor speed when turning right
*/
#define FRONT_MOTOR_SPEED_R               -FRONT_MOTOR_SPEED_L

/* Public variables ----------------------------------------------------------*/
volatile int16_t angle_cmd = 133;
volatile static float motor_speed_F = 0;
volatile static int16_t car_angle = 0;
int low_error;


/* Public functions ----------------------------------------------------------*/
/**
 * @brief   Initialisation of the front motor
 * @retval  None
*/
void FrontMotor_QuickInit(void) {
    Motor_QuickInit(FRONT_MOTOR);
}

/**
 * @brief   Recurrent operations on the front motor
 * @retval  None
*/
void FrontMotor_Callback(void){
	FrontMotor_control(angle_cmd); 
	//angle cmd étant la variable globale contenant l'angle de commande reçu par le can	 
}


/**
 * @brief   Second function of the front motor regulation
 * @retval  the speed that the front motor has to have
*/
float ComputeMotorCommand_F (int16_t angle_cmd, int16_t car_angle){
	
	float speed;         //out duty cycle;
	volatile int32_t in_P;
 
	in_P = angle_cmd - car_angle; //Calcul de l'erreur qu'on envoie ensuite dans le correcteur P
	if (abs(in_P)<3){low_error = 1;}
	else {low_error = 0;}
	/*La variable globale low_error sert à ne pas rentrer continuellement dans la régulation car
	  la valeur retournée par le potar n'est JAMAIS la même,on aura donc des oscillations en continu */
	
	speed = FrontMotor_P_regulator(in_P) ; //On applique le correcteur P
		
	return speed;
}


/**
 * @brief   Main function of the front motor regulation
 * @retval  none
*/
void FrontMotor_control(int16_t angle_cmd){
    static float motor_speed_F = 0.0;
		int16_t front_motor_current = Motor_getCurrent(FRONT_MOTOR);
		car_angle = Direction_get();     
    motor_speed_F = ComputeMotorCommand_F(angle_cmd, car_angle); 
		
		//Si l'erreur est suffisament petite alors on considère que l'angle est le bon 
		if (low_error == 1){
			Motor_Disable(FRONT_MOTOR);
		}
		else {
			Motor_setSpeed(FRONT_MOTOR, motor_speed_F);
			Motor_Enable(FRONT_MOTOR);
		}
}

/**
 * @brief   Last function of the front motor regulation
 * @retval  the output of the P regulatoir
*/
float FrontMotor_P_regulator(int32_t in_P){
	
	float Kp = 5.3;
	float command = 0.0;
	
	 command = (float)in_P * Kp / 100.0;
	
	//Saturateur
	if (command > 1.0){
		command = 1.0 ;
	}
	
	//On évite d'envoyer des commandes trop faibles
	else if (command > 0 && command < 0.15){
		command = 0.15;
	}		
	else if (command < 0 && command > -0.15){
		command = -0.15;
	}		
	else if (command < -1.0){
		command = -1.0;
	}
	return command;
}
