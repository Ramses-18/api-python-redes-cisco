import csv
import json
import requests

BASE_URL = "http://localhost:58001/api/v1"
CREDENCIALES = {
    "username": "grupo9",
    "password": "cisco"
}

def obtener_ticket():
    """Obtiene el token de autenticación automáticamente."""
    url = f"{BASE_URL}/ticket"
    headers = {"content-type": "application/json"}
    
    resp = requests.post(url, data=json.dumps(CREDENCIALES), headers=headers)
    resp.raise_for_status()
    return resp.json()["response"]["serviceTicket"]

def generar_inventario_csv():
    try:
        ticket = obtener_ticket()
        headers = {"X-Auth-Token": ticket}
        inventario = []

        resp_devices = requests.get(f"{BASE_URL}/network-device", headers=headers)
        resp_devices.raise_for_status()
        devices = resp_devices.json().get("response", [])

        for dev in devices:
            inventario.append({
                "Categoria": "Equipo de Red",
                "Nombre": dev.get("hostname", "N/A"),
                "IP": dev.get("managementIpAddress", "N/A"),
                "MAC": dev.get("macAddress", "N/A"),
                "Detalle_Extra": dev.get("platformId", "N/A")
            })

        resp_hosts = requests.get(f"{BASE_URL}/host", headers=headers, verify=False)
        resp_hosts.raise_for_status()
        hosts = resp_hosts.json().get("response", [])

        for host in hosts:
            inventario.append({
                "Categoria": "Host",
                "Nombre": host.get("hostName", "N/A"),
                "IP": host.get("hostIp", "N/A"),
                "MAC": host.get("hostMac", "N/A"),
                "Detalle_Extra": f"Interfaz: {host.get('connectedInterfaceName', 'N/A')}"
            })

        nombre_archivo = "inventario_completo.csv"
        columnas = ["Categoria", "Nombre", "IP", "MAC", "Detalle_Extra"]

        with open(nombre_archivo, mode="w", newline="", encoding="utf-8") as archivo:
            writer = csv.DictWriter(archivo, fieldnames=columnas)
            writer.writeheader()
            writer.writerows(inventario)

        print(f"¡Éxito! Se exportaron {len(inventario)} equipos/hosts a '{nombre_archivo}'.")

    except requests.exceptions.RequestException as e:
        print(f"Error de conexión con la API del controlador: {e}")

if __name__ == "__main__":
    generar_inventario_csv()
