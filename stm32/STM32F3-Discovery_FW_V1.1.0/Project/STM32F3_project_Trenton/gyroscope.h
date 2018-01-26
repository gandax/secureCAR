
#ifndef _GYROSCOPE_H
#define _GYROSCOPE_H


#include "stm32f30x.h"
#include "stm32f3_discovery.h"
#include <stdio.h>
#include "stm32f3_discovery_l3gd20.h"


#define ABS(x)         (x < 0) ? (-x) : x

#define L3G_Sensitivity_250dps     (float)   114.285f         /*!< gyroscope sensitivity with 250 dps full scale [LSB/dps] */
#define L3G_Sensitivity_500dps     (float)    57.1429f        /*!< gyroscope sensitivity with 500 dps full scale [LSB/dps] */
#define L3G_Sensitivity_2000dps    (float)    14.285f	      /*!< gyroscope sensitivity with 2000 dps full scale [LSB/dps] */
#define PI                         (float)     3.14159265f



void GyroConfig(void);
void GyroReadAngRate (float* pfData);

#endif // _GYROSCOPE_H