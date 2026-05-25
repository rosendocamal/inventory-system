import streamlit as st
import time
from core.models import Product
import pandas as pd
from main import db as inventory

st.set_page_config(
    page_title='Buscar producto',
    page_icon=':material/search:'
)

if 'product_found' not in st.session_state:
    st.session_state.product_found = None

st.markdown('# Buscar producto')
st.sidebar.header('Buscar producto')

col1, col2 = st.columns(2)

with col1:
    with st.form('search_product_code'):
        code = st.number_input (
            label='CÓDIGO:',
            placeholder='Código del producto',
            step=10**12,
            min_value=10**12,
            max_value=10**13 - 1,
        )

        submitted_primary = st.form_submit_button(
        label='Buscar',
        type='primary',
        width='stretch',
        )

        if submitted_primary:
            if not code:
                st.warning('Código del producto no ingresado.')
                st.stop()
            if len(str(code)) != 13:
                st.warning('El código debe tener únicamente 13 dígitos.')
                st.stop()
            progress_text = 'Buscando producto mediante código...'
            my_bar = st.progress(0, text=progress_text)
            product: Product | bool = inventory.search_product(int(code))
            for percent_complete in range(3):
                time.sleep(0.01)
                my_bar.progress(percent_complete * 50, text=progress_text)
                time.sleep(0.5)
            else:
                my_bar.empty()
                if isinstance(product, bool):
                    st.error('El producto no existe', icon=None)
                else:
                    product_df = pd.DataFrame(
                        {
                            'PRODUCTO ENCONTRADO': [product.code, str(product.name), product.description, product.unity, product.quantity, product.price, product.total_value()],
                        },
                        index=['CÓDIGO', 'NOMBRE', 'DESCRIPCIÓN', 'UNIDAD DE MEDIDA', 'EXISTENCIAS', 'PRECIO POR UNIDAD', 'VALOR INVENTARIO'],
                    )
                    st.dataframe(product_df)

with col2:
    with st.form('search_product_name'):
        name = st.text_input(
            label='NOMBRE:',
            placeholder='Nombre del producto',
        )

        submitted_primary = st.form_submit_button(
        label='Buscar',
        type='primary',
        width='stretch',
        )

        if submitted_primary:
            if not name:
                st.warning('Nombre del producto no ingresado.')
                st.stop()
            progress_text = 'Buscando producto mediante nombre...'
            my_bar = st.progress(0, text=progress_text)
            product: Product | bool = inventory.search_by_name(name)
            for percent_complete in range(3):
                time.sleep(0.01)
                my_bar.progress(percent_complete * 50, text=progress_text)
                time.sleep(0.5)
            else:
                my_bar.empty()
                if isinstance(product, bool):
                    st.error('El producto no existe', icon=None)
                else:
                    product_df = pd.DataFrame(
                        {
                            'PRODUCTO ENCONTRADO': [product.code, str(product.name), product.description, product.unity, product.quantity, product.price, product.total_value()],
                        },
                        index=['CÓDIGO', 'NOMBRE', 'DESCRIPCIÓN', 'UNIDAD DE MEDIDA', 'EXISTENCIAS', 'PRECIO POR UNIDAD', 'VALOR INVENTARIO'],
                    )
                    st.dataframe(product_df)