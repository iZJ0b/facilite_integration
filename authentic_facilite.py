import requests
import json


def autenticacao_facilite():
    url = "https://adminbackend.facilite.co/api/authenticate"

    payload = json.dumps({
        "username": "easyjob",
        "password": "FaciliteParceiro",
        "rememberMe": True
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=payload)

    return response.json()['id_token']

def listagem_empresas(token):
    url = "https://adminbackend.facilite.co/api/empresas/lista-custom/pageable?searchable=&page=0&size=1000&sort=dataCriacao,desc&sort=id&isAtivo=true"

    payload = {}
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()



if __name__ == "__main__":
    token = autenticacao_facilite()
    # id_token = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJlYXN5am9iIiwiYXV0aCI6IlJPTEVfRU1QUkVTQVMsUk9MRV9FU0NSSVRPUklPX0NPTlRBQklMSURBREUsUk9MRV9GSU5BTkNFSVJPLFJPTEVfRklTQ0FMLFJPTEVfR1JBRklDT1MsUk9MRV9QRVNTT0FMLFJPTEVfUFJPQ0VTU09TLFJPTEVfVVNFUiIsImV4cCI6MTczMDkxNTI0M30.1g-t7xrwgN6ixRguF4m0eUrsYxXjDh300xtuCARqVOigwv9rP17yRr-uxoTwfqgPQ9JhfLn2Es85_bcc3Rm79Q"
    # listagem_empresas(token=id_token)
    print()