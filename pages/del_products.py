import streamlit as st
import time
from core.models import Product
from pages.home import inventory

import pandas as pd

st.set_page_config(
    page_title='Eliminar producto',
    page_icon=':material/delete:'
)

if 'product_found' not in st.session_state:
    st.session_state.product_found = None

st.markdown('# Eliminar producto')
st.sidebar.info('Eliminar producto')

with st.form('search_product'):
    st.write('### Buscar producto')
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
                st.session_state.product_found = None
            else:
                st.session_state.product_found = product

if st.session_state.product_found is not None:
    product = st.session_state.product_found 

    with st.form('del_product'): 
        st.write('### Producto')

        product_df = pd.DataFrame(
            {
                'PRODUCTO ENCONTRADO': [product.code, str(product.name), product.description, product.unity, product.quantity, product.price, product.total_value()],
            },
            index=['CÓDIGO', 'NOMBRE', 'DESCRIPCIÓN', 'UNIDAD DE MEDIDA', 'EXISTENCIAS', 'PRECIO POR UNIDAD', 'VALOR INVENTARIO'],
        )
        st.table(product_df)
    
        time.sleep(1)

        st.warning('¿Está seguro que desea eliminar este producto?')
        submitted_secondary = st.form_submit_button(
            label='Eliminar',
            type='secondary',
            use_container_width=True,
        )

        if submitted_secondary:
            with st.spinner('Eliminando producto...', show_time=False):
                product_was_del: bool | str = inventory.del_product(product.code)
                time.sleep(2)
            if not isinstance(product_was_del, str):
                st.success('El producto ha sido eliminado.')
                st.session_state.product_found = None
                time.sleep(3)
                st.rerun(scope='app')
            else:
                st.error(f'El producto no ha sido eliminado: {product_was_del}')