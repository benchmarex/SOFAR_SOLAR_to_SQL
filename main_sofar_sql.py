"""
Author Marek Pikulski 12.03.2023. benchmarek[at]outlook[dot]com https://github.com/benchmarex

This project downloads data solar production and operating parameters of the photovoltaic system from the SofarSolar
inverter via local connection MODBUS TCP/IP. The data is sent to the local mysql server.
The script is written in Python and invoked using the cron mechanism at intervals of __ minutes.
"""


from pyModbusTCP.client import ModbusClient
from pythonping import ping
import json
import sys
import datetime


def data_converter(param):  # funkcja  sprawdzajaca i przeliczająca czy dodatnia czy ujemna

    if param > 0x8000:  # jest na minusie wartości
       return param - 0x10000

    return param

def get_inverter_data_modbus(SERVER_MODBUS_HOST, SERVER_MODBUS_PORT):
    print("Reading modbus...\n")
    c = ModbusClient(host=SERVER_MODBUS_HOST, port=SERVER_MODBUS_PORT, unit_id=1, timeout=5, auto_open=True,
                     auto_close=True)
    regs=c.read_holding_registers(0, 48)

    if regs:
        return regs
    else:
        print("Modbus read error")
    sys.exit()

def get_time():
    # get system time

    now = datetime.datetime.now()
    pm_solartime = now.strftime("%Y-%m-%d %H:%M:%S")
    return (pm_solartime)









###########___start program___#################



with open('C:\\Users\\Marek\\PycharmProjects\\pythonProject\\config12.json') as jsonFile:
    jsonObject = json.load(jsonFile)

SERVER_MODBUS_HOST = jsonObject['SERVER_MODBUS_HOST']
SERVER_MODBUS_PORT = jsonObject['SERVER_MODBUS_PORT']

resp = str(ping(SERVER_MODBUS_HOST))
resp = resp.find("Request timed out")

if resp == -1:
        print(SERVER_MODBUS_HOST, 'Host is up')

else:
        print(SERVER_MODBUS_HOST, 'Host is unreachable')
        sys.exit()

response_modbus = get_inverter_data_modbus(SERVER_MODBUS_HOST, SERVER_MODBUS_PORT)
print(response_modbus, "\n")




###############___AC GRID___##############
AC_V1 = response_modbus[0x0f]/10
AC_V2 = response_modbus[0x11]/10
AC_V3 = response_modbus[0x13]/10

AC_V1_CURRENT = response_modbus[0x10]/100
AC_V2_CURRENT = response_modbus[0x12]/100
AC_V3_CURRENT = response_modbus[0x14]/100

AC_V1_3_ACTIVE_POWER = response_modbus[0x0c]

AC_V1_3_REACTIVE_POWER = data_converter(response_modbus[0x0d])

AC_V1_3_FREQ = response_modbus[14]/100

AC_Today_Production = response_modbus[0x019]/100
AC_Today_Generation_Time = response_modbus[0x01A]

print(f"Voltage AC1 = {AC_V1} V, Current AC1 = {AC_V1_CURRENT} A")
print(f"Voltage AC2 = {AC_V2} V, Current AC2 = {AC_V2_CURRENT} A")
print(f"Voltage AC3 = {AC_V3} V, Current AC3 = {AC_V3_CURRENT} A")
print("\n")
print(f"Active Power AC1_3 = {AC_V1_3_ACTIVE_POWER}W")
print(f"Reactive Power AC1_3 = {AC_V1_3_REACTIVE_POWER}VAR")
print("\n")

print(f"AC_V1_3_Frequency = {AC_V1_3_FREQ}Hz")
print("\n")

print(f"Today_Production = {AC_Today_Production}kWh")
print("\n")
print(f"AC_Today_Generation_Time = {AC_Today_Generation_Time}min")
print("\n")
###############___AC GRID___#####################

###############___Temperature___#################

TEMP_INVERTER = response_modbus[0x1c]
TEMP_INVERTER_MODULE = response_modbus[0x1b]

print(f"Inverter temperature {TEMP_INVERTER}°C Inverter module temperature {TEMP_INVERTER_MODULE}°C")
print("\n")
###############___Temperature___#################

###############___DC ___#################


DC_V1 = response_modbus[0x06]/10
DC_V2 = response_modbus[0x08]/10

DC_V1_CURRENT = response_modbus[0x07]/100
DC_V2_CURRENT = response_modbus[0x09]/100

