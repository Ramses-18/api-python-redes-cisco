# Módulos que se usarán
import requests  # Para entender solicitudes
import json  # Para reconocer el formato json
from tabulate import tabulate  # Para crear tablas

baseUri = "http://localhost:58001/api/v1"  # URL de PT

# Llamada al API por el ticket
headers = {"Content-Type": "application/json"}
data = json.dumps({"username": "grupo9", "password": "cisco"})
resp = requests.post(baseUri + "/ticket", data=data, headers=headers)

print("Status de Solicitud:")
print(resp.status_code)
result = resp.json()

# Validar si recibimos el serviceTicket
if "serviceTicket" not in result.get("response", {}):
    print("\nError de autenticación. Respuesta del servidor:")
    print(json.dumps(result, indent=4))
    exit()

ticket = result["response"]["serviceTicket"]
print("\nEl Service Ticket es:")
print(ticket)

# Llamada al API para recibir los dispositivos de red
headers = {"X-Auth-Token": ticket}
resp = requests.get(baseUri + "/network-device", headers=headers)
result = resp.json()

print("\nDispositivos de Red:")
device_list = []
for i, item in enumerate(result.get("response", []), start=1):
    device_list.append([
        i,
        item.get("hostname", "N/A"),
        item.get("serialNumber", "N/A"),
        item.get("softwareVersion", "N/A")
    ])

print(tabulate(device_list, headers=["#", "Hostname", "Serial Number", "Software Version"], tablefmt="rst"))

# Llamada al API para recibir los host
headers = {"X-Auth-Token": ticket}
resp = requests.get(baseUri + "/host", headers=headers)
result = resp.json()

print("\nHosts de la Red:")
host_list = []
for i, item in enumerate(result.get("response", []), start=1):
    host_list.append([
        i,
        item.get("hostName", "N/A"),
        item.get("hostType", "N/A"),
        item.get("hostIp", "N/A")
    ])

print(tabulate(host_list, headers=["#", "Hostname", "Tipo", "IP"], tablefmt="rst"))
