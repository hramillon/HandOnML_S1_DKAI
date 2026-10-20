import sys
import os
import time
import requests
import pandas as pd

if len(sys.argv) != 3:
    print("Usage: python worker.py <fichier_todo.csv> <fichier_resultat.csv>")
    sys.exit(1)

todo_file, result_file = sys.argv[1], sys.argv[2]
todo_df = pd.read_csv(todo_file)

# Gestion de la reprise
if os.path.exists(result_file):
    done_df = pd.read_csv(result_file)
    todo_df = todo_df.merge(done_df[['LAT_20KM', 'LON_20KM', 'DATE_1J']], on=['LAT_20KM', 'LON_20KM', 'DATE_1J'], how='left', indicator=True)
    todo_df = todo_df[todo_df['_merge'] == 'left_only'].drop(columns=['_merge'])
else:
    pd.DataFrame(columns=['LAT_20KM', 'LON_20KM', 'DATE_1J', 'TEMP_MAX', 'HUMIDITY_MIN', 'WIND_SPEED_MAX', 'PRECIPITATION']).to_csv(result_file, index=False)

url = "https://archive-api.open-meteo.com/v1/archive"
session = requests.Session()

for count, (_, row) in enumerate(todo_df.iterrows(), 1):
    lat, lon, date = row['LAT_20KM'], row['LON_20KM'], row['DATE_1J']
    params = {
        "latitude": lat, "longitude": lon, "start_date": date, "end_date": date,
        "daily": ["temperature_2m_max", "relative_humidity_2m_min", "wind_speed_10m_max", "precipitation_sum"],
        "timezone": "auto"
    }
    
    while True:
        try:
            res = session.get(url, params=params, timeout=10)
            if res.status_code == 429:
                time.sleep(60) # Limite atteinte, pause
                continue
            if res.status_code == 200:
                data = res.json().get('daily', {})
                if data:
                    df_res = pd.DataFrame([{
                        'LAT_20KM': lat, 'LON_20KM': lon, 'DATE_1J': date,
                        'TEMP_MAX': data['temperature_2m_max'][0],
                        'HUMIDITY_MIN': data['relative_humidity_2m_min'][0],
                        'WIND_SPEED_MAX': data['wind_speed_10m_max'][0],
                        'PRECIPITATION': data['precipitation_sum'][0]
                    }])
                    df_res.to_csv(result_file, mode='a', header=False, index=False)
            break
        except Exception:
            time.sleep(5) # Erreur réseau, on attend avant de retry
            
    time.sleep(1.5) # Délai pour éviter le ban Open-Meteo
    if count % 100 == 0:
        print(f"Progression : {count} / {len(todo_df)}")
