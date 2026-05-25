import streamlit as st
from pages.home import inventory

st.set_page_config(
    page_title='Productos con stock bajo',
    page_icon=':material/trending_down:'
)

st.write('# Productos con stock bajo')
st.sidebar.header('Productos con bajo stock')

with st.form('list_products'):
    submitted = st.form_submit_button(
        label='Listar productos ahora',
        type='primary',
        width='stretch',
    )
    
    if submitted:
        all_products = inventory.low_stock_products()

        product_df: dict [str, list[int | str | float]] = {
                'CÓDIGO': [],
                'NOMBRE': [],
                'DESCRIPCIÓN': [],
                'UNIDAD DE MEDIDA': [],
                'EXISTENCIAS': [],
                'PRECIO POR UNIDAD': [],
                'VALOR EXISTENCIAS': [],
            }

        for product in all_products:
            product_df['CÓDIGO'].append(product.code)
            product_df['NOMBRE'].append(product.name)
            product_df['DESCRIPCIÓN'].append(product.description)
            product_df['UNIDAD DE MEDIDA'].append(product.unity)
            product_df['EXISTENCIAS'].append(product.quantity)
            product_df['PRECIO POR UNIDAD'].append(product.unity)
            product_df['VALOR EXISTENCIAS'].append(product.total_value())

        st.dataframe(product_df)