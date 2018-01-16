# STM32

## CAN

Different data are send through the CAN bus, they are detailled in the following tab:

|Name                |Size|Period |Source|Destination|
|--------------------|----|-------|------|-----------|
|pose steering wheel |1   |50ms   |STM32|Raspi      |
|pose wheels Left    |2   |50ms   |STM32|Raspi      |
|pose wheels Right   |2   |50ms   |STM32|Raspi      |
|motors order        |1   |50ms   |Raspi |Nucleo     |
|steering wheel order|1   |50ms   |Raspi |Nucleo     |

## USART
