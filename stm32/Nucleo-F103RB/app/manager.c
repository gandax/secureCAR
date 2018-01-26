/**
 * @file    nucleo_functionnalities_manager.c
 * @author  Curtis Team
 * @brief   for the initialization of all the structures and recurrent operations
 * @modif   Team Trenton
 */


/* Includes ------------------------------------------------------------------*/
#include <stdint.h>
#include "system_time.h"
#include "position_sensors.h"
#include "hall_sensors.h"
#include "speed_sensors.h"
#include "motors.h"
#include "front_motor.h"
#include "rear_motors.h"
#include "us_sensors.h"
#include "direction.h"
#include "API_CAN.h"
#include "data_interface.h"



/* Private typedef -----------------------------------------------------------*/
/* Private define ------------------------------------------------------------*/
/**
 * @brief   Manager refresh time (in ms)
*/
#define MANAGER_TIME_BETWEEN_TWO_UPDATES 10 //ms

/* Private macro -------------------------------------------------------------*/
/* Public variables ----------------------------------------------------------*/



/* Private variables ---------------------------------------------------------*/
/**
 * @brief   Speed of the motors
*/
float motor_speed = 0.0;
uint16_t speedD;
uint16_t speedG;

/* Private function prototypes -----------------------------------------------*/
/* Public functions ----------------------------------------------------------*/



/** 
* @brief  Initializes all the sensors / actuators
* @retval none  
*/

void Manager_Init(void) {
    
		can_init(20); //On reçoit les messages de id = 20
		can_init_cyclic_transaction(50000);
	
    FrontMotor_QuickInit();
    RearMotors_QuickInit();
    
    RearMotors_Enable();
    
    PositionSensor_QuickInit(SENSOR_L);
    PositionSensor_QuickInit(SENSOR_R);
       
		SpeedSensor_QuickInit(SENSOR_L);
    SpeedSensor_QuickInit(SENSOR_R);

	 Direction_QuickInit();
   System_Time_QuickInit();
}

/**
 * @brief   Callback associated to the nucleo functionnalities manager whose aim is to update the value send in the CAN bus
 * @retval	None
*/
void Manager_Callback(void) {
	
	/*Traitement des commandes pour le moteur avant------------------------------------------------------------*/
	if (data_received_raspi.steering_wheel_command.num_steering_wheel_command !=0){
		//Formule pour convertir les données reçues depuis le bus CAN
		angle_cmd = 109 + (158-109)*(data_received_raspi.steering_wheel_command.num_steering_wheel_command-10)/10;
	}
	else
		Motor_Disable(FRONT_MOTOR);

	//On met à jour la commande de vitesse (mise à l'échelle en multipliant par 0.7
	//si on est pas en état de marche, on actualise quand même la vitesse
	
	/*Traitement des commandes pour les moteurs arrières---------------------------------------------------------*/
	if (data_received_raspi.motor_command.num_motor_command == 2){
		speed_cmd = (float)data_received_raspi.motor_speed.num_motor_speed * 0.7;
	}
	else if (data_received_raspi.motor_command.num_motor_command == 0){
		speed_cmd = (float)data_received_raspi.motor_speed.num_motor_speed;
	}
	
	else if (data_received_raspi.motor_command.num_motor_command == 1){
		//Si la commande indique d'aller en arrière alors on met la vitesse opposée
		speed_cmd = -(float)data_received_raspi.motor_speed.num_motor_speed * 0.7;
	 }           
} 
	
