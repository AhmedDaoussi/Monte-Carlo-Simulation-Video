import pandas as pd
from datetime import datetime, timedelta
import math
import pytz

# Funktion zur Umwandlung der Zeit in ein Dezimalformat
def time_to_decimal(time_str):
    # Teile die Uhrzeit (im String-Format) in Stunden und Minuten
    hours, minutes = map(int, time_str.split(':'))

    # Konvertiere Minuten zu einem Bruchteil einer Stunde
    decimal_time = hours + minutes / 60.0

    return round(decimal_time, 2)

# Beispiel-Eingabe eines Datums
datum_string = input("Bitte Datum im Format 'YYYY-MM-DD HH:MM' eingeben: ")

# Definiere die Zeitzone für Europa/Berlin
berlin_tz = pytz.timezone('Europe/Berlin')

# Konvertiere den Datumstring in ein datetime-Objekt
lokale_zeit = datetime.strptime(datum_string, "%Y-%m-%d %H:%M")

# Lokalisieren der lokalen Zeit mit der Berlin-Zeitzone
lokalisierte_zeit = berlin_tz.localize(lokale_zeit)

# Konvertiere die lokalisierte Zeit in UTC
utc_zeit = lokalisierte_zeit.astimezone(pytz.utc)

# Berechnung des Tages des Jahres basierend auf der UTC-Zeit
tag_des_jahres = utc_zeit.timetuple().tm_yday

# Formatieren der Uhrzeit in HH:MM für UTC
uhrzeit_utc = utc_zeit.strftime("%H:%M")

# Erstellen des DataFrames mit einer Zeile
df = pd.DataFrame({
    'Längengrad': [8.404],
    'Breitengrad': [49.014],
    'Tag des Jahres': [tag_des_jahres],
    'Uhrzeit (UTC)': [uhrzeit_utc],
    'Stadt': ['Karlsruhe']
})

# Berechnung der Deklination und Zeitgleichung
B = (360 / 365) * (tag_des_jahres - 1)
B_rad = math.radians(B)
zeit_deci = time_to_decimal(uhrzeit_utc)
deklination = -23.45 * (math.cos(math.radians(360 * (tag_des_jahres + 10) / 365)))
zeitgleichung = 229.2 * (0.000075 + 0.001868 * math.cos(B_rad) - 0.032077 * math.sin(B_rad) - 0.014615 * math.cos(2 * B_rad) - 0.040849 * math.sin(2 * B_rad))

# Berechnung des LC (in Minuten) für MEZ (Winterzeit)
LC = (15 - df['Längengrad']) * 4

# Berechnung der wahren Ortszeit (WOZ)
WOZ = zeit_deci + (zeitgleichung / 60) + (LC / 60)

# Hinzufügen der berechneten Werte zum DataFrame
df['Zeit_Dezimal in Stunden (h) (UTC)'] = df['Uhrzeit (UTC)'].apply(time_to_decimal)
df['Deklination (in Grad)'] = deklination
df['Zeitgleichung (in Minuten)'] = zeitgleichung
df['LC (in Minuten)'] = LC
df['WOZ (in UTC)'] = WOZ

# Berechnung des Stundenwinkels und Sonnenhöhenwinkels
stundenwinkel = (WOZ - 12) * 15
sonnenhoehenwinkel = math.asin(
    math.cos(math.radians(df['Breitengrad'].iloc[0])) * math.cos(math.radians(deklination)) * math.cos(math.radians(stundenwinkel)) +
    math.sin(math.radians(deklination)) * math.sin(math.radians(df['Breitengrad'].iloc[0]))
)

df['Stundenwinkel in Grad'] = stundenwinkel
df['Sonnenhoehenwinkel in Radian'] = sonnenhoehenwinkel
df['Sonnenhoehenwinkel in Grad'] = math.degrees(sonnenhoehenwinkel)

# Berechnung des Azimuts basierend auf der WOZ
if WOZ.iloc[0] <= 12:
    azimut = 180 - math.degrees(math.acos(
        (math.sin(sonnenhoehenwinkel) * math.sin(math.radians(df['Breitengrad'].iloc[0])) - math.sin(math.radians(deklination))) /
        (math.cos(sonnenhoehenwinkel) * math.cos(math.radians(df['Breitengrad'].iloc[0])))
    ))
else:
    azimut = 180 + math.degrees(math.acos(
        (math.sin(sonnenhoehenwinkel) * math.sin(math.radians(df['Breitengrad'].iloc[0])) - math.sin(math.radians(deklination))) /
        (math.cos(sonnenhoehenwinkel) * math.cos(math.radians(df['Breitengrad'].iloc[0])))
    ))

df['Sonnenazimutwinkel in Grad'] = azimut
df['lokale Zeit'] = datum_string

# Ausgabe des DataFrames
print(df)
print(1)