DC_V1_POWER = response_modbus[0x0a]/10
DC_V2_POWER = response_modbus[0x0b]/10


DC_V1_INSULATION_TO_GND = response_modbus[0x24]
DC_V2_INSULATION_TO_GND = response_modbus[0x25]

DC_V_INSULATION_TO_GND = response_modbus[0x26]

print(f"Voltage DC1 = {DC_V1} V, Current DC1 = {DC_V1_CURRENT} A, {DC_V1_POWER} W")
print(f"Voltage DC2 = {DC_V2} V, Current DC2 = {DC_V2_CURRENT} A, {DC_V2_POWER} W")
print("\n")


###############___DC ___#################


######SQL#####
DataMysql = get_time()
print(DataMysql)

# '2022-11-04 22:21:36'

# sql table making
# CREATE TABLE Sofar_Base.`Sofar` (Id DOUBLE NOT NULL AUTO_INCREMENT, Date DATE NOT NULL , Time TIME NOT NULL , Energy FLOAT NOT NULL COMMENT 'kWh' , Power_AC FLOAT NOT NULL COMMENT 'kW' , Temperature FLOAT NOT NULL COMMENT 'C°' , Voltage_AC1 FLOAT NOT NULL COMMENT 'V', Voltage_AC2 FLOAT NOT NULL COMMENT 'V' , Voltage_AC3 FLOAT NOT NULL COMMENT 'V', Current_AC1 FLOAT NOT NULL COMMENT 'A' , Current_AC2 FLOAT NOT NULL COMMENT 'A', Current_AC3 FLOAT NOT NULL COMMENT 'A', Power_DC1 FLOAT NOT NULL COMMENT 'W', Power_DC2 FLOAT NOT NULL COMMENT 'W', Voltage_DC1 FLOAT NOT NULL COMMENT 'V' , Voltage_DC2 FLOAT NOT NULL COMMENT 'V' , Current_DC1 FLOAT NOT NULL COMMENT 'A' , Current_DC2 FLOAT NOT NULL COMMENT 'A',PRIMARY KEY (Id) ) ENGINE = InnoDB;

# INSERT INTO `Sofar`(`date`, `Energy`) VALUES ('23-02-01 12:00:00', '3.9')


sql = f"""INSERT INTO Sofar (date, Energy, Power_AC, Inverter_temperature, Voltage_AC1, Voltage_AC2, Voltage_AC3,\n
 Current_AC1, Current_AC2, Current_AC3, Power_DC1, Power_DC2, Voltage_DC1, Voltage_DC2, Current_DC1, Current_DC2, \n
 Ac_freq, Module_temperature, Insulation_imp_cath_gnd, Insulation_imp_PV1, Insulation_imp_PV2, AC_reactive_power, AC_Today_Generation_Time) VALUES\n

 ('{DataMysql}', '{AC_Today_Production}','{AC_V1_3_ACTIVE_POWER}', '{TEMP_INVERTER}', '{AC_V1}', '{AC_V2}', '{AC_V3}',\n
  '{AC_V1_CURRENT}','{AC_V2_CURRENT}','{AC_V3_CURRENT}', '{DC_V1_POWER}','{DC_V2_POWER}', '{DC_V1}','{DC_V2}', '{DC_V1_CURRENT}',\n
  '{DC_V2_CURRENT}','{AC_V1_3_FREQ}', '{TEMP_INVERTER_MODULE}', '{DC_V_INSULATION_TO_GND}', '{DC_V1_INSULATION_TO_GND}',\n
  '{DC_V2_INSULATION_TO_GND}', '{AC_V1_3_REACTIVE_POWER}', '{AC_Today_Generation_Time}');"""


print(sql)

SQL_HOST = jsonObject["SQL_HOST"]
SQL_USER = jsonObject["SQL_USER"]
SQL_PASSWORD = jsonObject["SQL_PASSWORD"]
SQL_DATABASE = jsonObject["SQL_DATABASE"]

# Open database connection
db = pymysql.connect(host=SQL_HOST, user=SQL_USER, password=SQL_PASSWORD, database=SQL_DATABASE)

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()
print("Database version : %s " % data)

try:
    # Execute the SQL command
    cursor.execute(sql)

    # Commit your changes in the database
    db.commit()

except:
    # Rollback in case there is any error
    db.rollback()

# disconnect from server
db.close()


