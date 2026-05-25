import streamlit as st
import time
import pandas as pd
from core.models import Product
from main import db as inventory

st.set_page_config(
    page_title='Actualizar stock producto',
    page_icon=':material/update:'
)

st.markdown('# Actualizar stock producto')
st.sidebar.header('Actualizar stock producto')

with st.form('add_product'):
    col1, col2 = st.columns(2)
    with col1:
        code = st.number_input (
            label='CÓDIGO:',
            placeholder='Código del producto',
            step=10**12, # temporal steps
            min_value=10**12,
            max_value=10**13 - 1,
        )
    with col2:
        quantity = st.number_input(
            label='CANTIDAD:',
            step=100,
            value=0
            )


    submitted = st.form_submit_button(
        label='Guardar',
        type='primary',
        width='stretch'
        )
    
    if submitted:
        if not code:
            st.warning('Código del producto no ingresado.')
            st.stop()

        if len(str(code)) != 13:
            st.warning('El código debe tener únicamente 13 dígitos.')
            st.stop()

        col3, col4 = st.columns(2)

        with col3:
            product: Product | bool = inventory.search_product(int(code))
            if not isinstance(product, bool):
                st.success('Producto encontrado')
                product_df = pd.DataFrame(
                            {
                                'PRODUCTO ENCONTRADO': [product.code, str(product.name), product.description, product.unity, product.quantity, product.price, product.total_value()],
                            },
                            index=['CÓDIGO', 'NOMBRE', 'DESCRIPCIÓN', 'UNIDAD DE MEDIDA', 'EXISTENCIAS', 'PRECIO POR UNIDAD', 'VALOR INVENTARIO'],
                        )
                st.dataframe(product_df)
                with col4:
                    time.sleep(0.2) 
                    product_was_saved= inventory.update_stock(code, quantity)

                    progress_text = 'Actualizando...'
                    my_bar = st.progress(0, text=progress_text)

                    for percent_complete in range(5):
                        time.sleep(0.01)
                        my_bar.progress(percent_complete * 25, text=progress_text)
                        time.sleep(0.5)
                    else:
                        my_bar.empty()
                        if product_was_saved:
                            st.success('El stock ha sido actualizado', icon=None, width='stretch')
                            product_df = pd.DataFrame(
                                {
                                    'PRODUCTO ACTUALIZADO': [product.code, str(product.name), product.description, product.unity, product.quantity, product.price, product.total_value()],
                                },
                                index=['CÓDIGO', 'NOMBRE', 'DESCRIPCIÓN', 'UNIDAD DE MEDIDA', 'EXISTENCIAS', 'PRECIO POR UNIDAD', 'VALOR INVENTARIO'],
                            )
                            st.dataframe(product_df)
                        else:
                            st.error('El stock no se actualizó', icon=None)
                        
            else:
                st.warning('El producto no existe')
