import pandas as pd
from datetime import datetime, timedelta
import math
import pytz
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
import numpy as np

# Funktion zur Umwandlung der Zeit in ein Dezimalformat
def time_to_decimal(time_str):
    hours, minutes = map(int, time_str.split(':'))
    decimal_time = hours + minutes / 60.0
    return round(decimal_time, 2)

# Funktion zur Berechnung der Wahren Ortszeit (WOZ)
def calculate_woz(zeit_deci, zeitgleichung, laengengrad, is_sommerzeit):
    if is_sommerzeit:
        LC = (15 * 2 - laengengrad) * 4  # Sommerzeit berücksichtigt UTC+2
    else:
        LC = (15 - laengengrad) * 4  # Winterzeit berücksichtigt UTC+1
    WOZ = zeit_deci + (zeitgleichung / 60) + (LC / 60)
    if is_sommerzeit:
        WOZ -= 1  # 1 Stunde zurück für Sommerzeit
    return WOZ

# Funktion zur Berechnung des Sonnenstandes (Azimut und Höhenwinkel)
def calculate_sun_position(date, latitude, longitude):
    times = []
    azimuts = []
    elevations = []

    # Iteriere über die Stunden von 0 bis 23 in 2-Stunden-Schritten
    for hour in range(0, 24, 2):
        datum_string = f"{date} {hour:02d}:00"
        berlin_tz = pytz.timezone('Europe/Berlin')
        lokale_zeit = datetime.strptime(datum_string, "%Y-%m-%d %H:%M")
        lokalisierte_zeit = berlin_tz.localize(lokale_zeit)
        utc_zeit = lokalisierte_zeit.astimezone(pytz.utc)
        tag_des_jahres = utc_zeit.timetuple().tm_yday
        uhrzeit_utc = utc_zeit.strftime("%H:%M")
        zeit_deci = time_to_decimal(uhrzeit_utc)

        # Berechnung der Deklination und Zeitgleichung
        B = (360 / 365) * (tag_des_jahres - 1)
        B_rad = math.radians(B)
        deklination = -23.45 * math.cos(math.radians(360 * (tag_des_jahres + 10) / 365))
        zeitgleichung = 229.2 * (0.000075 + 0.001868 * math.cos(B_rad) - 0.032077 * math.sin(B_rad) -
                                 0.014615 * math.cos(2 * B_rad) - 0.040849 * math.sin(2 * B_rad))

        # Bestimmung, ob Sommerzeit oder Winterzeit
        is_sommerzeit = lokale_zeit.dst() != timedelta(0)

        # Berechnung der Wahren Ortszeit (WOZ)
        WOZ = calculate_woz(zeit_deci, zeitgleichung, longitude, is_sommerzeit)

        # Berechnung des Stundenwinkels und Sonnenhöhenwinkels
        stundenwinkel = (WOZ - 12) * 15
        sonnenhoehenwinkel = math.asin(
            math.cos(math.radians(latitude)) * math.cos(math.radians(deklination)) * math.cos(
                math.radians(stundenwinkel)) +
            math.sin(math.radians(deklination)) * math.sin(math.radians(latitude))
        )

        # Berechnung des Azimuts basierend auf WOZ
        if WOZ <= 12:
            azimut = 180 - math.degrees(math.acos(
                (math.sin(sonnenhoehenwinkel) * math.sin(math.radians(latitude)) - math.sin(
                    math.radians(deklination))) /
                (math.cos(sonnenhoehenwinkel) * math.cos(math.radians(latitude))))
            )
        else:
            azimut = 180 + math.degrees(math.acos(
                (math.sin(sonnenhoehenwinkel) * math.sin(math.radians(latitude)) - math.sin(
                    math.radians(deklination))) /
                (math.cos(sonnenhoehenwinkel) * math.cos(math.radians(latitude))))
            )

        if math.degrees(sonnenhoehenwinkel) >= 0:  # Nur positive Elevationswerte beibehalten
            times.append(hour)
            azimuts.append(azimut)
            elevations.append(math.degrees(sonnenhoehenwinkel))

    return times, azimuts, elevations

# Koordinaten
latitude = 49.014
longitude = 8.404

# Daten, für die die Sonnenstandesdiagramme erstellt werden sollen
dates = ["2024-06-21", "2024-03-21", "2024-12-21"]

# Plotten der Diagramme
plt.figure(figsize=(12, 8))

for date in dates:
    times, azimuts, elevations = calculate_sun_position(date, latitude, longitude)

    # Sortiere die Azimutwerte und die entsprechenden Höhenwinkel
    sorted_indices = np.argsort(azimuts)
    azimuts_sorted = np.array(azimuts)[sorted_indices]
    elevations_sorted = np.array(elevations)[sorted_indices]
    times_sorted = np.array(times)[sorted_indices]

    # Entfernen von doppelten Azimut-Werten
    azimuts_unique, indices = np.unique(azimuts_sorted, return_index=True)
    elevations_unique = elevations_sorted[indices]

    # Interpolieren für glattere Kurven
    azimuts_smooth = np.linspace(min(azimuts_unique), max(azimuts_unique), 500)
    spl = make_interp_spline(azimuts_unique, elevations_unique, k=3)
    elevations_smooth = spl(azimuts_smooth)

    plt.plot(azimuts_smooth, elevations_smooth, label=date)
    plt.scatter(azimuts, elevations, color='red')  # Punkte für die tatsächlichen Daten

    # Füge die Stundenbeschriftungen hinzu
    for i, hour in enumerate(times):
        plt.text(azimuts[i], elevations[i], f"{hour:02d}:00", fontsize=8, ha='right')

# Achsenbeschriftungen hinzufügen
plt.xlabel("Azimut (Grad)")
plt.ylabel("Sonnenhöhe (Grad)")
plt.title("Sonnenstandesdiagram für verschiedene Daten")

# Anpassung der x-Achse mit spezifischen Labels für Süd, West, Ost
plt.xticks(
    np.arange(0, 361, 30),  # Anpassen der Tick-Positionen
    [f'{i}°\n{label}' if label else f'{i}°' for i, label in zip(range(0, 361, 30),
        ['Nord'] + [''] * 2 + ['Ost'] + [''] * 2 + ['Süd'] + [''] * 2 + ['West'] + [''] * 2 + ['Nord'])]
)

plt.legend()
plt.grid(True)
plt.show()
