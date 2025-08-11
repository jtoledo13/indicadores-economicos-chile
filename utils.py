import pandas as pd
import numpy as np
import requests
from scipy.stats import skew, kurtosis
import plotly.express as px
from fpdf import FPDF
from datetime import datetime, timedelta

# --- API ---
def fetch_data(indicador: str, year: int) -> pd.DataFrame | None:
    url = f'https://mindicador.cl/api/{indicador}/{year}'
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    if "serie" not in data:
        return None
    df = pd.DataFrame(data["serie"])
    if df.empty:
        return None
    df['fecha'] = pd.to_datetime(df['fecha']).dt.tz_convert(None)
    df.set_index('fecha', inplace=True)
    return df.sort_index()

# --- Estadísticas ---
def compute_stats(df: pd.DataFrame) -> dict:
    stats = {
        "Media": df['valor'].mean(),
        "Mediana": df['valor'].median(),
        "Varianza": df['valor'].var(),
        "Desviación Estándar": df['valor'].std(),
        "Asimetría (Skewness)": skew(df['valor']),
        "Curtosis (Kurtosis)": kurtosis(df['valor']),
        "Mínimo": df['valor'].min(),
        "Máximo": df['valor'].max(),
        "Rango Intercuartílico": df['valor'].quantile(0.75) - df['valor'].quantile(0.25)
    }
    return stats

# --- Tendencias ---
def detect_trend(df: pd.DataFrame) -> str:
    x = np.arange(len(df))
    y = df['valor'].values
    coeff = np.polyfit(x, y, 1)
    slope = coeff[0]
    if slope > 0:
        return "Creciente"
    elif slope < 0:
        return "Decreciente"
    else:
        return "Estable"

# --- Anomalías ---
def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    mean = df['valor'].mean()
    std = df['valor'].std()
    anomalies = df[(df['valor'] > mean + 2*std) | (df['valor'] < mean - 2*std)]
    return anomalies

# --- Correlación ---
def create_correlation_heatmap(df_comb: pd.DataFrame):
    corr = df_comb.corr()
    fig = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        color_continuous_scale='RdBu_r',
        title='Matriz de Correlación entre Indicadores'
    )
    return fig

# --- Comparaciones entre años por mes/semestre/trimestre ---
def comparar_periodo(df: pd.DataFrame, mes: int = None, trimestre: int = None, semestre: int = None) -> pd.DataFrame:
    if mes:
        return df[df.index.month == mes]
    elif trimestre:
        return df[df.index.month.isin(range((trimestre - 1) * 3 + 1, trimestre * 3 + 1))]
    elif semestre:
        return df[df.index.month.isin(range((semestre - 1) * 6 + 1, semestre * 6 + 1))]
    return pd.DataFrame()

# --- Valor actual y variaciones ---
def obtener_valor_actual_y_cambios(df: pd.DataFrame) -> dict:
    df = df.sort_index()
    ultimo_valor = df['valor'].iloc[-1]
    ultima_fecha = df.index[-1]

    # Buscar valor anterior al último día
    anterior_dia = df[df.index < ultima_fecha]
    if not anterior_dia.empty:
        valor_dia_anterior = anterior_dia['valor'].iloc[-1]
        cambio_dia = (ultimo_valor - valor_dia_anterior) / valor_dia_anterior * 100
    else:
        cambio_dia = np.nan

    # Buscar valor hace un mes
    un_mes_atras = ultima_fecha - pd.DateOffset(months=1)
    valor_mes = df[df.index <= un_mes_atras]
    if not valor_mes.empty:
        valor_mes_anterior = valor_mes['valor'].iloc[-1]
        cambio_mes = (ultimo_valor - valor_mes_anterior) / valor_mes_anterior * 100
    else:
        cambio_mes = np.nan

    return {
        "fecha": ultima_fecha.date(),
        "valor_actual": ultimo_valor,
        "variacion_dia": cambio_dia,
        "variacion_mes": cambio_mes
    }

# --- Descripción de indicadores ---
def descripcion_indicador(nombre: str) -> str:
    descripciones = {
        "uf": "Unidad de Fomento: indexada a la inflación. Se usa en contratos, créditos y valores inmobiliarios.",
        "ivp": "Índice de Valor Promedio: indexado como la UF pero se ajusta cada 10 días.",
        "dolar": "Dólar observado: tipo de cambio entre peso chileno y dólar estadounidense.",
        "dolar_intercambio": "Dólar acuerdo: utilizado en transacciones interbancarias.",
        "euro": "Valor del Euro respecto al peso chileno.",
        "ipc": "Índice de Precios al Consumidor: mide la inflación mensual.",
        "utm": "Unidad Tributaria Mensual: utilizada para pagos tributarios y legales.",
        "imacec": "Indicador Mensual de Actividad Económica: estima la evolución del PIB.",
        "tpm": "Tasa de Política Monetaria: tasa base del Banco Central.",
        "libra_cobre": "Precio internacional de la libra de cobre.",
        "tasa_desempleo": "Porcentaje de la población económicamente activa que está desempleada.",
        "bitcoin": "Valor de Bitcoin en pesos chilenos (aproximado desde casas de cambio)."
    }
    return descripciones.get(nombre, "Sin descripción disponible.")

# --- Exportar PDF ---
class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Reporte Económico de Indicadores de Chile", ln=True, align="C")
        self.ln(5)

    def add_section_title(self, title):
        self.set_font("Arial", "B", 11)
        self.set_text_color(0)
        self.cell(0, 10, title, ln=True)
        self.ln(2)

    def add_text(self, text):
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 8, text)
        self.ln(2)

    def add_table(self, df: pd.DataFrame):
        self.set_font("Arial", "", 9)
        col_width = self.epw / len(df.columns)
        for col in df.columns:
            self.cell(col_width, 8, str(col), border=1)
        self.ln()
        for i in df.index:
            for col in df.columns:
                self.cell(col_width, 8, str(df.loc[i, col]), border=1)
            self.ln()