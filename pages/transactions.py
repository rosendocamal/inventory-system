import streamlit as st
from main import db as inventory

st.set_page_config(
    page_title='Listar productos',
    page_icon=':material/contract:'
)

st.write('# Historial de Transacciones')
st.sidebar.header('Transacciones')

with st.form('list_products'):
    submitted = st.form_submit_button(
        label='Mostrar historial',
        type='primary',
        width='stretch',
    )
    
    if submitted:
        all_transactions: dict = inventory.transactions

        transaction_df: dict [str, list[int | str]] = {
                'TRANSACCIÓN': [],
                'TIPO': [],
                'CÓDIGO DE PRODUCTO': [],
                'FECHA DE TRANSACCIÓN': [],
     
            }
            
        for key, transaction in all_transactions.items():
            transaction_df['TRANSACCIÓN'].append(str(key))
            transaction_df['TIPO'].append(transaction.type)
            transaction_df['CÓDIGO DE PRODUCTO'].append(transaction.product_code)
            transaction_df['FECHA DE TRANSACCIÓN'].append(transaction.to_dict()['transaction_date'])

        st.dataframe(data=transaction_df)