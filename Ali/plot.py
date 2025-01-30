import matplotlib.pyplot as plt
import numpy as np
from astral import LocationInfo
from astral.sun import azimuth, elevation
from datetime import datetime, timedelta, timezone
import pytz
from scipy.interpolate import make_interp_spline


# Funktion zur Berechnung der Sonnenpositionen an einem gegebenen Datum
def calculate_sun_positions(location, date):
    times = []
    azimuts = []
    elevations = []

    # Holen der Zeitzone
    local_tz = pytz.timezone(location.timezone)

    # Berechne die Sonnenpositionen für jede Stunde des Tages
    for hour in range(0, 24, 2):
        local_time = local_tz.localize(datetime(date.year, date.month, date.day, hour, 0))
        utc_time = local_time.astimezone(pytz.utc)
        azimuth_value = azimuth(location.observer, utc_time)
        elevation_value = elevation(location.observer, utc_time)

        # Speichere nur positive Elevationswerte und deren zugehörige Azimuts
        if elevation_value >= 0:
            times.append(hour)
            azimuts.append(azimuth_value)
            elevations.append(elevation_value)

    # Füge Start- und Endpunkte hinzu (Azimutwerte für Sonnenaufgang und -untergang)
    if elevations and elevations[0] > 0:
        elevations.insert(0, 0)
        azimuts.insert(0, azimuts[0])
        times.insert(0, times[0])
    if elevations and elevations[-1] > 0:
        elevations.append(0)
        azimuts.append(azimuts[-1])
        times.append(times[-1])

    return times, azimuts, elevations


# Standortinformationen (Karlsruhe)
location = LocationInfo("Karlsruhe", "Germany", "Europe/Berlin", 49.014, 8.404)

# Daten für die Diagramme
dates = [datetime(2024, 6, 21), datetime(2024, 3, 21), datetime(2024, 12, 21)]

# Plotten der Sonnenstandskurven
plt.figure(figsize=(12, 8))

for date in dates:
    times, azimuts, elevations = calculate_sun_positions(location, date)

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

    # Filter für positive Höhenwinkel
    positive_indices = elevations_smooth >= 0
    azimuts_smooth_positive = azimuts_smooth[positive_indices]
    elevations_smooth_positive = elevations_smooth[positive_indices]

    plt.plot(azimuts_smooth_positive, elevations_smooth_positive, label=date.strftime('%Y-%m-%d'))
    plt.scatter(azimuts, elevations, color='red')  # Punkte für die tatsächlichen Daten

    # Füge die Stundenbeschriftungen hinzu
    for i, hour in enumerate(times_sorted):
        local_time_str = f"{hour:02d}:00"
        plt.text(azimuts_sorted[i], elevations_sorted[i], local_time_str, fontsize=8, ha='right')

# Achsenbeschriftungen hinzufügen
plt.xlabel("Azimut (Grad)")
plt.ylabel("Sonnenhöhe (Grad)")
plt.title("Sonnenstandesdiagram für verschiedene Daten (Lokale Zeit)")

# Anpassung der x-Achse mit spezifischen Labels für Süd, West, Ost
plt.xticks(
    np.arange(0, 361, 30),  # Anpassen der Tick-Positionen
    [f'{i}°\n{label}' if label else f'{i}°' for i, label in zip(range(0, 361, 30),
                                                                ['Nord'] + [''] * 2 + ['Ost'] + [''] * 2 + ['Süd'] + [
                                                                    ''] * 2 + ['West'] + [''] * 2 + ['Nord'])]
)

plt.legend()
plt.grid(True)
plt.show()
