import streamlit as st
from authentic_facilite import *
from contabil import *
import datetime
import calendar


# st.set_page_config(page_title='Integration Facilite', layout='wide')

def main():
    st.header('Facilite Integration')

    if 'TOKEN' not in st.session_state:
        st.session_state.TOKEN = autenticacao_facilite()
        st.session_state.lista_empresas = listagem_empresas(st.session_state.TOKEN)
        st.session_state.export = True
        st.session_state.valid_export = []
        st.session_state.layout_texto = ""
    
    st.divider()
    empresas = [f'{empresa["id"]} - {empresa["razaoSocial"]}' for empresa in st.session_state.lista_empresas]
    col_11, col_12, col_13 = st.columns([2, 2, 2])
    with col_11:
        options_empresas = st.multiselect('Selecione as Empresas', empresas)
    
    with col_12:
        today = datetime.datetime.now()

        jan_1 = datetime.date(2024, 1, 1)

        ultimo_dia_mesAtual = calendar.monthrange(today.year, today.month)[1]
        mes_atual = datetime.date(today.year, today.month, ultimo_dia_mesAtual)

        periodo_datas = st.date_input(
            "Selecione o periodo",
            (),
            jan_1,
            mes_atual,
            format="DD/MM/YYYY",
        )
        # st.write(periodo_datas[1].strftime("%Y-%m-%d"))

    st.divider()
    if len(options_empresas) > 0:

        col_14, col_15, col_16, col_17 = st.columns([2, 3, 3, 2])
        
        with col_15:
            st.subheader('Lançamento Contábil')

            st.checkbox('Finanças', key='export_financas_contabil')
            st.checkbox('Notas Emitidas', key='export_nf_emitidas_contabil', disabled=True)
            st.checkbox('Notas Recebidas', key='export_nf_recebido_contabil', disabled=True)
            st.checkbox('Provisão Simples Nacional', key='export_impostos_contabil', disabled=True)
        
        with col_16:
            st.subheader('Lançamento Fiscal')
            st.checkbox('Notas Emitidas', key='export_nf_emitidas_fiscal', disabled=True)
            st.checkbox('Notas Recebidas', key='export_nf_recebido_fiscal', disabled=True)

        with col_17:
            if st.button('Gerar Lançamentos', use_container_width=True, icon=":material/sync:"):
                itens_export = [item for item in st.session_state if 'export_' in item]
                st.session_state.valid_export = [item for item in itens_export if st.session_state[item]]
                
                if st.session_state.valid_export:   # se possui campo selecionado para exportacao
                    with st.spinner('In progress ...'):
                        for empresa in options_empresas:    # fazer o loop por empresas que foram selecionados para exportacao
                            lancamentos_naoClassificados = []
                            for item_export in st.session_state.valid_export:
                                
                                if 'financas_contabil' in item_export:
                                    texto_layout, naoClassificados = exportar_financas(
                                        st.session_state.TOKEN,
                                        int(empresa.split(' - ')[0]), 
                                        periodo_datas[0].strftime("%Y-%m-%d"), 
                                        periodo_datas[1].strftime("%Y-%m-%d")
                                        )
                                    st.session_state.layout_texto += texto_layout
                                    lancamentos_naoClassificados.append(naoClassificados)
                        
                        st.session_state.export = False
                else:
                    st.error('Nenhum item selecionado para exportação')
            
            if st.download_button('Exportar', 
                                  data=st.session_state.layout_texto, 
                                  file_name="export_lancamentos.txt", 
                                  use_container_width=True, 
                                  icon=':material/exit_to_app:', 
                                  disabled=st.session_state.export):
                st.session_state.layout_texto = ""
                st.session_state.export = True
                st.rerun()






main()
if __name__ == "__main__":
    main()