Author Marek Pikulski 12.03.2023.
benchmarek[at]outlook[dot]com
https://github.com/benchmarex

This project downloads data solar production and operating parameters of the photovoltaic system from the
SofarSolar inverter via local connection MODBUS TCP/IP.
The data is sent to the local mysql server.

Projekt jest rozszeżenie poprzedniego mojego projektu który przeładowywał dane z serwera API Solarman. 


Połaczenie pomiędzy RS485 a Wifi wykonane zostało za pomocą Elfin EW11 który został skonfigurowany jako sewer Modbus i udostępniony w sieci lokalnej.
Rs 485 zostało podłączone pod jeden z  portów falownika Sofar Solar KTL-X 11. 9600,8,1,n tak należy ustawić serwer w EW11  do komunikacji z tym Sofarem. 

