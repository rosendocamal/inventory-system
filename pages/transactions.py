import streamlit as st
from pages.home import inventory

st.set_page_config(
    page_title='Listar productos',
    page_icon=':material/contract:'
)

st.write('# Historial de Transacciones')
st.sidebar.info('Transacciones')

with st.form('list_products'):
    submitted = st.form_submit_button(
        label='Mostrar historial',
        type='primary',
        width='stretch',
    )
    
    if submitted:
        info_transactions: dict[str, bool | str | list[dict[str, str | int]]] = inventory.list_transactions()

        if info_transactions['status'] is False:
            st.info(info_transactions['message'])
        else:
            all_transactions: list[dict[str, str | int]] = info_transactions['transactions']

            transaction_df: dict [str, list[int | str]] = {
                    'TRANSACCIÓN': [],
                    'TIPO': [],
                    'CÓDIGO DE PRODUCTO': [],
                    'FECHA DE TRANSACCIÓN': [],

                }
            
            for index, transaction in enumerate(all_transactions):
                transaction_df['TRANSACCIÓN'].append(index + 1)
                transaction_df['TIPO'].append(transaction['category'])
                transaction_df['CÓDIGO DE PRODUCTO'].append(transaction['affected_product_code'])
                transaction_df['FECHA DE TRANSACCIÓN'].append(transaction['transaction_date'])

            st.dataframe(data=transaction_df)