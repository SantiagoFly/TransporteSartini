import streamlit as st
import pandas as pd
import tempfile
import os

def show_maestros_tab(all_sheets_df):
    # Acceder a cada tabla por nombre
    remito_df = all_sheets_df['Remito']
    camion_df = all_sheets_df['Camion']
    producto_df = all_sheets_df['Producto']
    chofer_df = all_sheets_df['Chofer']
    destinos_df = all_sheets_df['Destino']
    facturas_df = all_sheets_df['Factura']
    clientes_df = all_sheets_df['Cliente']

    st.session_state.remitos_sub_tab = "Lista de Remitos"    
    st.session_state.facturas_sub_tab = "Lista de Facturas"

    # Inicializar el subestado de la pestaña si no existe
    if 'maestros_sub_tab' not in st.session_state:
        st.session_state.maestros_sub_tab = "Lista de Maestros"
    
    st.markdown("<h1 style='text-align: center;'>Maestros</h1>", unsafe_allow_html=True)
    st.write(st.session_state.maestros_sub_tab)

    # Gestión de las pestañas
    if st.session_state.maestros_sub_tab == "Lista de Maestros":
        st.markdown("<h3 style='text-align: center; font-size: 25px;'>Lista de Camiones</h3>", unsafe_allow_html=True)
        st.dataframe(camion_df, width=1000)
    
    # Botones para modificar o eliminar el Camion seleccionado
        col1, col2 , col3= st.columns(3)
        with col1:
            if st.button("Agregar Nueva Camion"):
                st.session_state.maestros_sub_tab = "Agregar Nuevo Camion"
                st.rerun()    
            
        with col2:
            if st.button("Modificar Camion"):
                
                st.session_state.maestros_sub_tab = "Modificar Camion"
                
                st.rerun()

        with col3:
            if st.button("Eliminar Camion"):
                st.session_state.maestros_sub_tab = "Eliminar Camion"
                st.rerun()

    
        st.subheader("Lista de productos")
        st.dataframe(producto_df, width=1000)
    
        # Crear columnas con más espacio a los lados para centrar los botones
        col1, col2, col3, col4, col5 = st.columns(5)
        with col2:
            if st.button("Agregar Nueva producto"):
                st.session_state.maestros_sub_tab = "Agregar Nueva producto"
                st.rerun()    
            
        with col3:
            if st.button("Modificar producto"):
                
                st.session_state.maestros_sub_tab = "Modificar producto"
                
                st.rerun()

        with col4:
            if st.button("Eliminar producto"):
                st.session_state.maestros_sub_tab = "Eliminar producto"
                st.rerun()


        st.subheader("Lista de Choferes")
        st.dataframe(chofer_df, width=1000)
    
    # Botones para modificar o eliminar el Chofer seleccionado
        col1, col2 , col3= st.columns(3)
        with col1:
            if st.button("Agregar Nueva Chofer"):
                st.session_state.maestros_sub_tab = "Agregar Nueva Chofer"
                st.rerun()    
            
        with col2:
            if st.button("Modificar Chofer"):
                
                st.session_state.maestros_sub_tab = "Modificar Chofer"
                
                st.rerun()

        with col3:
            if st.button("Eliminar Chofer"):
                st.session_state.maestros_sub_tab = "Eliminar Chofer"
                st.rerun()

        st.subheader("Lista de Destinos")
        st.dataframe(destinos_df, width=1000)
    
    # Botones para modificar o eliminar el Destino seleccionado
        col1, col2 , col3= st.columns(3)
        with col1:
            if st.button("Agregar Nueva Destino"):
                st.session_state.maestros_sub_tab = "Agregar Nueva Destino"
                st.rerun()    
            
        with col2:
            if st.button("Modificar Destino"):
                
                st.session_state.maestros_sub_tab = "Modificar Destino"
                
                st.rerun()

        with col3:
            if st.button("Eliminar Destino"):
                st.session_state.maestros_sub_tab = "Eliminar Destino"
                st.rerun()

    elif st.session_state.maestros_sub_tab == "Agregar Nuevo Camion":
        st.markdown("<h2 style='text-align: center;'>Agregar Nuevo Camion</h2>", unsafe_allow_html=True)
        form_camion( camion_df, all_sheets_df)
         # Botón para volver a la lista de maestros
        if st.button("Volver a la pantalla de Maestros"):
            st.session_state.maestros_sub_tab = "Lista de Maestros"
            st.rerun()
        
    elif st.session_state.maestros_sub_tab == "Modificar Camion":
        st.markdown("<h2 style='text-align: center;'>Modificar Camion</h2>", unsafe_allow_html=True)
        form_camion(camion_df, all_sheets_df, modificar=True)
        if st.button("Volver a la Lista de Maestros"):
            st.session_state.maestros_sub_tab = "Lista de Maestros"
            st.rerun()

    elif st.session_state.maestros_sub_tab == "Eliminar Camion":
        selected_camion = st.selectbox("Selecciona un Camion para eliminar:", 
                            camion_df["Patente"].astype(str))
        st.session_state.selected_camion_index = camion_df[camion_df["Patente"].astype(str) == selected_camion].index[0]
        # Confirmación de eliminación
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Eliminar Camion"):
                st.session_state.show_delete_confirmation = True
                st.rerun()

        with col2:
            if st.button("Cancelar"):
                st.session_state.show_delete_confirmation = False
                st.session_state.maestros_sub_tab = "Lista de Maestros"
                st.rerun()
       

        

        if st.session_state.get('show_delete_confirmation', False):
            st.warning("¿Estás seguro de que deseas eliminar este Camion?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Sí, eliminar"):
                    camion_df = camion_df.drop(st.session_state.selected_camion_index).reset_index(drop=True)
                    guardar_cambios_cam(camion_df, all_sheets_df)
                    st.session_state.show_delete_confirmation = False
                    st.session_state.maestros_sub_tab = "Lista de Maestros"
                    st.rerun()

            with col2:
                if st.button("Cancelar "):
                    st.session_state.show_delete_confirmation = False
                    st.session_state.maestros_sub_tab = "Lista de Maestros"
                    st.rerun()

