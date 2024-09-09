import streamlit as st
import pandas as pd
import datetime
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
import re


def show_facturas_tab(all_sheets_df):
    # Acceder a cada tabla por nombre
    remito_df = all_sheets_df['Remito']
    camion_df = all_sheets_df['Camion']
    producto_df = all_sheets_df['Producto']
    chofer_df = all_sheets_df['Chofer']
    destinos_df = all_sheets_df['Destino']
    facturas_df = all_sheets_df['Factura']
    clientes_df = all_sheets_df['Cliente']

    st.session_state.remitos_sub_tab = "Lista de Remitos"
    st.session_state.maestros_sub_tab = "Lista de Maestros"

    # Inicializar el subestado de la pestaña si no existe
    if 'facturas_sub_tab' not in st.session_state:
        st.session_state.facturas_sub_tab = "Lista de Facturas"

    if 'selected_factura_index' not in st.session_state:
        st.session_state.selected_factura_index = None

    # Gestión de las pestañas
    if st.session_state.facturas_sub_tab == "Lista de Facturas":
        st.markdown("<h1 style='text-align: center;'>Facturas</h1>", unsafe_allow_html=True)

        st.divider()
        # Subtítulo con el número del remito seleccionado
        st.markdown("<h3 style='text-align: left; font-size: 20px;'>Filtros</h3>", unsafe_allow_html=True)
        # Filtros
        # Obtener el primer día del mes actual
        primer_dia_mes_actual = pd.to_datetime(datetime.date.today().replace(day=1))
        col1, col2, col3 = st.columns(3)

        with col1:
            fecha_desde = st.date_input("Fecha desde", value=pd.to_datetime(primer_dia_mes_actual))
            
        
        with col2:
            fecha_hasta = st.date_input("Fecha hasta", value=pd.to_datetime("today"))
        
        with col3:
            cliente_filter = st.selectbox("Cliente", options=["Todos"] + list(clientes_df['Cliente'].unique()))

        # Aplicar filtros
        if fecha_desde and fecha_hasta:
            facturas_df = facturas_df[(facturas_df['Fecha'] >= pd.to_datetime(fecha_desde)) & (facturas_df['Fecha'] <= pd.to_datetime(fecha_hasta))]


        if cliente_filter != "Todos":
            facturas_df = facturas_df[facturas_df['Cliente'] == cliente_filter]
   

        st.divider()
        # Subtítulo con el número del factura seleccionado
        st.markdown("<h3 style='text-align: center; font-size: 25px;'>Lista de Facturas</h3>", unsafe_allow_html=True)
        
        # Mostrar la tabla filtrada
        facturas_df['Nro Remito'] = facturas_df['Nro Remito'].astype(str)
        facturas_df['Fecha'] = facturas_df['Fecha'].dt.strftime('%Y-%m-%d')
        st.dataframe(facturas_df, width=1500)

        

            # Crear columnas con más espacio a los lados para centrar los botones
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

        with col2:
            if st.button("Agregar Nueva Factura"):
                st.session_state.facturas_sub_tab = "Agregar Nueva Factura"
                st.rerun()    

        with col3:
            if st.button("Modificar Factura"):
                st.session_state.facturas_sub_tab = "Modificar Factura"
                st.rerun()

        with col4:
            if st.button("Eliminar Factura"):
                st.session_state.facturas_sub_tab = "Eliminar Factura"
                st.rerun()

         
        

    elif st.session_state.facturas_sub_tab == "Agregar Nueva Factura":
        st.markdown("<h1 style='text-align: center;'>Nueva Factura</h1>", unsafe_allow_html=True)
        # Filtrado de remitos no facturados
        remitos_no_facturados = remito_df[remito_df['Facturado'] == "No"]

        # Agregar un filtro de cliente
        clientes_no_facturados = remitos_no_facturados['Cliente'].unique()
        cliente_filtro = st.selectbox("Filtrar remitos por cliente", options=["Todos"] + list(clientes_no_facturados))
        if 'last_cliente_filtro' not in st.session_state or st.session_state.last_cliente_filtro != cliente_filtro:
            st.session_state.last_cliente_filtro = cliente_filtro
            st.rerun()

        
        if cliente_filtro != "Todos":
            remitos_no_facturados = remitos_no_facturados[remitos_no_facturados['Cliente'] == cliente_filtro]

        # Agregar un filtro de producto
        productos_no_facturados = remitos_no_facturados['Producto'].unique()
        producto_filtro = st.selectbox("Filtrar remitos por producto", options=["Todos"] + list(productos_no_facturados))
        if 'last_producto_filtro' not in st.session_state or st.session_state.last_producto_filtro != producto_filtro:
            st.session_state.last_producto_filtro = producto_filtro
            st.rerun()

        if producto_filtro != "Todos":
            remitos_no_facturados = remitos_no_facturados[remitos_no_facturados['Producto'] == producto_filtro]


        if remitos_no_facturados.empty:
            st.write("No hay remitos sin facturar.")
            nro_remito_seleccionados = []
            nro_remito_str = ""
            cliente_seleccionado = None
        else:
            st.markdown("### Remitos sin facturar disponibles")

            # Configurar AgGrid para mostrar la tabla y permitir la selección
            gb = GridOptionsBuilder.from_dataframe(remitos_no_facturados)
            gb.configure_selection(selection_mode="multiple", use_checkbox=True)
            # Establecer la altura automática basada en el número de filas
            grid_height = min(400, 50 + len(remitos_no_facturados) * 35)  # Ajusta el 35 según la altura de cada fila

            grid_options = gb.build()

            # Mostrar la tabla con remitos no facturados
            grid_response = AgGrid(
                remitos_no_facturados,
                gridOptions=grid_options,
                update_mode=GridUpdateMode.SELECTION_CHANGED,
                data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
                fit_columns_on_grid_load=True,
                height=grid_height
            )
            
            # Verificar si se han seleccionado filas
            if grid_response['selected_rows'] is not None and len(grid_response['selected_rows']) > 0:
                selected_rows_df = pd.DataFrame(grid_response['selected_rows'])
                # Sumar el campo "Precio Total" de los registros seleccionados
                total_precio = selected_rows_df['Precio Total'].sum()
                st.write(f"Suma Total de Precio: {total_precio}")
            else:
                selected_rows_df = pd.DataFrame()
                total_precio = 0.0
            

            if not selected_rows_df.empty:
                nro_remito_seleccionados = selected_rows_df["Nro Remito"].tolist()
                clientes_seleccionados = selected_rows_df["Cliente"].unique()

                # Verificar si todos los clientes son iguales
                if len(clientes_seleccionados) > 1:
                    st.error("Solo se pueden seleccionar remitos de un cliente")
                    st.stop()  # Detener la ejecución si hay un error
                else:
                    cliente_seleccionado = clientes_seleccionados[0]  # Todos los clientes son iguales, tomar el primero
                    
            else:
                nro_remito_seleccionados = []
                nro_remito_str = ""
                cliente_seleccionado = None

            nro_remito_str = ', '.join(map(str, nro_remito_seleccionados))
            





        st.subheader("Agregar Nueva Factura")
        # Si ya se seleccionaron remitos, estos se pre-cargan en el campo Nro Remito
        form_factura(remito_df, facturas_df, clientes_df, all_sheets_df, modificar=False, nro_remito_inicial=nro_remito_str , cliente_sel = cliente_seleccionado , preciotot= total_precio)
         # Botón para volver a la lista de Facturas
        if st.button("Volver a la Lista de Facturas"):
            st.session_state.facturas_sub_tab = "Lista de Facturas"
            st.rerun()
        
    elif st.session_state.facturas_sub_tab == "Modificar Factura":
        st.markdown("<h1 style='text-align: center;'>Modificar Factura</h1>", unsafe_allow_html=True)
        form_factura(remito_df,  facturas_df,clientes_df, all_sheets_df, modificar=True)
        if st.button("Volver a la Lista de Facturas"):
            st.session_state.facturas_sub_tab = "Lista de Facturas"
            st.rerun()

    elif st.session_state.facturas_sub_tab == "Eliminar Factura":
        selected_factura = st.selectbox("Selecciona un Factura para eliminar:", 
                            facturas_df["Nro Factura"].astype(str))
        st.session_state.selected_factura_index = facturas_df[facturas_df["Nro Factura"].astype(str) == selected_factura].index[0]
        # Confirmación de eliminación
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Eliminar Factura"):
                st.session_state.show_delete_confirmation = True
                st.rerun()

        with col2:
            if st.button("Cancelar"):
                st.session_state.show_delete_confirmation = False
                st.session_state.facturas_sub_tab = "Lista de Facturas"
                st.rerun()
       

        

        if st.session_state.get('show_delete_confirmation', False):
            st.warning("¿Estás seguro de que deseas eliminar esta Factura?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Sí, eliminar"):
                    facturas_df = facturas_df.drop(st.session_state.selected_factura_index).reset_index(drop=True)
                    guardar_cambios(facturas_df, all_sheets_df)
                    st.session_state.show_delete_confirmation = False
                    st.session_state.facturas_sub_tab = "Lista de facturas"
                    st.rerun()

            with col2:
                if st.button("Cancelar"):
                    st.session_state.show_delete_confirmation = False
                    st.session_state.facturas_sub_tab = "Lista de facturas"
                    st.rerun()

