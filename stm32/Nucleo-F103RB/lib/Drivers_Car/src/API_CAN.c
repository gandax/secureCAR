/**
 * @file    API_CAN.c
 * @author  Team TRENTON
 * @brief   middleware for the CAN communication
 */

#include "API_CAN.h"


unsigned char can_trame[8];	

int id;															   //id of the trame to be send
data_commands data_received_raspi ;    //Variable globale des données recues de la raspi


/** 
* @brief  Initializes the CAN communication
* @retval none  
*/
void can_init(int id){
	CAN_setup ();                                   /* setup CAN Controller     */
	CAN_wrFilter (id, STANDARD_FORMAT);             /* Enable reception of msgs */
	CAN_start ();                                   /* start CAN Controller   */
	CAN_waitReady ();                               /* wait til tx mbx is empty */	
}


/** 
* @brief  Initializes the cyclic transaction of the CAN communication
* @retval none  
*/
void can_init_cyclic_transaction(int period){
	//Initalisation du timer 2 et assignation de la primitive d'envoi des données
	Timer_1234_Init(TIM2,50000);
	Timer_Active_IT(TIM2,0,CAN_send);
}

/** 
* @brief  Merges all the data that have to be send in the can trame
* @parameter data : data from the odometers and the potentiometer
* @parameter gyro_data : data from the gyroscope
* @parameter can_trame : the trame that will be sent
* @retval none  
*/
void merge_data1_STM(data_sensors data, data_orientation gyro_data, unsigned char* can_trame){
	

	can_trame[0] = data.left_odometer.bytes_left_odometer[0] ;
	can_trame[1] = data.left_odometer.bytes_left_odometer[1] ;
	can_trame[2] = data.right_odometer.bytes_right_odometer[0] ;
	can_trame[3] = data.right_odometer.bytes_right_odometer[1] ;
	can_trame[4] = data.potentiometer.bytes_potentiometer[0] ;
	can_trame[5] = data.potentiometer.bytes_potentiometer[1] ;
	can_trame[6] = gyro_data.gyro_angle.byte_measured_angle[0];
	can_trame[7] = gyro_data.gyro_angle.byte_measured_angle[1];
}


/** 
* @brief  Unwrap the data received from the Raspberry PI
* @retval none  
*/
void CAN_receive_STM(){
	
	if (CAN_RxRdy){
		CAN_RxRdy = 0;
		data_received_raspi.motor_command.bytes_motor_command = CAN_RxMsg.data[0] ;
		data_received_raspi.steering_wheel_command.bytes_steering_wheel_command = CAN_RxMsg.data[1] ;
		data_received_raspi.motor_speed.bytes_motor_speed = CAN_RxMsg.data[2] ;
	}
}



//Il faut une fonction void void car on la passe dans le handler
//Cette fonction va envoyer les données issues des capteurs de la voiture
/** 
* @brief  Sending primitive
* @retval none  
*/
void CAN_send(void){
	
	int i = 0,i2 = 0, message_size = 0 ;
	
	data_sensors sensor_data_sent;
	data_orientation gyro_data ;
	
	//On construit la trame
	sensor_data_sent = fill_structure_CAN1();
	gyro_data = fill_structure_CAN2();
	merge_data1_STM(sensor_data_sent, gyro_data, can_trame);
	
	CAN_TxMsg.len = 8;	
	CAN_TxMsg.id = 10;
	CAN_TxMsg.format = STANDARD_FORMAT;
	CAN_TxMsg.type = DATA_FRAME;
	message_size = 8 ; 
	
		
	//On initalise les données de la trame
	for (i = 0 ;i<8;i++){
			CAN_TxMsg.data[i] = 0 ;
	}

	if (CAN_TxRdy) {                              /* tx msg on CAN Ctrl       */
		CAN_TxRdy = 0;
		for(i2=0;i2<message_size;i2++){
			CAN_TxMsg.data[i2] = can_trame[i2];
		}
      
		CAN_wrMsg (&CAN_TxMsg);                     /* transmit message         */
    }
	
}

/** 
* @brief  fill the structure that will be put in the CAN trame
* @retval data_sensors : a structure with the value retrieved from the sensors  
*/
data_sensors fill_structure_CAN1(){
	
	data_sensors data ;
	data.left_odometer.num_left_odometer = HallSensor_compute_angle(SENSOR_L);
	data.right_odometer.num_right_odometer = HallSensor_compute_angle(SENSOR_R);
	data.potentiometer.num_potentiometer = Direction_get();
	
	return data;
}

/** 
* @brief  fill the structure that will be put in the CAN trame
* @retval data_orientation : a structure with the value retrieved from the USART  
*/
data_orientation fill_structure_CAN2(){
	
	data_orientation gyro_data ;
	gyro_data.gyro_angle.num_measured_angle = g_measured_angle;
	
	return gyro_data;
}
