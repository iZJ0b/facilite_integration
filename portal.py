import streamlit as st
from authentic_facilite import *
from contabil import *

st.set_page_config(page_title='Integration Facilite', layout='wide')

def main():
    st.header('Facilite Integration')

    if 'TOKEN' not in st.session_state:
        st.session_state.TOKEN = autenticacao_facilite()
        st.session_state.lista_empresas = listagem_empresas(st.session_state.TOKEN)
        st.session_state.export = 0
        st.session_state.valid_export = []
    
    st.divider()
    empresas = [f'{empresa["id"]} - {empresa["razaoSocial"]}' for empresa in st.session_state.lista_empresas]
    col_11, col_12, col_13 = st.columns([2, 2, 2])
    with col_11:
        options_empresas = st.multiselect('Selecione as Empresas', empresas)
    # st.write(st.session_state.lista_empresas)

    st.divider()
    if len(options_empresas) > 0:

        col_14, col_15, col_16, col_17 = st.columns([2, 3, 3, 2])
        
        with col_15:
            st.subheader('Lançamento Contábil')

            st.checkbox('Finanças', key='export_financas_contabil')
            st.checkbox('Notas Emitidas', key='export_nf_emitidas_contabil', disabled=True)
            st.checkbox('Notas Recebidas', key='export_nf_recebido_contabil', disabled=True)
            st.checkbox('Impostos', key='export_impostos_contabil', disabled=True)
        
        with col_16:
            st.subheader('Lançamento Fiscal')
            st.checkbox('Notas Emitidas', key='export_nf_emitidas_fiscal', disabled=True)
            st.checkbox('Notas Recebidas', key='export_nf_recebido_fiscal', disabled=True)

        with col_17:
            if st.button('Exportar', use_container_width=True, icon=':material/exit_to_app:'):
                st.session_state.export = 1

                itens_export = [item for item in st.session_state if 'export_' in item]
                st.session_state.valid_export = [item for item in itens_export if st.session_state[item]]
                
            
            if st.button('Voltar', use_container_width=True):
                pass
        
        # mostrar os dados depois de clicar em EXPORTAR
        if st.session_state.export == 1:
            if st.session_state.valid_export:   # se possui campo selecionado para exportacao
                
                for empresa in options_empresas:    # fazer o loop por empresas que foram selecionados para exportacao
                    with st.expander(empresa):
                        for item_export in st.session_state.valid_export:
                            
                            if 'financas_contabil' in item_export:
                                layout_texto, naoClassificados = exportar_financas(int(empresa.split(' - ')[0]))

                                tab1, tab2 = st.tabs(['Exportavel', 'Não Classificados'])
                                with tab1:
                                    st.text(layout_texto)
                                with tab2:
                                    for iten in naoClassificados:
                                        st.code(iten)
                                    # st.write(naoClassificados)


            else:
                st.error('Nenhum item selecionado para exportação')




if __name__ == "__main__":
    main()