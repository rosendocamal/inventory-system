import streamlit as st
from core.inventory import Inventory
from core.database import DatabaseManager

inventory: Inventory = Inventory(DatabaseManager())

st.write('# Sistema de Inventario')
st.write(
'''
Este Sistema de Inventario le facilitará gestionar su inventario,
desde añadir, eliminar, listar y buscar productos que usted mismo
tenga en sus manos.
**Seleccione en la sección lateral la opción de su preferencia** y 
empieza a explorar esta increíble herramienta.
## ¿Quiere aprender más?
- ![Consulte el repositorio en GitHub](https://github.com/rosendocamal/inventory-system/)
- **Contacto:** ![RosendoCamal](https://github.com/rosendocamal)
'''
)
