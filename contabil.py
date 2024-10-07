import requests
from relacoes_contas.util import plano_contas, bancos
from layouts import layout_lancContabil

def exportar_financas():
    contas_contabeis = plano_contas()
    contas_bancos = bancos()
    url = "https://adminbackend.facilite.co/api/financas"

    payload = {
        "empresaId": 8551,
        "dataInicial": "2024-09-01",
        "dataFinal":"2024-09-30",
        "transacoesManuais": False,
        "apenasTransacoesNaoClassificadas": False,
        "statusTransacao": "ATIVO",
        "size": 1000
    }
    headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJlYXN5am9iIiwiYXV0aCI6IlJPTEVfRU1QUkVTQVMsUk9MRV9FU0NSSVRPUklPX0NPTlRBQklMSURBREUsUk9MRV9GSU5BTkNFSVJPLFJPTEVfRklTQ0FMLFJPTEVfR1JBRklDT1MsUk9MRV9QRVNTT0FMLFJPTEVfUFJPQ0VTU09TLFJPTEVfVVNFUiIsImV4cCI6MTcyOTM2MjA2N30.P_aARH0h07KaJCft68ijSz8qXNTR0yUzHRDpk0ExS_aBvglo248NL-zEdk6sVV5l3-cdUvr0TmBSyuPhEMt1xQ'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    lancamentos = response.json()

    layout_text = f"|0000||\n"
    naoClassificado = []
    for lancamento in lancamentos:
        tipo_movimento = lancamento['tipo']
        descricao = lancamento['descricao']
        dataPagamento = lancamento['dataPagamento']
        valor = lancamento['valor']

        if lancamento['descricaoClassificacao'] == "Não classificada":
            naoClassificado.append(lancamento)

        else: 
            # verifica o codigo reduzido da contrapartida
            codigoClassificacao = lancamento['codigoClassificacao'].replace('CODIGO_', '').replace('_', '')
            codReduzido_contrapartida = [conta['id'] for conta in contas_contabeis if conta['classificacao'] == codigoClassificacao][0]
            
            # buscar o codigo reduzido da conta bancaria
            id_banco_facilite = lancamento['banco']['id']
            codReduzido_banco = bancos()[str(id_banco_facilite)]

            text = layout_lancContabil(tipo_movimento, dataPagamento, codReduzido_banco, codReduzido_contrapartida, valor, descricao)
            layout_text += text
    print()


if __name__ == "__main__":
    exportar_financas()