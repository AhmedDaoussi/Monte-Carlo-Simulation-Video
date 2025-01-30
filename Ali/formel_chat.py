
# Beispiel-Eingabe
datum_string = "2024-08-27 15:15"
latitude = 49.014
longitude = 8.404
import pandas as pd
from datetime import datetime, timedelta
import math
import pytz
from astral import Observer
from astral.sun import azimuth, elevation

def calculate_deklination(tag_des_jahres):
    # Berechnung der Deklination (in Grad)
    deklination = -23.44 * math.cos(math.radians((360 / 365) * (tag_des_jahres + 10)))
    return deklination

def calculate_zeitgleichung(tag_des_jahres):
    # Berechnung der Zeitgleichung (in Minuten)
    B = (360 / 365) * (tag_des_jahres - 1)
    B_rad = math.radians(B)
    zeitgleichung = 229.18 * (0.000075 + 0.001868 * math.cos(B_rad) - 0.032077 * math.sin(B_rad)
                               - 0.014615 * math.cos(2 * B_rad) - 0.040849 * math.sin(2 * B_rad))
    return zeitgleichung

def calculate_stundenwinkel(woz, laengengrad):
    # Berechnung des Stundenwinkels
    stundenwinkel = (woz - 12) * 15
    return stundenwinkel

def time_to_decimal(time_str):
    # Konvertiere HH:MM in Dezimalformat
    hours, minutes = map(int, time_str.split(':'))
    decimal_time = hours + minutes / 60.0
    return decimal_time

def calculate_woz(zeit_deci, zeitgleichung, laengengrad, is_sommerzeit):
    # Berechnung der Wahren Ortszeit (WOZ)
    if is_sommerzeit:

        LC = (15*2 - laengengrad) * 4
    else:
        LC = (15 - laengengrad) * 4
    WOZ = zeit_deci + (zeitgleichung / 60) + (LC / 60)
    if is_sommerzeit:
        WOZ -= 1  # 1 Stunde zurück für Sommerzeit
    return WOZ

# Beispiel-Eingabe
datum_string = "2024-02-26 17:42"
latitude = 49.014
longitude = 8.404

# Konvertierung der lokalen Zeit in UTC-Zeit
local = pytz.timezone('Europe/Berlin')
naive = datetime.strptime(datum_string, "%Y-%m-%d %H:%M")
local_dt = local.localize(naive, is_dst=None)
utc_dt = local_dt.astimezone(pytz.utc)

# Berechnungen durchführen basierend auf UTC-Zeit
tag_des_jahres = utc_dt.timetuple().tm_yday
uhrzeit_utc = utc_dt.strftime("%H:%M")
zeit_deci = time_to_decimal(uhrzeit_utc)

# Deklination
deklination = calculate_deklination(tag_des_jahres)

# Zeitgleichung
zeitgleichung = calculate_zeitgleichung(tag_des_jahres)

# Sommerzeit checken (wird bei WOZ berücksichtigt)
is_sommerzeit = local_dt.timetuple().tm_isdst > 0

# Wahre Ortszeit (WOZ)
woz = calculate_woz(zeit_deci, zeitgleichung, longitude, is_sommerzeit)

# Stundenwinkel
stundenwinkel = calculate_stundenwinkel(woz, longitude)

# Azimut und Höhe über dem Horizont berechnen
observer = Observer(latitude=latitude, longitude=longitude)
azimuth_value = azimuth(observer, utc_dt)
elevation_value = elevation(observer, utc_dt)

# Erstellen des DataFrames
df = pd.DataFrame({
    'Datum': [datum_string],
    'Längengrad': [longitude],
    'Breitengrad': [latitude],
    'Tag des Jahres': [tag_des_jahres],
    'Deklination (in Grad)': [deklination],
    'Zeitgleichung (in Minuten)': [zeitgleichung],
    'Stundenwinkel (in Grad)': [stundenwinkel],
    'WOZ (Wahre Ortszeit)': [woz],
    'Lokale Zeit': [local_dt.strftime("%Y-%m-%d %H:%M")],
    'UTC-Zeit': [utc_dt.strftime("%Y-%m-%d %H:%M")],
    'Azimut (in Grad)': [azimuth_value],
    'Höhe über dem Horizont (in Grad)': [elevation_value]
})

# Ausgabe des DataFrames
print(df)
print(1)