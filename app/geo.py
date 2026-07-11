import httpx
import time

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
OSRM_URL = "http://router.project-osrm.org/table/v1/driving"


def geocode_place(place_name: str, city: str) -> dict | None:
    """Yer adından koordinat tapır (latitude, longitude), fallback ilə."""
    headers = {"User-Agent": "DayRouteAI/1.0 (contact: toghrulahmad@gmail.com)"}

    attempts = [
        f"{place_name}, {city}",
        f"{place_name}, {city}, Azerbaijan",
        f"{place_name}",
    ]

    for query in attempts:
        params = {"q": query, "format": "json", "limit": 1}
        try:
            response = httpx.get(NOMINATIM_URL, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            results = response.json()
        except (httpx.HTTPStatusError, httpx.RequestError, ValueError) as e:
            print(f"Geocoding xətası ({query}): {e}")
            time.sleep(1)
            continue

        if results:
            return {
                "lat": float(results[0]["lat"]),
                "lon": float(results[0]["lon"]),
            }

        time.sleep(1)  # Nominatim rate limit qaydası: saniyədə 1 sorğu

    return None