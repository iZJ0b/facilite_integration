

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