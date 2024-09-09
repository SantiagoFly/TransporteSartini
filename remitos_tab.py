import streamlit as st
import pandas as pd
import datetime
import io

def show_remitos_tab(all_sheets_df):
    # Acceder a cada tabla por nombre
    remito_df = all_sheets_df['Remito']
    camion_df = all_sheets_df['Camion']
    producto_df = all_sheets_df['Producto']
    chofer_df = all_sheets_df['Chofer']
    destinos_df = all_sheets_df['Destino']
    facturas_df = all_sheets_df['Factura']
    clientes_df = all_sheets_df['Cliente']

    st.session_state.facturas_sub_tab = "Lista de Facturas"
    st.session_state.maestros_sub_tab = "Lista de Maestros"

    # Inicializar el subestado de la pestaña si no existe
    if 'remitos_sub_tab' not in st.session_state:
        st.session_state.remitos_sub_tab = "Lista de Remitos"

    if 'selected_remito_index' not in st.session_state:
        st.session_state.selected_remito_index = None

    # Gestión de las pestañas
    if st.session_state.remitos_sub_tab == "Lista de Remitos":
        st.markdown("<h1 style='text-align: center;'>Remitos</h1>", unsafe_allow_html=True)

        st.divider()
        # Subtítulo con el número del remito seleccionado
        st.markdown("<h3 style='text-align: left; font-size: 20px;'>Filtros</h3>", unsafe_allow_html=True)
        # Filtros
        # Obtener el primer día del mes actual
        primer_dia_mes_actual = pd.to_datetime(datetime.date.today().replace(day=1))
        col1, col2, col3 = st.columns(3)

        with col1:
            fecha_desde = st.date_input("Fecha desde", value=pd.to_datetime(primer_dia_mes_actual))
            fecha_hasta = st.date_input("Fecha hasta", value=pd.to_datetime("today"))
        
        with col2:
            facturado_filter = st.selectbox("Facturado", options=["Todos", "Si", "No"])
            nro_factura_filter = st.selectbox("Nro de Factura", options=["Todos"] + list(facturas_df['Nro Factura'].unique()))
        
        with col3:
            cliente_filter = st.selectbox("Cliente", options=["Todos"] + list(clientes_df['Cliente'].unique()))
            chofer_filter = st.selectbox("Chofer", options=["Todos"] + list(chofer_df['Chofer'].unique()))

        # Aplicar filtros
        if fecha_desde and fecha_hasta:
            remito_df = remito_df[(remito_df['Fecha'] >= pd.to_datetime(fecha_desde)) & (remito_df['Fecha'] <= pd.to_datetime(fecha_hasta))]

        if facturado_filter != "Todos":
            remito_df = remito_df[remito_df['Facturado'] == facturado_filter]

        if cliente_filter != "Todos":
            remito_df = remito_df[remito_df['Cliente'] == cliente_filter]

        
        if nro_factura_filter != "Todos":
            remito_df = remito_df[remito_df['Nro Factura'] == nro_factura_filter]

        if chofer_filter != "Todos":
            remito_df = remito_df[remito_df['Chofer'] == chofer_filter]    

        st.divider()
        # Subtítulo con el número del remito seleccionado
        st.markdown("<h3 style='text-align: center; font-size: 25px;'>Lista de Remitos</h3>", unsafe_allow_html=True)
        
        # Mostrar la tabla filtrada
        remito_df['Fecha'] = remito_df['Fecha'].dt.strftime('%Y-%m-%d')
        st.dataframe(remito_df, width=1500)

        

        # Botones para modificar o eliminar el remito 
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
        with col2:
            if st.button("Agregar Nuevo Remito"):
                st.session_state.remitos_sub_tab = "Agregar Nuevo Remito"
                st.rerun()    
            
        with col3:
            if st.button("Modificar Remito"):
                
                st.session_state.remitos_sub_tab = "Modificar Remito"
                
                st.rerun()

        with col4:
            if st.button("Eliminar Remito"):
                st.session_state.remitos_sub_tab = "Eliminar Remito"
                st.rerun()
        
        st.divider()
        # Convertir el DataFrame filtrado a un archivo Excel en memoria
        excel_data = to_excel(remito_df)
        if chofer_filter != "Todos":
            filename = chofer_filter
        elif cliente_filter != "Todos":
            filename = cliente_filter
        else: 
            filename= "remitos_filtrados"
    
        

        # Botón de descarga
        st.download_button(
            label="Descargar Excel",
            data=excel_data,
            file_name= f'{filename}.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

              

    elif st.session_state.remitos_sub_tab == "Agregar Nuevo Remito":
        st.markdown("<h2 style='text-align: center;'>Agregar Nuevo Remito</h2>", unsafe_allow_html=True)
        form_remito(remito_df, camion_df, producto_df, chofer_df, destinos_df, facturas_df, clientes_df, all_sheets_df, modificar=False)
         # Botón para volver a la lista de remitos
        if st.button("Volver a la Lista de Remitos"):
            st.session_state.remitos_sub_tab = "Lista de Remitos"
            st.session_state.nuevoremito = "No"
            st.rerun()
        
    elif st.session_state.remitos_sub_tab == "Modificar Remito":
        st.markdown("<h2 style='text-align: center;'>Modificar Remito</h2>", unsafe_allow_html=True)
        form_remito(remito_df, camion_df, producto_df, chofer_df, destinos_df, facturas_df, clientes_df, all_sheets_df, modificar=True)
        if st.button("Volver a la Lista de Remitos"):
            st.session_state.remitos_sub_tab = "Lista de Remitos"
            st.session_state.nuevoremito = "No"
            st.rerun()

    elif st.session_state.remitos_sub_tab == "Eliminar Remito":
        selected_remito = st.selectbox("Selecciona un Remito para eliminar:", 
                            remito_df["Nro Remito"].astype(str))
        st.session_state.selected_remito_index = remito_df[remito_df["Nro Remito"].astype(str) == selected_remito].index[0]
        # Confirmación de eliminación
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Eliminar Remito"):
                st.session_state.show_delete_confirmation = True
                st.rerun()

        with col2:
            if st.button("Cancelar"):
                st.session_state.show_delete_confirmation = False
                st.session_state.remitos_sub_tab = "Lista de Remitos"
                st.rerun()
       

        

        if st.session_state.get('show_delete_confirmation', False):
            st.warning("¿Estás seguro de que deseas eliminar este remito?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Sí, eliminar"):
                    remito_df = remito_df.drop(st.session_state.selected_remito_index).reset_index(drop=True)
                    guardar_cambios(remito_df, all_sheets_df)
                    st.session_state.show_delete_confirmation = False
                    st.session_state.remitos_sub_tab = "Lista de Remitos"
                    st.rerun()

            with col2:
                if st.button("Cancelar "):
                    st.session_state.show_delete_confirmation = False
                    st.session_state.remitos_sub_tab = "Lista de Remitos"
                    st.rerun()
                    

def form_remito(remito_df, camion_df, producto_df, chofer_df, destinos_df, facturas_df, clientes_df, all_sheets_df, modificar=False):
    # Si estamos modificando, cargamos los datos del remito seleccionado
    # Seleccionar remito para modificar
    if modificar:
        selected_remito = st.selectbox("Selecciona un Remito para modificar:", 
                            remito_df["Nro Remito"].astype(str))
        st.session_state.selected_remito_index = remito_df[remito_df["Nro Remito"].astype(str) == selected_remito].index[0]
        st.divider()
        # Subtítulo con el número del remito seleccionado
        st.markdown(f"<h3 style='text-align: center; font-size: 20px;'>Modificando remito Nro: {selected_remito}</h3>", unsafe_allow_html=True)


    if modificar == True :
        index = st.session_state.selected_remito_index
        nro_remito = remito_df.loc[index, "Nro Remito"]
        fecha = pd.to_datetime(remito_df.loc[index, "Fecha"], errors='coerce')
        cliente = remito_df.loc[index, "Cliente"]
        producto = remito_df.loc[index, "Producto"]
        patente = remito_df.loc[index, "Patente"]
        chofer = remito_df.loc[index, "Chofer"]
        origen = remito_df.loc[index, "Origen"]
        destino = remito_df.loc[index, "Destino"]
        toneladas = remito_df.loc[index, "Tonelada"]
        precio_tn = remito_df.loc[index, "Precio Tn"]
        facturado = remito_df.loc[index, "Facturado"]
        nro_factura = remito_df.loc[index, "Nro Factura"]

        # Reemplazar NaN por valores predeterminados
        cliente = cliente if pd.notna(cliente) else ""
        producto = producto if pd.notna(producto) else ""
        patente = patente if pd.notna(patente) else ""
        chofer = chofer if pd.notna(chofer) else ""
        origen = origen if pd.notna(origen) else ""
        destino = destino if pd.notna(destino) else ""
        nro_factura = nro_factura if pd.notna(nro_factura) else ""
        
        
    else:
        nro_remito = ""
        fecha = pd.to_datetime("today")  # Se asigna la fecha actual como valor por defecto
        cliente = ""
        producto = ""
        patente = ""
        chofer = ""
        origen = ""
        destino = ""
        toneladas = ""
        precio_tn = ""
        facturado = "No"
        nro_factura = ""

    with st.form(key="form_remito"):
        col1, col2 = st.columns(2)

        with col1:
            nro_remito = st.text_input("Nro Remito", value=nro_remito)
            fecha = st.date_input("Fecha", value=fecha)
            cliente = st.selectbox("Cliente", [""] + list(clientes_df['Cliente'].unique()), index=0 if cliente == "" else list(clientes_df['Cliente'].unique()).index(cliente)+1)
            producto = st.selectbox("Producto", [""] + list(producto_df['Producto'].unique()), index=0 if producto == "" else list(producto_df['Producto'].unique()).index(producto)+1)
            toneladas = st.text_input("Tonelada", value=toneladas)
            facturado = st.selectbox("Facturado", ["No", "Si"], index=["No", "Si"].index(facturado))
            
            
            

        with col2:
            patente = st.selectbox("Patente", [""] + list(camion_df['Patente'].unique()), index=0 if patente == "" else list(camion_df['Patente'].unique()).index(patente)+1)
            chofer = st.selectbox("Chofer", [""] + list(chofer_df['Chofer'].unique()), index=0 if chofer == "" else list(chofer_df['Chofer'].unique()).index(chofer)+1)
            origen = st.selectbox("Origen", [""] + list(destinos_df['Destino'].unique()), index=0 if origen == "" else list(destinos_df['Destino'].unique()).index(origen)+1)
            destino = st.selectbox("Destino", [""] + list(destinos_df['Destino'].unique()), index=0 if destino == "" else list(destinos_df['Destino'].unique()).index(destino)+1)
            precio_tn = st.text_input("Precio por Tn", value=precio_tn)
            opciones_factura = [""] + list(facturas_df['Nro Factura'].unique())
            index_factura = 0 if nro_factura == "" else opciones_factura.index(nro_factura) if nro_factura in opciones_factura else 0
            nro_factura = st.selectbox("Nro Factura", opciones_factura, index=index_factura)
            
        

        submit_button = st.form_submit_button(label="Guardar Remito" if not modificar else "Modificar Remito")



        if submit_button:
            if not nro_remito or not toneladas or not precio_tn or not cliente or not producto:
                st.error("Por favor, completa todos los campos numéricos.")
            else:
                try:
                    toneladas = float(toneladas)
                    precio_tn = float(precio_tn)
                    precio_total = toneladas*precio_tn

                except ValueError:
                    st.error("Asegúrate de que los campos numéricos contengan valores válidos.")
                    st.stop()

                if modificar:
                     # Aquí actualizamos los valores directamente en la fila correspondiente
                    remito_df.at[index, "Nro Remito"] = nro_remito
                    remito_df.at[index, "Fecha"] = fecha
                    remito_df.at[index, "Cliente"] = cliente
                    remito_df.at[index, "Producto"] = producto
                    remito_df.at[index, "Patente"] = patente
                    remito_df.at[index, "Chofer"] = chofer
                    remito_df.at[index, "Origen"] = origen
                    remito_df.at[index, "Destino"] = destino   
                    remito_df.at[index, "Tonelada"] = toneladas
                    remito_df.at[index, "Precio Tn"] = precio_tn
                    remito_df.at[index, "Facturado"] = facturado
                    remito_df.at[index, "Precio Total"] = precio_total
                
                else:
                    nuevo_remito = pd.DataFrame({
                        "Nro Remito": [nro_remito],
                        "Fecha": [fecha],
                        "Cliente": [cliente],
                        "Producto": [producto],
                        "Patente": [patente],
                        "Chofer": [chofer],
                        "Origen": [origen],
                        "Destino": [destino],
                        "Tonelada": [toneladas],
                        "Precio Tn": [precio_tn],
                        "Precio Total": [precio_total],
                        "Facturado": [facturado],
                        "Nro Factura": [nro_factura]
                    })

                    remito_df = pd.concat([remito_df, nuevo_remito], ignore_index=True)

                st.success("Remito guardado exitosamente" if not modificar else "Remito modificado exitosamente")
                guardar_cambios(remito_df, all_sheets_df)
                
                st.session_state.remitos_sub_tab = "Lista de Remitos"

def guardar_cambios(remito_df, all_sheets_df):
    # Ruta al archivo Excel
    excel_file = 'C:\\Users\\SantiagoFlynn\\Desktop\\Codigo\\Proyectos Arkano\\Git\\Transporte\\BDSartini.xlsx'

    # Actualizar solo la hoja de 'Remito'
    all_sheets_df['Remito'] = remito_df

    # Guardar todas las hojas nuevamente en el archivo Excel
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        for sheet_name, df in all_sheets_df.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    processed_data = output.getvalue()
    return processed_data
    
