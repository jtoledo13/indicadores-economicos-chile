# Indicadores Económicos de Chile

Aplicación interactiva desarrollada con **Streamlit** para explorar, analizar y comparar indicadores económicos históricos de Chile.  
Permite estadísticas detalladas, gráficos interactivos, correlaciones, detección de tendencias, alertas y exportación de datos a CSV y PDF.

---

## 🚀 Características

- 📥 **Carga de datos históricos** de múltiples indicadores.
- 📈 **Visualización interactiva** con gráficos de Plotly y Streamlit.
- 📑 **Estadísticas automáticas** para cada indicador.
- 🔍 **Comparación por periodos** (mes, trimestre, semestre).
- 🔗 **Mapa de correlaciones** entre indicadores.
- ⚠️ **Detección de anomalías** y alertas configurables.
- 💾 **Exportación de resultados** en CSV y PDF.

---

## 🖼️ Capturas de pantalla


1. **Pantalla principal**  
  <img width="1891" height="295" alt="image" src="https://github.com/user-attachments/assets/25b561e5-0172-4ff6-82a2-d19752b64d91" />
<img width="1579" height="404" alt="image" src="https://github.com/user-attachments/assets/5ee403a8-cc13-4102-9b23-916b43905933" />


2. **Estadísticas y tendencias**  
<img width="1579" height="404" alt="image" src="https://github.com/user-attachments/assets/7f9b32aa-8ebb-48cc-9d43-7c672ae7585d" />
<img width="1424" height="786" alt="image" src="https://github.com/user-attachments/assets/940b0862-c7c9-4865-bdef-bca08e420d57" />
<img width="1604" height="632" alt="image" src="https://github.com/user-attachments/assets/e28b2db3-2a94-4e74-8739-3e76ddbd876c" />
<img width="1576" height="426" alt="image" src="https://github.com/user-attachments/assets/d2e02c94-d644-4556-b2cb-98ae73b46c91" />
<img width="1616" height="487" alt="image" src="https://github.com/user-attachments/assets/02a84da8-db24-47a7-bbbd-20d9290cc198" />
<img width="1625" height="336" alt="image" src="https://github.com/user-attachments/assets/ff05909e-ac81-409d-ac28-467b2e4d36a8" />
<img width="1603" height="438" alt="image" src="https://github.com/user-attachments/assets/551bae9d-ead3-45ce-8708-5ccb82c26a6a" />
<img width="1645" height="370" alt="image" src="https://github.com/user-attachments/assets/2709e02d-b15a-4a02-83fa-c788630cd080" />
<img width="1592" height="428" alt="image" src="https://github.com/user-attachments/assets/76ef9ee8-c565-472c-a6da-b6e8082f06c0" />
<img width="1602" height="460" alt="image" src="https://github.com/user-attachments/assets/1fdb873e-41f9-45a2-9e75-a1da30925f8c" />
<img width="394" height="196" alt="image" src="https://github.com/user-attachments/assets/a379e3c4-21be-4549-9958-bdbd2d4028ff" />


---


## 🌐 Fuente de datos: API REST de Indicadores Económicos

Esta aplicación obtiene los datos desde la **API REST de indicadores económicos diarios** de [mindicador.cl](https://mindicador.cl), un servicio *open source* que entrega los principales indicadores económicos para Chile en formato **JSON**.

📌 **Características de la API**:
- Datos **diarios** y **históricos**.
- Actualización constante a partir del sitio del **Banco Central de Chile**.
- Valores desde décadas pasadas hasta hoy, según el indicador.

**Indicadores disponibles**:
- **Unidad de fomento (UF)**: desde 1977.
- **Libra de Cobre**: desde 2012.
- **Tasa de desempleo**: desde 2009.
- **Euro**: desde 1999.
- **Imacec**: desde 1997.
- **Dólar observado**: desde 1984.
- **Tasa Política Monetaria (TPM)**: desde 2001.
- **Índice de valor promedio (IVP)**: desde 1990.
- **Índice de Precios al Consumidor (IPC)**: desde 1928.
- **Dólar acuerdo**: desde 1988.
- **Unidad Tributaria Mensual (UTM)**: desde 1990.
- **Bitcoin**: desde 2009.

---

## 📊 Interactividad y visualizaciones

Los gráficos generados con **Plotly** son completamente interactivos:
- 🔍 **Zoom** y desplazamiento.
- 💾 **Descarga en imagen**.
- 📐 **Selección de rango temporal**.
- 📌 **Filtrado dinámico** de series.

La interfaz de **Streamlit** permite configurar fácilmente:
- Fechas de inicio y fin.
- Selección de uno o múltiples indicadores.
- Comparaciones por **mes**, **trimestre** o **semestre**.

---

## 🚨 Sistema de alertas

El panel lateral permite establecer **umbrales máximos** para cada indicador.  
Si el valor supera ese umbral, el sistema muestra una advertencia visual clara.

💡 *Ideal para monitorear indicadores críticos sin tener que revisar manualmente cada gráfico.*

---

## 💾 Exportación de datos

La app incluye opciones para:
- Exportar todos los datos combinados a CSV con un clic
- Generar reportes PDF
- ## Dependencias

**Requisitos mínimos**
- Python 3.7+

**Librerías (mínimas para ejecutar la app)**
- pandas
- numpy
- streamlit
- plotly
- requests
- scipy
- fpdf2




