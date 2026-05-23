import streamlit as st

import time

from core.models import Product
from main import sys_inv as inventory


st.set_page_config(
    page_title='Añadir productos',
    page_icon=':material/add_circle:'
)
st.markdown('# Añadir productos')
st.sidebar.header('Añadir productos')
with st.form('add_product'):
    col1, col2, col3 = st.columns(3)
    with col1:
        code = st.number_input (
            label='CÓDIGO:',
            placeholder='Código del producto',
            step=10000000,
            value=None,
        )
        name = st.text_input(
            label='NOMBRE:',
            placeholder='Nombre del producto',
            max_chars=36,
        )
    with col2:
        description = st.text_input(
            label='DESCRIPCIÓN:',
            placeholder='Descripción del producto'
            )
        price = st.number_input(
            label='PRECIO:',
            min_value=0.00,
        )
    with col3:
        quantity = st.number_input(
            label='CANTIDAD:',
            step=10000,
            value=0
            )
        unity = st.selectbox(
            'UNIDAD:',
            ('PZ', 'CJ', 'GR', 'KG', 'ML', 'LT'),
            placeholder='Unidad de medida'
        )
    submitted = st.form_submit_button(
        label='Guardar',
        type='primary',
        width='stretch'
        )
    if submitted:
        if not code:
            st.warning('Por favor, ingrese el código del producto.')
            st.stop()
        if not name:
            st.warning('Por favor, ingrese el nombre del producto.')
            st.stop()
        if not description:
            st.warning('Por favor, ingrese la descripción del producto.')
            st.stop()
        if not price:
            st.warning('Por favor, ingrese el precio del producto.')
            st.stop()
        if not quantity:
            st.warning('Por favor, ingrese la cantidad del producto.')
            st.stop()
        if not unity:
            st.warning('Por favor, ingrese la unidad de medida del producto.')
            st.stop()
        product = Product(code, name, description, price, quantity, unity)
        
        is_save: bool = inventory.add_product(product)

        progress_text = 'Guardando...'
        my_bar = st.progress(0, text=progress_text)
        for percent_complete in range(6):
            time.sleep(0.01)
            my_bar.progress(percent_complete * 20, text=progress_text)
            time.sleep(1)
        else:
            my_bar.empty()
            if is_save:
                st.success('El producto ha sido guardado', icon=None, width='stretch')
            else:
                st.error('El producto no ha sido guardado', icon=None)