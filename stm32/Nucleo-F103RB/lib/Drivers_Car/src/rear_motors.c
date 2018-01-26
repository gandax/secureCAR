/**
 * @file    rear_motors.c
 * @author  Curtis Team
 * @brief   Functions to handle rear motors
 */
 
 /* Includes ------------------------------------------------------------------*/
#include <math.h>
#include "rear_motors.h"
#include "stm32f10x_conf.h"
#include "motors.h"
#include "position_sensors.h"
#include "hall_sensors.h"
#include "system_time.h"
#include "data_interface.h"
#include "modules_definitions.h"
#include "API_CAN.h"
#include "math.h"

/* Private typedef -----------------------------------------------------------*/
/* Private define ------------------------------------------------------------*/
/* Private macro -------------------------------------------------------------*/
/* Public variables ----------------------------------------------------------*/

/**
 * @brief   Last measured car position on left wheel
*/
volatile static float car_position_L = 0;

/* @brief   Last measured car position on right wheel
*/
volatile static float car_position_R = 0;

/**
 * @brief   Expected speed on the wheel
*/
volatile float speed_cmd = 0.;

/**
 * @brief   Speed expected on the left wheel
*/
volatile static float speed_L = 0;

/**
 * @brief   Speed expected on the right wheel
*/
volatile static float speed_R = 0;

/**
 * @brief   Counter to determine command refreshing time
*/
uint32_t RearMotors_remainingTimeInCommandPeriod = MOTORS_COMMAND_TIME_BETWEEN_TWO_UPDATES;

/**
 * @brief   Formal output of the system
*/
static float out_prec = 0;



/* Private function prototypes -----------------------------------------------*/
int16_t car_model(float in);
float PI_Controller (float in);
float PI_Current_Controller (float in_PI);
float ComputeMotorCommand_L(int16_t speed_cmd, int16_t current, Sensor_Enum sensor_id);
void RearMotor_control(int16_t speed_cmd, Motors_Enum motor_id);

/* Public functions ----------------------------------------------------------*/
/**
 * @brief   Initializes rear motors
 * @retval  None
*/
void RearMotors_QuickInit(void) {
    Motor_QuickInit(REAR_MOTOR_L);
    Motor_QuickInit(REAR_MOTOR_R);
}

/**
 * @brief   Allows rear motors to spin
 * @retval  None
*/
void RearMotors_Enable(void) {
    Motor_Enable(REAR_MOTOR_L);
    Motor_Enable(REAR_MOTOR_R);
}

/**
 * @brief   Forbides rear motors to spin
 * @retval  None
*/
void RearMotors_Disable(void) {
    Motor_Disable(REAR_MOTOR_L);
    Motor_Disable(REAR_MOTOR_R);
}

/**
 * @brief   Callback associated to rear motors whose aim is to set the adequate command on the motor 
 * @retval	None
*/
void RearMotors_Callback(void) {
	
  
  RearMotor_control(speed_cmd, REAR_MOTOR_L);
  RearMotor_control(speed_cmd, REAR_MOTOR_R);		

}

/**
 * @brief   Sets speed which must be regulated. 
 * @param   speed Expected speed (in cm/s)
 * @retval	None
*/
void RearMotors_setSpeed(int16_t speed) {
    speed_cmd = speed; 
}
/* Private functions ---------------------------------------------------------*/
/**
 * @brief   [for debug only] Calculates system answer according to its input.
 * @param   in The input of the system.
 * @retval	System output.
*/
int16_t car_model(float in) {
    
    float K_model = 250.0;   // speed in cm/s
    float T_model = 0.1;
    int16_t out;
    out = (K_model * (float)(in-MOTORS_PWM_ZERO) - T_model * out_prec);
    out_prec = (float)out;
    return out;
}


//Current loop regulation
//Proportional integral regulator with Anti-Windup

