import pandas as pd
from relacoes_contas.util import plano_contas
from layouts import layout_lancContabil_Varios_Varios
import streamlit as st
import time

def exportar_dados_dexion(planilha):
    df_cnpj = pd.read_excel(planilha, engine='xlrd')
    nome_empresa = df_cnpj['Unnamed: 3'][0]
    cnpj_empresa = df_cnpj['Unnamed: 3'][1].replace('.', '').replace('/', '').replace('-', '')

    df = pd.read_excel(planilha, engine='xlrd', header=4)

    index_colunas_delete = [1, 2, 3, 4, 5, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]

    df = df.drop(df.columns[index_colunas_delete], axis=1)

    df = df[df['Unnamed: 6'].notna()]

    df = df[df['Unnamed: 18'] > 0]

    return df.values.tolist(), cnpj_empresa, nome_empresa

def depara_contas_dominio(dados):

    contas_contabeis = plano_contas()

    for lancamento in dados:
        for conta in contas_contabeis:
            
            if conta['classificacao'] == str(int(lancamento[0])):
                lancamento.append(conta['id'])
                break

    return dados

def main():
    st.header('Exportar Saldo Inicial')

    planilha = st.file_uploader('Importar Planilha Balancete Dexion', type='xls')
    data_saldo_inicial = st.text_input('Data Saldo Inicial', help='Formato DD/MM/AAAA')

    if planilha is not None:
        if st.button('Processar Planilha'):
            with st.status("Processando Planilha...", expanded=True) as status:
                st.write("Lendo dados planilha...")
                dados, cnpj, nome_empresa = exportar_dados_dexion(planilha)
                time.sleep(2)
                st.write(f"Identificado Empresa: {nome_empresa} - {cnpj}")
                time.sleep(1)
                st.write("Realizando depara de contas...")
                contas_depara = depara_contas_dominio(dados)
                time.sleep(1)
                st.write("Gerando layout...")
                layout = f"|0000|{cnpj}|\n" \
                         f"|6000|V||||\n"
                contas_nao_encontradas = []
                for lancamento in contas_depara:
                    texto = layout_lancContabil_Varios_Varios(lancamento, data_saldo_inicial)
                    if texto is not None:
                        layout += texto
                    else:
                        contas_nao_encontradas.append(lancamento)


                status.update(
                    label="Processamento Completo!", state="complete", expanded=False
                )
            st.download_button(
                'Download Layout',
                data=layout, 
                file_name="saldo_inicial.txt", 
                icon=':material/exit_to_app:', 
                )
            st.subheader('Lançamentos Não Identificado a Conta Contábil')
            st.write(contas_nao_encontradas)
            st.code(layout)



main()
if __name__ == "__main__":
    planilha = 'EMPRESAS LUCRO PRESUMIDO/Balancete Analítico - Dezembro 2023 - AYRES SOFTWARE.XLS'
    data_lancamento = "31/12/2024"
    # cnpj = "48244439000196"
    dados, cnpj = exportar_dados_dexion(planilha)
    contas_depara = depara_contas_dominio(dados)

    layout = f"|0000|{cnpj}|\n" \
             f"|6000|V||||\n"
    
    for lancamento in contas_depara:

        texto = layout_lancContabil_Varios_Varios(lancamento, data_lancamento)
        layout += texto
        print()
print()