import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# Ruta al archivo Excel
excel_file = 'C:\\Users\\SantiagoFlynn\\Desktop\\Codigo\\Proyectos Arkano\\Git\\Transporte\\BDSartini.xlsx'

# Cargar todas las tablas en un diccionario de DataFrames
all_sheets_df = pd.read_excel(excel_file, sheet_name=None)

# Inicializar el estado de la pestaña si no existe
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "Remitos"

# Crear las pestañas
tabs = ["Remitos", "Facturas", "Maestros"]
tab_selected = st.sidebar.radio("Selecciona una pestaña", tabs)

# Guardar la pestaña seleccionada en el estado de la sesión
st.session_state.active_tab = tab_selected

# Importar y ejecutar el código de la pestaña correspondiente
if tab_selected == "Remitos":
    import remitos_tab
    st.session_state.nuevoremito = "No"
    remitos_tab.show_remitos_tab(all_sheets_df)
elif tab_selected == "Facturas":
    import facturas_tab
    facturas_tab.show_facturas_tab(all_sheets_df)
elif tab_selected == "Maestros":
    import maestros_tab
    maestros_tab.show_maestros_tab(all_sheets_df)

