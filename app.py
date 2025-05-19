import streamlit as st
import pandas as pd
import ast
from io import BytesIO

# Configurar layout ancho
st.set_page_config(layout="wide")

# Cargar los datos
@st.cache_data
def load_data():
    df = pd.read_csv("respuestas_foro - respuestas_foro (1).csv")
    df['Conceptos interpretativos'] = df['Conceptos interpretativos'].apply(ast.literal_eval)
    df['Estrategias detectadas'] = df['Estrategias detectadas'].apply(ast.literal_eval)
    return df

df = load_data()

# Crear listas únicas de conceptos y estrategias
all_concepts = sorted({item for sublist in df['Conceptos interpretativos'] for item in sublist})
all_strategies = sorted({item for sublist in df['Estrategias detectadas'] for item in sublist})

# Interfaz de usuario
st.title("Filtrado de opiniones del foro")

selected_concepts = st.multiselect("Selecciona Conceptos Interpretativos:", all_concepts)
selected_strategies = st.multiselect("Selecciona Estrategias Detectadas:", all_strategies)

# Filtrado
filtered_df = df.copy()
if selected_concepts:
    filtered_df = filtered_df[filtered_df['Conceptos interpretativos'].apply(lambda x: any(item in x for item in selected_concepts))]
if selected_strategies:
    filtered_df = filtered_df[filtered_df['Estrategias detectadas'].apply(lambda x: any(item in x for item in selected_strategies))]

# Mostrar resultado solo con las primeras 4 columnas
st.subheader("Resultados del Filtrado")
shown_df = filtered_df.iloc[:, :4]
st.dataframe(shown_df, use_container_width=True)

# Botón para descargar los resultados
st.subheader("Descargar resultados filtrados")
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Resultados')
    processed_data = output.getvalue()
    return processed_data

excel_data = to_excel(shown_df)
st.download_button(
    label="📥 Descargar Excel",
    data=excel_data,
    file_name="resultados_filtrados.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
