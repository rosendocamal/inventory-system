import streamlit as st
from core.inventory import Inventory


st.set_page_config(
    page_title='Sistema de Inventario',
    page_icon=':material/edit:'
)

# st.write('# Sistema de Inventario')
st.sidebar.success('Selecciona una opción.')


pages = {
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


# st.markdown(
#     '''
#     Este Sistema de Inventario le facilitará gestionar su inventario,
#     desde añadir, eliminar, listar y buscar productos que usted mismo
#     tenga en sus manos.
#     **Seleccione en la sección lateral la opción de su preferencia** y 
#     empieza a explorar esta increíble herramienta.
#     ## ¿Quiere aprender más?
#     - Consulte el repositorio en GitHub.
#     '''
# )

db = Inventory()

pg = st.navigation(pages)
pg.run()