#ifndef API_CAN_H
#define API_CAN_H

#include <stdarg.h>
#include <stdlib.h>
#include <string.h>
#include "stm32f10x.h"       /* STM32F10x Definitions    */
#include <stdio.h>
#include <stdarg.h>
#include <math.h>
#include "CAN.h"
#include "usart.h"
#include "Timer_1234.h"   
#include "IT.h"
#include "hall_sensors.h"
#include "speed_sensors.h"
#include "direction.h"
#include "data_interface.h"



/*----------------------------------------------------------------------------------------------------------------------------------------------
//Definition of the datas exchanged in the CAN communication
//We use union types to convert short in char[8] to permit the integration of the onformation in
//a frame
------------------------------------------------------------------------------------------------------------------------------------------------*/

//Definiton of the data from the sensors
typedef struct data_sensors 	
	{		
		union {
			short num_left_odometer;  
			unsigned char  bytes_left_odometer[2];
		}left_odometer;
		
		union {
			short num_right_odometer;
			unsigned char  bytes_right_odometer[2];
		}right_odometer;
		
		union {
			short num_potentiometer;
			unsigned char  bytes_potentiometer[2];
		}potentiometer;
		
	}data_sensors;

//Defintion of the command data
typedef struct data_commands 	
	{
		
		union {
			uint8_t num_motor_command;
			unsigned char  bytes_motor_command;
		}motor_command;
		
			union {
			uint8_t num_motor_speed;
			unsigned char  bytes_motor_speed;
		}motor_speed;
		
		union {
			uint8_t num_steering_wheel_command;
			unsigned char  bytes_steering_wheel_command;
		}steering_wheel_command;
		
	}data_commands;
	
	typedef struct data_orientation{
		union 
		{
			short num_measured_angle;
			char byte_measured_angle[2];
	}gyro_angle;
		
}data_orientation;


	//FOnctions relatives au can
	void can_init (int id);
	void can_init_cyclic_transaction(int period);
	void CAN_send(void);
	void merge_data1_STM(data_sensors data, data_orientation gyro_data, unsigned char* can_trame);
	void merge_data_test(data_commands data,unsigned char* can_trame);
	void CAN_receive_STM(void);
	data_sensors fill_structure_CAN1(void);
	data_orientation fill_structure_CAN2();
			
	extern unsigned char can_trame[8];													//data of the trame to be send
	extern int id;																			//id of the trame to be send 
	extern data_commands data_received_raspi ;
	
#endif
 	