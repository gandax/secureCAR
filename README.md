# secureCAR



Imagine a car that can detect its own failures and make decisions to protect its integrity. The goal of the secureCAR project is to provide a fully equipped car that can handle interactions with its environment.

Failures can occur into the system and affect the ability of the car to correctly answer orders from the user. Secure Car is able to detect various types of failures and notify the user. 

To do so, secureCar uses an odometric model and in this way, it is able to know its position and its attitude from a starting point at all times.


## Architecture

<img src="/Images/main_archi.png">

This project is implemented on a STM32 and on a RaspberryPi and they are communicating through a CAN bus.
That is why there is a directory for each board.

***

Concerning the Model_Simulation directory, it contains all the files to simulate the model and to display its results.