def form_factura(remito_df, facturas_df,clientes_df, all_sheets_df, modificar=False, nro_remito_inicial=[], cliente_sel = "", preciotot= 0):
    # Si estamos modificando, cargamos los datos del factura seleccionado
    
    
    if modificar:
        selected_factura = st.selectbox("Selecciona un factura para modificar:", 
                            facturas_df["Nro Factura"].astype(str))
        st.session_state.selected_factura_index = facturas_df[facturas_df["Nro Factura"].astype(str) == selected_factura].index[0]

    if modificar:
        index = st.session_state.selected_factura_index
        nro_factura = facturas_df.loc[index, "Nro Factura"]
        fecha = pd.to_datetime(facturas_df.loc[index, "Fecha"], errors='coerce')
        nro_remito = facturas_df.loc[index, "Nro Remito"]
        cliente = facturas_df.loc[index, "Cliente"]
        total_facturado = facturas_df.loc[index, "Total Facturado"]

        # Manejar el caso donde 'Nro Remito' es NaN o vacío
        if pd.isna(nro_remito) or not nro_remito:
            nro_remito = []
        else:
            # Convertir nro_remito a lista de cadenas
            if isinstance(nro_remito, (int, float)):
                nro_remito = [str(nro_remito)]
            elif isinstance(nro_remito, str):
                nro_remito = nro_remito.split(', ')
            else:
                nro_remito = list(map(str, nro_remito))

    else:
        nro_remito = nro_remito_inicial
        fecha = pd.to_datetime("today")  # Se asigna la fecha actual como valor por defecto
        nro_factura = "_-____-______"
        if cliente_sel is not None:
            cliente = cliente_sel
        else:
            cliente = ""
        total_facturado = preciotot

    with st.form(key="form_factura"):
        col1, col2 = st.columns(2)

        with col1:
            nro_factura = st.text_input("Nro Factura", value=nro_factura)
            fecha = st.date_input("Fecha", value=fecha)

            # Filtrar solo los remitos que están en la lista de opciones
            remito_options = list(map(str, remito_df['Nro Remito'].unique()))  # Convertir opciones a cadenas
            
            if isinstance(nro_remito, str):
                nro_remito = [remito.strip() for remito in nro_remito.split(",")]
            
            default_remitos = [remito for remito in nro_remito if remito in remito_options]
            
            # Usar `multiselect` con los valores filtrados
            nro_remito = st.multiselect("Remitos", remito_options, default=default_remitos)

        with col2:
            cliente = st.selectbox("Cliente", [""] + list(clientes_df['Cliente'].unique()), index=0 if cliente == "" else list(clientes_df['Cliente'].unique()).index(cliente)+1)
            total_facturado = st.text_input("Total Facturado", value=total_facturado)

       

        submit_button = st.form_submit_button(label="Guardar factura" if not modificar else "Modificar factura")


        if submit_button:
            # Validar que Nro Factura, Nro Remito y Cliente no estén vacíos
            if not nro_factura:
                st.error("El campo 'Nro Factura' no puede estar vacío.")
            elif not nro_remito:
                st.error("El campo 'Nro Remito' no puede estar vacío.")
            elif not cliente:
                st.error("El campo 'Cliente' no puede estar vacío.")
            else:
                try:
                    total_facturado = float(total_facturado)
                except ValueError:
                    st.error("Asegúrate de que los campos numéricos contengan valores válidos.")
                    st.stop()

                # Convertir la lista de remitos seleccionados en una cadena separada por comas
                nro_remito_str = ', '.join(map(str, nro_remito))
                nro_factura= nro_factura.replace("_", "")
                nro_factura= formatear_numero_factura(nro_factura)

                if modificar:
                     # Aquí actualizamos los valores directamente en la fila correspondiente
                    facturas_df.at[index, "Nro Factura"] = nro_factura 
                    facturas_df.at[index, "Fecha"] = fecha
                    facturas_df.at[index, "Cliente"] = cliente
                    facturas_df.at[index, "Nro Remito"] = nro_remito_str
                    facturas_df.at[index, "Total Facturado"] =  total_facturado
                else:
                    nueva_factura = pd.DataFrame({
                        "Nro Factura": [nro_factura],
                        "Fecha": [fecha],
                        "Cliente": [cliente],
                        "Nro Remito": [nro_remito_str],
                        "Total Facturado": [total_facturado]
                    })
                    facturas_df = pd.concat([facturas_df, nueva_factura], ignore_index=True)
                
                

                # Asegúrate de que `nro_remito` y `Nro Remito` sean del mismo tipo (convertir a string)
                remito_df['Nro Remito'] = remito_df['Nro Remito'].astype(str)
                nro_remito = list(map(str, nro_remito))

                # Actualizar los remitos seleccionados en remito_df
                remito_df.loc[remito_df['Nro Remito'].isin(nro_remito), 'Facturado'] = "Si"
                remito_df.loc[remito_df['Nro Remito'].isin(nro_remito), 'Nro Factura'] = nro_factura

                st.success("factura guardado exitosamente" if not modificar else "factura modificado exitosamente")
                guardar_cambios(facturas_df,remito_df, all_sheets_df)

                st.session_state.facturas_sub_tab = "Lista de Facturas"
                st.rerun()