float  PI_Current_Controller(float in_PI){
	
	//Variable for the anti-windup
	static float output_no_offset = 0. ;
	static float output_offseted = 0; 
	float AW_f = 0. /*Action de l'anti_windup */, K_AW = 0.1;  //Coefficient de l'Anti-windup
	
	//Regulator's coefficients
	float Kp = 1. , Ki = 0.1 ;
		
	//We recover the previous state
	float previous_state_no_offset = output_no_offset ;
	float previous_state_offseted  = output_offseted;
	
	//Anti_windup
		if (previous_state_no_offset > MAX_SPEED_FOR)
		 AW_f =  K_AW*(previous_state_no_offset  - MAX_SPEED_FOR); 
	else if (previous_state_no_offset < MAX_SPEED_BAC)
		 AW_f = K_AW*(previous_state_no_offset  - MAX_SPEED_BAC);
	else 
		 AW_f = 0.0;        


	//x(t) = Kp * e(t) + Ki * x(t-1) ;
	previous_state_no_offset = Kp * in_PI /*+ Ki * previous_state_no_offset + AW_f */;
	
	//Saturateur
	if (previous_state_no_offset > MAX_SPEED_FOR)
		output_offseted = MAX_SPEED_FOR;
	else if (previous_state_no_offset < MAX_SPEED_BAC)
		output_offseted = MAX_SPEED_BAC;
	else
		output_offseted = output_no_offset ;
	
	previous_state_offseted = output_offseted;
	return output_offseted;

}



/**
 * @brief   Computes the next iteration Motor Duty-Cycle command (right wheel)
 * @param   speed_cmd The speed input command for the control loop (cm/s)
 * @param   current Current in the motor (mA)
 * @param   speed The car speed (cm/s)
 * @retval	The duty-cycle command for the motor
*/
float ComputeMotorCommand (int16_t speed_cmd, int16_t current, Sensor_Enum sensor_id){
    
  float output_speed;         //out speed;
  float in_PI;
  float car_position_measured;
	int current_ok = 0;

	if (sensor_id == SENSOR_L){
		car_position_L += speed_cmd * 0.01 ;  //Here we multiply the speed cmd by the sampling time to obtain the total distance traveled by the left wheel
		car_position_measured = PositionSensor_get(POSITION_CM,sensor_id);
		in_PI = (float)(car_position_L - car_position_measured);
	}
	
	else if (sensor_id == SENSOR_R){
		car_position_R += speed_cmd * 0.01 ;  //Here we multiply the speed cmd by the sampling time to obtain the total distance traveled by the left wheel
		car_position_measured = PositionSensor_get(POSITION_CM,sensor_id);
		in_PI = (float)(car_position_R - car_position_measured);
	}
	
	
	output_speed = PI_Controller(in_PI);
    
    return output_speed;
}


/**
 * @brief   Applies a PI controller to the input
 * @param   in PI controller input
 * @return  PI controller output
*/
float PI_Controller (float in)
{
	static const float Kp = 0.03;
	static float out_PI_Position ;           // buffer previous in & out

	float PI_output_f;      

	//Calcul of the error for the current regulation loop
	out_PI_Position = Kp*in ;
  //out_PI_Position -=current ;
	
	//We put this at the input of the current loop
	//PI_output_f = PI_Current_Controller(out_PI_Position);
	
		//Saturateur en vitesse
	if (out_PI_Position > MAX_SPEED_FOR)
		out_PI_Position = MAX_SPEED_FOR;
	else if (out_PI_Position < MAX_SPEED_BAC)
		out_PI_Position = MAX_SPEED_BAC;
	

	PI_output_f = out_PI_Position ;
	
	return PI_output_f;
}


/**
 * @brief   The core of the control loop for rear motor left
 * @param   speed_cmd The speed command 
 * @retval	None
*/

//Trenton modification : The loop is now in position
void RearMotor_control(int16_t speed_cmd, Motors_Enum motor_id){
		int16_t current;
	
		if (motor_id == REAR_MOTOR_L){
			Motor_setSpeed(motor_id, speed_L);
			current = Motor_getCurrent(REAR_MOTOR_L);
			if (fabs((float)current) < MAX_CURRENT)
				speed_L = ComputeMotorCommand(speed_cmd, current,SENSOR_L);
			else
				RearMotors_Disable();
		}
		else if (motor_id == REAR_MOTOR_R){
			Motor_setSpeed(motor_id, speed_R);
			current = Motor_getCurrent(REAR_MOTOR_R);
			if (fabs((float)current) < MAX_CURRENT)
				speed_R = ComputeMotorCommand(speed_cmd, current,SENSOR_R);
			else
				RearMotors_Disable();
		}
}





