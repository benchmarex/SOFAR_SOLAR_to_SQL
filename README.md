Author Marek Pikulski 12.03.2023.
benchmarek[at]outlook[dot]com
https://github.com/benchmarex


EN is above

**Pl**

Ten projekt pobiera dane produkcji solarnej oraz parametry z nią związaną z fotowoltaicznego systemu postanowionego na inwerterze Sofar Solar poprzez lokalne połaczenie MODBUS TCP/IP. Dane są przesyłane na lokalny serwer my SQL. 

Projekt jest rozszeżenie poprzedniego mojego projektu który przeładowywał dane z serwera API Solarman. 
Znajduje się tutaj https://github.com/benchmarex/API_SOLARMAN_to_SQL_to_Grafana

Tamten projekt jescze pracuje,ale po przetestowaniu tego zostanie wyłączony. Ten projekt całkowicie przejmie rolę dostarczania danych do serwera SQL bez udziału serwera Solarman. 


Połaczenie pomiędzy RS485 a Wifi wykonane zostało za pomocą Elfin EW11 który został skonfigurowany jako sewer Modbus i udostępniony w sieci lokalnej.
RS485 zostało podłączone pod jeden z  portów RS485 falownika Sofar Solar KTL-X 11. 9600,8,1,n tak należy ustawić serwer w EW11  do komunikacji z tym Sofarem. W katalogu z projektem znajduje się mapa MODBUS tego Sofara. 



**En**

This project downloads data solar production and operating parameters of the photovoltaic system from the
SofarSolar inverter via local connection MODBUS TCP/IP.
The data is sent to the local mysql server.

The project is an extension of my previous project that reloaded data from the Solarman API server.
Located here https://github.com/benchmarex/API_SOLARMAN_to_SQL_to_Grafana

That project is still working, but after testing this it will be disabled. This project will completely take over the role of delivering data to the SQL server without involving the Solarman server.


The connection between RS485 to Wifi was made using Elfin EW11 which was configured as a Modbus server and made available in the local network.
RS485 has been connected to one of the RS485 ports of the Sofar Solar KTL-X 11 inverter. 9600,8,1,n This is how the server in EW11 should be set to communicate with this Sofar. There is a MODBUS map of this Sofar in the project directory.

