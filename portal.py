import streamlit as st

st.set_page_config(page_title='Integration Facilite', layout='wide')

def main():

    integration = st.Page("integration.py", title="Integração Facilite", icon=":material/dataset:") 
    saldo_inicial = st.Page("saldo_inicial.py", title="Saldo Inicial", icon=":material/data_thresholding:")

    pg = st.navigation(
        {
            "Automação": [integration, saldo_inicial]
        }
    )

    pg.run()



if __name__ == "__main__":
    main()