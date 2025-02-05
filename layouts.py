

def layout_lancContabil(tipo, dataPagamento, codReduzido_banco, codReduzido_contrapartida, valor, historico):
    data_format = dataPagamento.split('T')[0].split('-')
    dataLancamento = f"{data_format[-1]}/{data_format[1]}/{data_format[0]}"
    valor_formatado = f"{valor:,.2f}".replace(',', '').replace('.', ',')

    if tipo == "ENTRADA":
        texto = f"|6000|X||||\n" \
                f"|6100|{dataLancamento}|{codReduzido_banco}|{codReduzido_contrapartida}|{valor_formatado}||{historico}||||\n"
        
    else:
        texto = f"|6000|X||||\n" \
                f"|6100|{dataLancamento}|{codReduzido_contrapartida}|{codReduzido_banco}|{valor_formatado}||{historico}||||\n"
        
    return texto

def layout_lancContabil_Varios_Varios(lancamento, data_lancamento):
    if len(lancamento) == 6:
        valor_formatado = f"{lancamento[-3]:,.2f}".replace(',', '').replace('.', ',')

        if lancamento[-2] == 'D':
            texto = f"|6100|{data_lancamento}|{lancamento[-1]}||{valor_formatado}||SALDO INICIAL||||\n"

        else:
            texto = f"|6100|{data_lancamento}||{lancamento[-1]}|{valor_formatado}||SALDO INICIAL||||\n"

        return texto
    
    return None
