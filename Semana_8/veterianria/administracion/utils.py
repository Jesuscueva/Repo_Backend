import requests

# FORMA DE CONSUMIR UNA BASE DE DATOS DE OTRA BASE DE DATOS

def consultarDNI(dni):
    base_url = "https://apiperu.dev/api/"
    solicitud = requests.get(url=base_url+"dni/"+dni, headers={
        "Content-Type": "aplication/json",
        "Authorization": "Bearer 8389c125f5c44cd4791786ff111992abd840f1128ce626db5a67e18af56a18bb"
    })
    print(solicitud.status_code)
    print(solicitud.json())
    return solicitud.json()