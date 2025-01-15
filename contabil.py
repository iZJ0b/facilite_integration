import requests
from relacoes_contas.util import plano_contas, bancos
from layouts import layout_lancContabil
from authentic_facilite import autenticacao_facilite

def exportar_financas(token, empresa_id: int, dataInicial: str, dataFinal:str):
    # contas_contabeis = plano_contas()
    contas_banco = consulta_codigoDominio_banco(token)
    url = "https://adminbackend.facilite.co/api/financas"

    payload = {
        "empresaId": empresa_id,
        "dataInicial":dataInicial,
        "dataFinal":dataFinal,
        "transacoesManuais": False,
        "apenasTransacoesNaoClassificadas": False,
        "statusTransacao": "ATIVO",
        "size": 1000
    }
    headers = {
    'Authorization': f'Bearer {token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    lancamentos = response.json()
    
    # buscar pelo cnpj da empresa
    cnpj = cnpj_empresa(token, empresa_id)
    layout_text = f"|0000|{cnpj}|\n"

    naoClassificado = []
    for lancamento in lancamentos:
        tipo_movimento = lancamento['tipo']
        descricao = lancamento['descricao']
        dataPagamento = lancamento['dataPagamento']
        valor = lancamento['valor']

        if lancamento['descricaoClassificacao'] == "Não classificada":
            data_format = dataPagamento.split('T')[0].split('-')
            dataLancamento = f"{data_format[-1]}/{data_format[1]}/{data_format[0]}"
            valor_formatado = f"{valor:,.2f}".replace(',', '').replace('.', ',')

            naoClassificado.append((dataLancamento, lancamento['descricao'], valor_formatado))

        else: 
            # verifica o codigo reduzido da contrapartida
            # codigoClassificacao = lancamento['codigoClassificacao'].replace('CODIGO_', '').replace('_', '')
            codReduzido_contrapartida = lancamento['codigoClassificacaoDominio']
            
            # buscar o codigo reduzido da conta bancaria
            id_banco_facilite = lancamento['banco']['bankid']
            codReduzido_banco = [conta['id'] for conta in contas_banco if conta['bankId'] == int(id_banco_facilite)][0]

            text = layout_lancContabil(tipo_movimento, dataPagamento, codReduzido_banco, codReduzido_contrapartida, valor, descricao)
            layout_text += text
    return layout_text, naoClassificado

def cnpj_empresa(token, empresa_id: int):
    url = f"https://adminbackend.facilite.co/api/empresas/{empresa_id}"
    headers = {
    'Authorization': f'Bearer {token}'
    }

    response = requests.request("GET", url, headers=headers)
    dados_empresa = response.json()
    return dados_empresa['cnpj']

def consulta_codigoDominio_banco(token):
    url = 'https://adminbackend.facilite.co/api/plano-contas/ofx'
    headers = {
    'Authorization': f'Bearer {token}'
    }

    response = requests.request("GET", url, headers=headers)
    lista_ofx = response.json()
    return [conta  for conta in lista_ofx if conta['bankId'] is not None] # retorna a lista das contas banco

def exportar_notas_fiscais():
    pass

def exportar_imposto(token, empresa_id, competencia):
    url = f"https://adminbackend.facilite.co/api/empresas/{empresa_id}/provisoes?page=0&size=1000&sort=id,desc"
    headers = {
    'Authorization': f'Bearer {token}'
    }


    response = requests.request("GET", url, headers=headers)
    provisoes = response.json()

    lancamento_provisoes = []
    for provisao in provisoes:
        if provisao['competencia'] == competencia:
            lancamento_provisoes.append(provisao)
    

    print()







if __name__ == "__main__":
    token = autenticacao_facilite()
    # exportar_financas(token, 8551, '2024-12-01', '2024-12-31')
    exportar_imposto(token, 8551, '2024-12')
    # cnpj_empresa(8551)

    # contas_banco = consulta_codigoDominio_banco(token)
    # for conta in contas_banco:
    #     if conta['bankId'] == 208:
    #         print()

    print()