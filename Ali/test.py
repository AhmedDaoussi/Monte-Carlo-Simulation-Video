import pandas as pd
from datetime import datetime, timedelta
import math
import pytz

def check_mez_or_mesz(datum_string):
    # Definiere die Zeitzone für Europa/Berlin
    tz = pytz.timezone('Europe/Berlin')

    # Konvertiere den Datumstring in ein datetime-Objekt
    datum = datetime.strptime(datum_string, "%Y-%m-%d %H:%M")

    # Lokalisieren des Datums mit der Berlin-Zeitzone
    localized_date = tz.localize(datum)

    # Prüfen, ob es Sommerzeit ist
    if localized_date.dst() != timedelta(0):
        return "MESZ"
    else:
        return "MEZ"

def time_to_decimal(time_str):
    # Teile die Uhrzeit (im String-Format) in Stunden und Minuten
    hours, minutes = map(int, time_str.split(':'))

    # Konvertiere Minuten zu einem Bruchteil einer Stunde
    decimal_time = hours + minutes / 60.0

    return round(decimal_time, 2)

# Beispiel-Liste von Datum-Strings
datum_string = input("Bitte Datum im Format 'YYYY-MM-DD HH:MM' eingeben: ")

# Berechnungen durchführen
datum = datetime.strptime(datum_string, "%Y-%m-%d %H:%M")

# Berechnung des Tages des Jahres
tag_des_jahres = datum.timetuple().tm_yday

# Formatieren der Uhrzeit in HH:MM
uhrzeit = datum.strftime("%H:%M")

# Erstellen des DataFrames
df = pd.DataFrame({
    'Längengrad': [8.404],
    'Breitengrad': [49.009],
    'Tag des Jahres': [tag_des_jahres],
    'Uhrzeit': [uhrzeit],
    'Stadt': ['Karlsruhe']
})

# Berechnungen
B = (360 / 365) * (tag_des_jahres - 1)
B_rad = math.radians(B)
zeit_deci = time_to_decimal(df['Uhrzeit'].iloc[0])
deklination = -23.45 * math.cos(math.radians(360 * (tag_des_jahres + 10) / 365))
zeitgleichung = 229.2 * (0.000075 + 0.001868 * math.cos(B_rad) - 0.032077 * math.sin(B_rad) -
                         0.014615 * math.cos(2 * B_rad) - 0.040849 * math.sin(2 * B_rad))

if check_mez_or_mesz(datum_string) == 'MESZ':
    LC = (15 * 2 - df['Längengrad'].iloc[0]) * 4
else:
    LC = (15 - df['Längengrad'].iloc[0]) * 4

WOZ_Sommer = zeit_deci + (zeitgleichung / 60) + (LC / 60) - 1
WOZ_Winter = zeit_deci + (zeitgleichung / 60) + (LC / 60)

# Ausgabe des DataFrames
df['Zeit_Dezimal'] = df['Uhrzeit'].apply(time_to_decimal)
df['Deklination (in Grad)'] = deklination
df['Zeitgleichung (in Minuten)'] = zeitgleichung

if check_mez_or_mesz(datum_string) == 'MESZ':
    df['WOZ'] = WOZ_Sommer
else:
    df['WOZ'] = WOZ_Winter

print(df)
print(1)