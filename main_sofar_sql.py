"""
Author Marek Pikulski 12.03.2023.
benchmarek[at]outlook[dot]com
https://github.com/benchmarex

It is a project that downloads data on the production and operating parameters of the photovoltaic system sent from the
SofarSolar inverter using local connection MODBUS TCP/IP.
The data is sent to the local mysql server.
The script is written in Python and invoked using the cron mechanism at intervals of __ minutes.
"""


from pyModbusTCP.client import ModbusClient
from pythonping import ping
import json
import sys
import os


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











###########___start program___#################



with open('config.json') as jsonFile:
    jsonObject = json.load(jsonFile)

SERVER_MODBUS_HOST = jsonObject['SERVER_MODBUS_HOST']
SERVER_MODBUS_PORT = jsonObject['SERVER_MODBUS_PORT']

resp=str(ping(SERVER_MODBUS_HOST))
resp = resp.find("Request timed out")

if resp == -1:
        print(SERVER_MODBUS_HOST, 'Host is up')

else:
        print(SERVER_MODBUS_HOST, 'Host is unreachable')
        sys.exit()

response_modbus = get_inverter_data_modbus(SERVER_MODBUS_HOST, SERVER_MODBUS_PORT)
print(response_modbus,"\n")




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




"""

# extracting AC voltages

acv1 = r1.get('dataList')[14].get('value')
facv1 = float(acv1)

acv2 = r1.get('dataList')[15].get('value')
facv2 = float(acv2)

acv3 = r1.get('dataList')[16].get('value')
facv3 = float(acv3)

# znalezienie najwyzeszej wartosci

table = []
table.append(facv1)
table.append(facv2)
table.append(facv3)

vacmax = max(table)
print('max voltage ', vacmax, 'V')

# get AC power

acpwr = r1.get('dataList')[21].get('value')

print(f"power {acpwr} W")

# extracting day energy

energy = float(r1.get('dataList')[23].get('value'))

energy_kwh = str(energy)
print('energy ', energy, ' kWh')

# extracting module temperature

tinv = r1.get('dataList')[27].get('value')
tinv = str(tinv)
print(f"temp {tinv} °C")

dc1_voltage = r1.get('dataList')[8].get('value')  # get jason  voltage  str dc1
dc2_voltage = r1.get('dataList')[9].get('value')  # get jason  voltage str dc2

dc1_current = r1.get('dataList')[10].get('value')  # get jason  current str dc1
dc2_current = r1.get('dataList')[11].get('value')  # get jason  current  str dc2

dc1_power = r1.get('dataList')[12].get('value')  # get jason  power str dc1
dc2_power = r1.get('dataList')[13].get('value')  # get jason  power   moc str dc2

acv1_current = r1.get('dataList')[17].get('value')  # get jason  current ac1
acv2_current = r1.get('dataList')[18].get('value')  # get jason  current  prąd ac2
acv3_current = r1.get('dataList')[19].get('value')  # get jason  current prąd ac3

ac_freq = r1.get('dataList')[20].get('value')  # get frequency AC
print(f"AC Frequency {ac_freq} Hz")

module_temperature = r1.get('dataList')[28].get('value')  # get module temperature
print(f"Module temperature {module_temperature} °C")

insulation_imp_cath_gnd = r1.get('dataList')[36].get('value')  # get "Insulation Impedance- Cathode to ground"
print(f"Insulation Impedance- Cathode to ground {insulation_imp_cath_gnd} kΩ")

insulation_imp_PV1 = r1.get('dataList')[39].get('value')  # get "Insulation Impedance- Cathode to ground"
print(f"PV1 Insulation Impedance {insulation_imp_PV1} kΩ")

insulation_imp_PV2 = r1.get('dataList')[40].get('value')  # get "Insulation Impedance- Cathode to ground"
print(f"PV2 Insulation Impedance {insulation_imp_PV2} kΩ")

print(f"Voltage string1 = {dc1_voltage} V, Current DC1 = {dc1_current} A, POWER DC2 = {dc2_power} W")
print(f"Voltage string2 = {dc2_voltage} V, Current DC2 = {dc2_current} A, POWER DC2 = {dc2_power} W")

print(f"Voltage AC1 = {acv1} V, Current AC1 = {acv1_current} A")
print(f"Voltage AC2 = {acv2} V, Current AC2 = {acv2_current} A")
print(f"Voltage AC3 = {acv3} V, Current AC3 = {acv3_current} A")
########################################################################################



"""