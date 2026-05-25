import streamlit as st
from core.inventory import Inventory

inventory = Inventory()

st.write('# Sistema de Inventario')
st.write(
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
