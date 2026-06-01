import streamlit as st
import time
import pandas as pd
from pages.home import inventory

st.set_page_config(
    page_title='Actualizar stock producto',
    page_icon=':material/update:'
)

st.markdown('# Actualizar stock producto')
st.sidebar.info('Actualizar stock producto')

with st.form('add_prod'):
    col1, col2 = st.columns(2)
    with col1:
        code = st.number_input (
            label='CÓDIGO:',
            placeholder='Código del producto',
            step=1,
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
            product: dict[str, bool | str | dict[str, str | int | float]] = inventory.search_by_code(code)
            if product['status'] is True:
                st.success(product['message'])
                product_dict: dict[str, str | int | dict] = product['product']
                product_df = pd.DataFrame(
                            {
                                'PRODUCTO ENCONTRADO': [product_dict['code'], product_dict['name'], product_dict['description'], product_dict['unity'], product_dict['quantity'], product_dict['price']],
                            },
                            index=['CÓDIGO', 'NOMBRE', 'DESCRIPCIÓN', 'UNIDAD DE MEDIDA', 'EXISTENCIAS', 'PRECIO POR UNIDAD'],
                        )
                st.dataframe(product_df)
                with col4:
                    time.sleep(0.2) 
                    product_was_saved: dict[str, bool | str] = inventory.update_stock(code, quantity)

                    progress_text = 'Actualizando...'
                    my_bar = st.progress(0, text=progress_text)

                    for percent_complete in range(5):
                        time.sleep(0.01)
                        my_bar.progress(percent_complete * 25, text=progress_text)
                        time.sleep(0.5)
                    else:
                        my_bar.empty()
                        if product_was_saved['status'] is True:
                            st.success(product_was_saved['message'], icon=None, width='stretch')
                            product_df = pd.DataFrame(
                                {
                                    'PRODUCTO ACTUALIZADO': [product_dict['code'], product_dict['name'], product_dict['description'], product_dict['unity'], product_dict['quantity'], product_dict['price']],
                                },
                                index=['CÓDIGO', 'NOMBRE', 'DESCRIPCIÓN', 'UNIDAD DE MEDIDA', 'EXISTENCIAS', 'PRECIO POR UNIDAD'],
                            )
                            st.dataframe(product_df)
                        else:
                            st.error(product_was_saved['message'], icon=None)
                        
            else:
                st.warning(product['message'])
