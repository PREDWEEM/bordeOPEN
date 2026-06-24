import pandas as pd
import requests

# Coordenadas del nuevo sitio (aprox. provincia de La Pampa, Argentina)
lat = -37.770949
lon = -63.087790

# Rango de fechas de tu archivo original
start_date = "2026-01-01"
end_date = "2026-06-23"

# URL de la API de Open-Meteo para datos históricos diarios
url = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={start_date}&end_date={end_date}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=America%2FSao_Paulo"

print("Obteniendo datos meteorológicos para las nuevas coordenadas...")
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    daily = data['daily']
    
    # Construcción del DataFrame con las columnas idénticas a tu archivo original
    df_clima = pd.DataFrame({
        'Fecha': daily['time'],
        'TMAX': daily['temperature_2m_max'],
        'TMIN': daily['temperature_2m_min'],
        'Prec': daily['precipitation_sum']
    })
    
    # Rellenar posibles datos nulos con 0 para lluvia o interpolando temperaturas
    df_clima['Prec'] = df_clima['Prec'].fillna(0)
    df_clima['TMAX'] = df_clima['TMAX'].interpolate()
    df_clima['TMIN'] = df_clima['TMIN'].interpolate()
    
    # Exportar el archivo final
    nombre_archivo = 'meteo_daily_bordeopen_real.csv'
    df_clima.to_csv(nombre_archivo, index=False)
    
    print(f"¡Archivo '{nombre_archivo}' generado con éxito!")
    print(df_clima.head())
else:
    print(f"Error al consultar la API. Código de estado: {response.status_code}")