def guardar_cambios(facturas_df,remito_df, all_sheets_df):
    # Ruta al archivo Excel
    excel_file = 'C:\\Users\\SantiagoFlynn\\Desktop\\Codigo\\Proyectos Arkano\\Git\\Transporte\\BDSartini.xlsx'

    # Actualizar solo la hoja de 'factura'
    all_sheets_df['Factura'] = facturas_df
    all_sheets_df['Remito'] = remito_df

    # Guardar todas las hojas nuevamente en el archivo Excel
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        for sheet_name, df in all_sheets_df.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    st.success("Los cambios se han guardado exitosamente en la hoja 'Factura'.")


def formatear_numero_factura(nro_factura):
    # Verificar si el formato inicial es correcto
    match = re.match(r"([A-Za-z])-?(\d*)-?(\d*)", nro_factura)
    if match:
        letra = match.group(1)
        parte1 = match.group(2).zfill(4)  # Completa con ceros a la izquierda para tener 4 dígitos
        parte2 = match.group(3).zfill(6)  # Completa con ceros a la izquierda para tener 6 dígitos
        
        # Combinar todas las partes en el formato deseado
        nro_factura_formateado = f"{letra}-{parte1}-{parte2}"
        return nro_factura_formateado
    else:
        return None  # Si el formato es incorrecto, devolver None o manejar el error apropiadamente

