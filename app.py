import streamlit as st
import pandas as pd
from datetime import datetime
import io
import plotly.express as px

from utils import (
    fetch_data, compute_stats, detect_trend, detect_anomalies,
    create_correlation_heatmap, obtener_valor_actual_y_cambios,
    descripcion_indicador, comparar_periodo, PDFReport
)

# Configuración de página
st.set_page_config(
    page_title="Indicadores Económicos Chile - Análisis Avanzado",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.markdown("<h1 style='color:white;'>📊 Indicadores Económicos de Chile - Análisis Avanzado</h1>", unsafe_allow_html=True)

st.markdown("""
Esta aplicación permite explorar, analizar y comparar indicadores económicos históricos de Chile.
Selecciona indicadores y años para obtener estadísticas completas, gráficos interactivos, correlaciones, detección de tendencias y alertas.
""")

# --- Selección de indicadores y años ---
indicadores_posibles = [
    'uf', 'ivp', 'dolar', 'dolar_intercambio', 'euro', 'ipc',
    'utm', 'imacec', 'tpm', 'libra_cobre', 'tasa_desempleo', 'bitcoin'
]

selected_indicadores = st.multiselect(
    "🎯 Selecciona uno o más indicadores",
    indicadores_posibles,
    default=['dolar', 'uf']
)

years = st.slider("🗓️ Selecciona rango de años", 1990, 2025, (2020, 2023))

# --- Configuración avanzada ---
st.sidebar.header("⚙️ Configuración avanzada")
fecha_inicio = st.sidebar.date_input("Fecha de inicio", datetime(years[0], 1, 1))
fecha_fin = st.sidebar.date_input("Fecha de fin", datetime(years[1], 12, 31))

alertas = []
st.sidebar.header("🚨 Configuración de alertas")
for ind in selected_indicadores:
    umbral = st.sidebar.number_input(f"🔔 Umbral para {ind.upper()} (valor máximo, 0 para desactivar)", min_value=0.0, value=0.0)
    if umbral > 0:
        alertas.append(f"{ind.upper()}: alerta si valor supera {umbral}")

# --- Carga de datos ---
with st.spinner("📥 Cargando datos..."):
    dict_dfs = {}
    for ind in selected_indicadores:
        df_total = pd.DataFrame()
        for y in range(years[0], years[1] + 1):
            df = fetch_data(ind, y)
            if df is not None:
                df_total = pd.concat([df_total, df])
        if not df_total.empty:
            df_total = df_total[
                (df_total.index >= pd.to_datetime(fecha_inicio)) &
                (df_total.index <= pd.to_datetime(fecha_fin))
            ]
            df_total = df_total[~df_total.index.duplicated(keep='last')]
            dict_dfs[ind] = df_total.sort_index()

if not dict_dfs:
    st.warning("⚠️ No se cargaron datos para los indicadores seleccionados y rango de años.")
    st.stop()

df_combined = pd.DataFrame({ind: df['valor'] for ind, df in dict_dfs.items()})
df_combined.dropna(how='all', inplace=True)

# --- Dashboard de Salud del Indicador ---
st.header("🧠 Dashboard de Salud de Indicadores")
for ind, df in dict_dfs.items():
    info = obtener_valor_actual_y_cambios(df)
    st.subheader(f"📌 {ind.upper()}")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Último Valor", round(info['valor_actual'], 2), f"Fecha: {info['fecha']}")
    col2.metric("Cambio Diario", f"{info['variacion_dia']:.2f}%" if not pd.isna(info['variacion_dia']) else "N/A")
    col3.metric("Cambio Mensual", f"{info['variacion_mes']:.2f}%" if not pd.isna(info['variacion_mes']) else "N/A")
    col4.markdown(f"📘 *{descripcion_indicador(ind)}*")

# --- Panel Resumen ---
st.header("📌 Resumen General")
col1, col2 = st.columns(2)

with col1:
    st.subheader("📑 Estadísticas")
    for ind, df in dict_dfs.items():
        stats = compute_stats(df)
        st.markdown(f"**{ind.upper()}**")
        st.dataframe(pd.DataFrame(stats, index=[0]).T.style.set_properties(**{
            'background-color': '#1E1E1E',
            'color': 'white',
            'border-color': 'gray'
        }))

with col2:
    st.subheader("📈 Tendencias")
    for ind, df in dict_dfs.items():
        tendencia = detect_trend(df)
        st.markdown(f"- **{ind.upper()}** → Tendencia: `{tendencia}`")

    st.subheader("🚨 Alertas Activas")
    if alertas:
        for a in alertas:
            st.warning(a)
    else:
        st.info("No se configuraron alertas.")

# --- Comparación por mes/trimestre/semestre ---
st.header("🔍 Comparar Indicador por Periodos Específicos")
indicador_comparar = st.selectbox("📊 Indicador a comparar", selected_indicadores)
periodo = st.radio("Periodo de comparación", ['Mes', 'Trimestre', 'Semestre'])
valor = None

if periodo == 'Mes':
    valor = st.selectbox("Mes", list(range(1, 13)))
elif periodo == 'Trimestre':
    valor = st.selectbox("Trimestre", [1, 2, 3, 4])
elif periodo == 'Semestre':
    valor = st.selectbox("Semestre", [1, 2])

if valor:
    df = dict_dfs[indicador_comparar]
    df_filtrado = comparar_periodo(df, mes=valor if periodo == 'Mes' else None,
                                         trimestre=valor if periodo == 'Trimestre' else None,
                                         semestre=valor if periodo == 'Semestre' else None)
    st.line_chart(df_filtrado['valor'])

# --- Gráficos temporales ---
st.header("📉 Evolución Temporal")
fig_ts = px.line(
    df_combined,
    x=df_combined.index,
    y=df_combined.columns,
    markers=True,
    title="📈 Indicadores en el tiempo",
    template="plotly_dark",
    color_discrete_sequence=px.colors.qualitative.Bold
)
fig_ts.update_layout(xaxis_title="Fecha", yaxis_title="Valor")
st.plotly_chart(fig_ts, use_container_width=True)

# --- Distribuciones (histograma y boxplot con mismo color) ---
st.header("📊 Distribuciones")
for ind, df in dict_dfs.items():
    st.subheader(f"📌 {ind.upper()}")

    fig_hist = px.histogram(
        df,
        x='valor',
        nbins=30,
        title=f"🔍 Histograma de {ind.upper()}",
        template="plotly_dark",
        color_discrete_sequence=['#20B2AA']
    )
    fig_hist.update_layout(xaxis_title="Valor", yaxis_title="Frecuencia")
    st.plotly_chart(fig_hist, use_container_width=True)

    fig_box = px.box(
        df,
        y='valor',
        points="outliers",
        title=f"📦 Boxplot de {ind.upper()}",
        template="plotly_dark",
        color_discrete_sequence=['#20B2AA']
    )
    st.plotly_chart(fig_box, use_container_width=True)

# --- Correlación ---
st.header("🔗 Correlación entre Indicadores")
fig_corr = create_correlation_heatmap(df_combined)
st.plotly_chart(fig_corr, use_container_width=True)



# --- Anomalías ---
st.header("⚠️ Anomalías Detectadas")
for ind, df in dict_dfs.items():
    anomalies = detect_anomalies(df)
    if anomalies.empty:
        st.success(f"✅ No se detectaron anomalías en {ind.upper()}")
    else:
        st.error(f"❗ Anomalías en {ind.upper()}")
        st.dataframe(anomalies)

# --- Exportar CSV ---
st.header("💾 Exportar Datos")
csv_buffer = io.StringIO()
df_combined.to_csv(csv_buffer)
csv_data = csv_buffer.getvalue()

st.download_button(
    label="⬇ Descargar CSV con datos combinados",
    data=csv_data,
    file_name="indicadores_combinados.csv",
    mime="text/csv"
)
# Generar el reporte en PDFF

if st.button("📤Generar Reporte PDF"):
    pdf = PDFReport()
    pdf.add_page()

    for ind, df in dict_dfs.items():
        pdf.add_section_title(f"{ind.upper()} - Resumen")
        pdf.add_text(descripcion_indicador(ind))

        stats = compute_stats(df)
        stats_df = pd.DataFrame(stats, index=[0]).T.reset_index()
        stats_df.columns = ["Indicador", "Valor"]
        pdf.add_table(stats_df)

        anomalies = detect_anomalies(df)
        if not anomalies.empty:
            pdf.add_section_title("Anomalías")
            pdf.add_text(f"{len(anomalies)} valores atípicos detectados.")
        pdf.ln()

    pdf_output = pdf.output(dest='S').encode('latin-1')



    st.download_button(
        label="📄 Descargar Reporte PDF",
        data=pdf_output,
        file_name="reporte_indicadores.pdf",
        mime="application/pdf"
    )

