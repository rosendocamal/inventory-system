import streamlit as st

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

class Main():
    st.set_page_config(
        page_title='Sistema de Inventario',
        page_icon=':material/edit:'
    )

    st.write('# ¡Bienvenido a su Inventario!')

    st.sidebar.success('Selecciona una opción.')

    st.markdown(
        '''
        Este Sistema de Inventario le facilitará gestionar su inventario,
        desde añadir, eliminar, listar y buscar productos que usted mismo
        tenga en sus manos.

        **Seleccione en la sección lateral la opción de su preferencia** y 
        empieza a explorar esta increíble herramienta.

        ## ¿Quiere aprender más?
        - Consulte el repositorio en GitHub.
        '''
    )