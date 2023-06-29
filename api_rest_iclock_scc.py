#Script de tiempo para Biometricos iclock
#Extraccion de Marcados Todos los dias 03::06:09

import time
import json
import requests
from zk import ZK, const

# creamos API REST - TOMCAT sistea EGOVF modulo SCC  afa636b2fb7cc7ef69d9a6b7ab1550e02472114f
api_url = "http://200.7.161.114:8080/fhce-egovf-scc/marcado/afa636b2fb7cc7ef69d9a6b7ab1550e02472114f"
headers = {"Content-Type":"application/json"}
respuesta = 0

#Lista de Biometricos con tecnologia Iclock
lista_biometrico = [['IP', port, False, 'lugar']]
conn = None

while True:
    #Obtenemos la hora del Servidor
    th = time.localtime().tm_hour
    tmin = time.localtime().tm_min
    tseg = time.localtime().tm_sec
    #Preguntamos si la hora esta en 23:50:30
    if((th == 23) and (tmin == 50) and (tseg >= 30)):
        tm_year = time.localtime().tm_year
        tm_mon = time.localtime().tm_mon
        tm_mday = time.localtime().tm_mday
        for biometrico in lista_biometrico:
            print('=========================================================================================================================')
            print(biometrico[0])
            print(biometrico[1])
            print(biometrico[2])
            print(biometrico[3])
            # Secrean los datos de Coneccion para el Biometrico
            zk = ZK(biometrico[0], port=biometrico[1], timeout=5, password=0, force_udp=biometrico[2], ommit_ping=False) # parametros de biometrico
            lugar = biometrico[3]
            # Conectamos el dispositivo
            try:
                conn = zk.connect()
                # dispositibo pausado
                conn.disable_device()
                # obtenemos los registros
                registros = conn.get_attendance()
                for r in registros:
                    # extraemos datos par el registro
                    times = r.timestamp
                    fecha = times.strftime("%Y-%m-%d")
                    hora = times.strftime("%H:%M:%S")
                    gestion = times.strftime("%Y")
                    mes = times.strftime("%m")
                    dia = times.strftime("%d")
                    h = times.strftime("%H")
                    m = times.strftime("%M")
                    #Preguntamos si los registros obtenidos se encuentran en el rango obtenido
                    if (int(gestion) == tm_year and int(mes) == tm_mon and int(dia) == tm_mday):
                        values = (r.uid, int(r.user_id), fecha, hora, int(gestion), int(mes), int(dia), int(h), int(m), r.punch, r.status, lugar)
                        # solo cargamos los registros pertenecientes al dia
                        print(values, ',')
                        #Creamos el Json para el API REST
                        marcado = {
                            "_01uid": r.uid,
                            "_02user_id": r.user_id,
                            "_03fecha": fecha,
                            "_04hora": hora,
                            "_05gestion": gestion,
                            "_06mes": mes,
                            "_07dia": dia,
                            "_08h": h,
                            "_09m": m,
                            "_10punch": r.punch,
                            "_11rstatus": r.status,
                            "_12lugar": lugar
                        }
                        #mandamos el Json
                        response = requests.post(api_url, data=json.dumps(marcado), headers=headers)
                        respuesta = response.status_code
                        #mostramos la Respuesta
                        print(respuesta)
                # Terminamos con un Saludo
                conn.test_voice()
                # Abilitamos el Dispositivo
                conn.enable_device()
            except Exception as e:
                print("Process terminate : {}".format(e))
            finally:
                if conn:
                    conn.disconnect()