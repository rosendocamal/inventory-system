import streamlit as st
import time
import pandas as pd
from pages.home import inventory

st.set_page_config(page_title="Buscar producto", page_icon=":material/search:")

if "product_found" not in st.session_state:
    st.session_state.product_found = None

st.markdown("# Buscar producto")
st.sidebar.info("Buscar producto")

col1, col2 = st.columns(2)

with col1:
    with st.form("search_product_code"):
        code = st.number_input(
            label="CÓDIGO:",
            placeholder="Código del producto",
            step=1,
            min_value=10**12,
            max_value=10**13 - 1,
        )

        submitted_primary = st.form_submit_button(
            label="Buscar",
            type="primary",
            width="stretch",
        )

        if submitted_primary:
            if not code:
                st.warning("Código del producto no ingresado.")
                st.stop()
            if len(str(code)) != 13:
                st.warning("El código debe tener únicamente 13 dígitos.")
                st.stop()
            progress_text = "Buscando producto mediante código..."
            my_bar = st.progress(0, text=progress_text)
            product: dict[str, bool | str | dict[str, str | int | float]] = (
                inventory.search_by_code(int(code))
            )
            for percent_complete in range(3):
                time.sleep(0.01)
                my_bar.progress(percent_complete * 50, text=progress_text)
                time.sleep(0.5)
            else:
                my_bar.empty()
                if product["status"] is False:
                    st.error(product["message"], icon=None)
                else:
                    product_dict = product["product"]
                    product_df = pd.DataFrame(
                        {
                            "PRODUCTO ENCONTRADO": [
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
                    st.dataframe(product_df)

with col2:
    with st.form("search_product_name"):
        name = st.text_input(
            label="NOMBRE:",
            placeholder="Nombre del producto",
        )

        submitted_primary = st.form_submit_button(
            label="Buscar",
            type="primary",
            width="stretch",
        )

        if submitted_primary:
            if not name:
                st.warning("Nombre del producto no ingresado.")
                st.stop()
            progress_text = "Buscando producto mediante nombre..."
            my_bar = st.progress(0, text=progress_text)
            product: dict[str, bool | str | dict[str, str | int | float]] = (
                inventory.search_by_name(name)
            )
            for percent_complete in range(3):
                time.sleep(0.01)
                my_bar.progress(percent_complete * 50, text=progress_text)
                time.sleep(0.5)
            else:
                my_bar.empty()
                if product["status"] is False:
                    st.error(product["message"], icon=None)
                else:
                    product_dict = product["product"]
                    product_df = pd.DataFrame(
                        {
                            "PRODUCTO ENCONTRADO": [
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
                    st.dataframe(product_df)