def form_camion( camion_df, all_sheets_df, modificar=False):
    # Si estamos modificando, cargamos los datos del camion seleccionado
    # Seleccionar camion para modificar
    if modificar:
        selected_camion = st.selectbox("Selecciona un Camion para modificar:", 
                            camion_df["Patente"].astype(str))
        st.session_state.selected_camion_index = camion_df[camion_df["Patente"].astype(str) == selected_camion].index[0]
        st.divider()
        # Subtítulo con el número del camion seleccionado
        st.markdown(f"<h3 style='text-align: center; font-size: 20px;'>Modificando camion con patente: {selected_camion}</h3>", unsafe_allow_html=True)


    if modificar:
        index = st.session_state.selected_camion_index
        patente = camion_df.loc[index, "Patente"]
        tipo = camion_df.loc[index, "Tipo"]
        marca = camion_df.loc[index, "Marca"]
        
        
    else:
        patente = ""
        tipo = "" 
        marca = ""

    with st.form(key="form_camion"):
        col1, col2 = st.columns(2)

        with col1:
            patente = st.text_input("Patente", value=patente)
            marca = st.text_input("Marca", value=marca)

        with col2:
            tipo = st.text_input("Tipo", value=tipo)
        
        

        

        submit_button = st.form_submit_button(label="Guardar camion" if not modificar else "Modificar camion")



        if submit_button:
            if not patente or not tipo or not marca:
                st.error("Por favor, completa todos los campos numéricos.")
            else: 
                if modificar:
                     # Aquí actualizamos los valores directamente en la fila correspondiente
                    camion_df.at[index, "Patente"] = patente
                    camion_df.at[index, "Tipo"] = tipo
                    camion_df.at[index, "Marca"] = marca
                else:
                    nuevo_camion = pd.DataFrame({
                        "Patente": [patente],
                        "Tipo": [tipo],
                        "Marca": [marca]
                    })

                    camion_df = pd.concat([camion_df, nuevo_camion], ignore_index=True)

                st.success("camion guardado exitosamente" if not modificar else "camion modificado exitosamente")
                guardar_cambios_cam(camion_df, all_sheets_df)

                st.session_state.maestros_sub_tab = "Lista de Maestros"
                st.rerun()

def guardar_cambios_cam(camion_df, all_sheets_df):
    # Ruta al archivo Excel
    excel_file = 'C:\\Users\\SantiagoFlynn\\Desktop\\Codigo\\Proyectos Arkano\\Git\\Transporte\\BDSartini.xlsx'

    # Actualizar solo la hoja de 'camion'
    all_sheets_df['Camion'] = camion_df

    # Guardar todas las hojas nuevamente en el archivo Excel
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        for sheet_name, df in all_sheets_df.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    st.success("Los cambios se han guardado exitosamente en la hoja 'camion'.")
