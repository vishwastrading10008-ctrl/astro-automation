import swisseph as swe
import pandas as pd
from datetime import datetime, timedelta

# Swiss Ephemeris path (GitHub runner friendly)
swe.set_ephe_path(".")

PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mars": swe.MARS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS,
    "Saturn": swe.SATURN,
    "Rahu": swe.MEAN_NODE
}

def navamsha(longitude):
    return int((longitude % 30) / 3.333333) + 1

start_time = datetime.utcnow()
end_time = start_time + timedelta(days=7)

rows = []

current = start_time

while current <= end_time:
    jd = swe.julday(
        current.year,
        current.month,
        current.day,
        current.hour + current.minute/60
    )

    moon_pos = swe.calc(jd, swe.MOON)[0][0]
    moon_nav = navamsha(moon_pos)

    for name, planet in PLANETS.items():
        if name == "Moon":
            continue

        planet_pos = swe.calc(jd, planet)[0][0]
        planet_nav = navamsha(planet_pos)

        if moon_nav == planet_nav:
            rows.append([
                current.strftime("%Y-%m-%d %H:%M"),
                round(moon_pos, 4),
                moon_nav,
                name
            ])

    current += timedelta(hours=1)

df = pd.DataFrame(
    rows,
    columns=["datetime", "moon_degree", "moon_navamsha", "conjunction_planet"]
)

df.to_csv("conjunctions.csv", index=False)

print("Generated conjunctions.csv")
