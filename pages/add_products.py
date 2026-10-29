import streamlit as st
import time
import pandas as pd
from core.models import Product
from pages.home import inventory

st.set_page_config(page_title="Añadir productos", page_icon=":material/add_2:")

st.markdown("# Añadir producto")
st.sidebar.info("Añadir producto")

with st.form("new_products"):
    col1, col2, col3 = st.columns(3)

    with col1:
        code = st.number_input(
            label="CÓDIGO:",
            placeholder="Código del producto",
            step=1,
            min_value=10**12,
            max_value=10**13 - 1,
        )
        name = st.text_input(
            label="NOMBRE:",
            placeholder="Nombre del producto",
            max_chars=36,
        )
    with col2:
        description = st.text_input(
            label="DESCRIPCIÓN:", placeholder="Descripción del producto"
        )
        price = st.number_input(
            label="PRECIO:",
            min_value=0.00,
        )
    with col3:
        quantity = st.number_input(label="CANTIDAD:", step=100, value=0)
        unity = st.selectbox(
            "UNIDAD:",
            ("PZ", "CJ", "GR", "KG", "ML", "LT", "M"),
            placeholder="Unidad de medida",
        )

    submitted = st.form_submit_button(label="Guardar", type="primary", width="stretch")

    if submitted:
        if not code:
            st.warning("Código del producto no ingresado.")
            st.stop()

        if len(str(code)) != 13:
            st.warning("El código debe tener únicamente 13 dígitos.")
            st.stop()

        if not name:
            st.warning("Ingrese el nombre del producto")
            st.stop()

        if not description:
            st.warning("Ingrese la descripción del producto.")
            st.stop()

        if not price:
            st.warning("Ingrese el precio del producto.")
            st.stop()

        if not unity:
            st.warning("Ingrese la unidad de medida del producto.")
            st.stop()

        product = Product(code, name, description, price, quantity, unity)
        product_dict = product.to_dict()

        product_df = pd.DataFrame(
            {
                "NUEVO PRODUCTO": [
                    product_dict["code"],
                    product_dict["name"],
                    product_dict["description"],
                    product_dict["unity"],
                    product_dict["quantity"],
                    product_dict["price"],
                ],
            },
            index=[
                "CÓDIGO",
                "NOMBRE",
                "DESCRIPCIÓN",
                "UNIDAD DE MEDIDA",
                "EXISTENCIAS",
                "PRECIO POR UNIDAD",
            ],
        )
        st.table(product_df)

        product_was_saved: dict[str, bool | str] = inventory.add_product(product)

        progress_text = "Guardando..."
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(5):
            time.sleep(0.01)
            my_bar.progress(percent_complete * 25, text=progress_text)
            time.sleep(0.20)
        else:
            my_bar.empty()
            if product_was_saved["status"] is True:
                st.success(product_was_saved["message"], icon=None, width="stretch")
            else:
                st.error(product_was_saved["message"], icon=None, width="stretch")
