import httpx

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OSRM_URL = "http://router.project-osrm.org/table/v1/driving"


def geocode_place(place_name: str, city: str) -> dict | None:
    """Yer adından koordinat tapır (latitude, longitude), fallback ilə."""
    headers = {"User-Agent": "DayRouteAI/1.0"}

    attempts = [
        f"{place_name}, {city}",
        f"{place_name}, {city}, Azerbaijan",
        f"{place_name}",
    ]

    for query in attempts:
        params = {"q": query, "format": "json", "limit": 1}
        response = httpx.get(NOMINATIM_URL, params=params, headers=headers, timeout=10)
        results = response.json()

        if results:
            return {
                "lat": float(results[0]["lat"]),
                "lon": float(results[0]["lon"]),
            }

    return None


def get_travel_time_matrix(coordinates: list[dict]) -> list[list[float]]:
    """
    Koordinatlar siyahısı arasında gediş vaxtı matrisini qaytarır (dəqiqə).
    coordinates: [{"lat": .., "lon": ..}, ...]
    """
    coords_str = ";".join(f"{c['lon']},{c['lat']}" for c in coordinates)
    url = f"{OSRM_URL}/{coords_str}"
    params = {"annotations": "duration"}

    response = httpx.get(url, params=params, timeout=15)
    data = response.json()

    durations_seconds = data["durations"]
    durations_minutes = [
        [round(sec / 60, 1) if sec is not None else None for sec in row]
        for row in durations_seconds
    ]
    return durations_minutes