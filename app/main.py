from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List
from app.geo import geocode_place, get_travel_time_matrix
from app.routing import build_route
from app.discovery import discover_places, explain_route

from app.database import engine, get_db, Base
from app import models, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="DayRoute AI")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "database": str(e)}


@app.post("/places", response_model=schemas.PlaceResponse)
def create_place(place: schemas.PlaceCreate, db: Session = Depends(get_db)):
    db_place = models.Place(**place.model_dump())
    db.add(db_place)
    db.commit()
    db.refresh(db_place)
    return db_place


@app.get("/places", response_model=List[schemas.PlaceResponse])
def list_places(db: Session = Depends(get_db)):
    return db.query(models.Place).all()


@app.post("/discover", response_model=schemas.DiscoveryResponse)
def discover_city(request: schemas.CityRequest, db: Session = Depends(get_db)):
    city_name = request.city.strip().lower()

    cached = db.query(models.City).filter(models.City.name == city_name).first()
    if cached:
        data = cached.discovered_places
        return {
            "city": request.city,
            "places": data["places"],
            "travel_matrix": data["travel_matrix"],
        }

    try:
        places = discover_places(request.city)
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))

    for place in places:
        coords = geocode_place(place["name"], request.city)
        if coords:
            place["lat"] = coords["lat"]
            place["lon"] = coords["lon"]
        else:
            place["lat"] = None
            place["lon"] = None

    valid_places = [p for p in places if p["lat"] is not None]
    coordinates = [{"lat": p["lat"], "lon": p["lon"]} for p in valid_places]
    travel_matrix = get_travel_time_matrix(coordinates) if len(coordinates) >= 2 else []

    cache_data = {"places": places, "travel_matrix": travel_matrix}
    new_city = models.City(name=city_name, discovered_places=cache_data)
    db.add(new_city)
    db.commit()

    return {"city": request.city, "places": places, "travel_matrix": travel_matrix}

class RouteRequest(schemas.BaseModel):
    city: str
    time_limit_minutes: int


@app.post("/route/generate")
def generate_route(request: RouteRequest, db: Session = Depends(get_db)):
    if request.time_limit_minutes < 30:
        raise HTTPException(status_code=400, detail="Vaxt limiti minimum 30 dəqiqə olmalıdır")

    city_name = request.city.strip().lower()
    cached = db.query(models.City).filter(models.City.name == city_name).first()

    if not cached:
        raise HTTPException(status_code=404, detail="Əvvəlcə /discover ilə bu şəhəri kəşf et")

    data = cached.discovered_places
    places = data["places"]
    travel_matrix = data["travel_matrix"]

    route = build_route(places, travel_matrix, request.time_limit_minutes)
    explanation = explain_route(
        route["selected"], route["excluded"], route["total_time"], request.time_limit_minutes
    )

    return {
        "city": request.city,
        "selected_places": route["selected"],
        "excluded_places": route["excluded"],
        "total_time_minutes": route["total_time"],
        "time_limit_minutes": request.time_limit_minutes,
        "explanation": explanation,
    }

