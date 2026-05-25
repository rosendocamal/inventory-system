import streamlit as st

st.set_page_config(
    page_title='Sistema de Inventario',
    page_icon=':material/edit:'
)

pages = {
    "Home": [
        st.Page('pages/home.py', title='Inicio', icon=':material/home:'),
    ],
    "Productos": [
        st.Page("pages/add_products.py", title="Agregar producto", icon=':material/add_2:'),
        st.Page("pages/del_products.py", title='Eliminar producto', icon=':material/delete:'),
        st.Page('pages/update_product.py', title='Actualizar stock', icon=':material/update:'),
        st.Page('pages/search_products.py', title='Buscar producto', icon=':material/search:'),
        st.Page('pages/low_stocks.py', title='Stocks bajos', icon=':material/trending_down:'),
        st.Page('pages/list_products.py', title='Listar productos', icon=':material/table:')
    ],
    "Transacciones": [
        st.Page("pages/transactions.py", title="Historial", icon=':material/contract:')
        ],
}

pg = st.navigation(pages)
pg.run()