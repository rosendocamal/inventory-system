import streamlit as st
import time
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
        step=1,
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
        product: dict[str, bool | str | dict[str, str | int | float]] = inventory.search_by_code(int(code))
        for percent_complete in range(3):
            time.sleep(0.01)
            my_bar.progress(percent_complete * 50, text=progress_text)
            time.sleep(0.5)
        else:
            my_bar.empty()
            if product['status'] is False:
                st.error(product['message'], icon=None)
                st.session_state.product_found = None
            else:
                st.session_state.product_found = product['product']

if st.session_state.product_found is not None:
    product = st.session_state.product_found 

    with st.form('del_product'):
        st.write('### Producto')

        product_df = pd.DataFrame(
            {
                'PRODUCTO ENCONTRADO': [product['code'], product['name'], product['description'], product['unity'], product['quantity'], product['price']],
            },
            index=['CÓDIGO', 'NOMBRE', 'DESCRIPCIÓN', 'UNIDAD DE MEDIDA', 'EXISTENCIAS', 'PRECIO POR UNIDAD'],
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
                product_was_del: dict = inventory.del_product(product['code'])
                time.sleep(2)
            if product_was_del['status'] is True:
                st.success(product_was_del['message'])
                st.session_state.product_found = None
                time.sleep(3)
                st.rerun(scope='app')
            else:
                st.error(product_was_del['message'])