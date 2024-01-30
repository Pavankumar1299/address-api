from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from math import radians, sin, cos, sqrt, atan2


# Create SQLite database and tables
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)

Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI()

# Pydantic model for address input
class AddressCreate(BaseModel):
    name: str
    latitude: float
    longitude: float

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API route to create an address
@app.post("/addresses/")
def create_address(address: AddressCreate, db: Session = Depends(get_db)):
    db_address = Address(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

# API route to get all addresses
@app.get("/addresses/get-list")
def get_adrs_list(db: Session = Depends(get_db)):
    addresses = db.query(Address).all()
    return {"addresses": addresses}

# API route to get addresses within a given distance
@app.get("/addresses/")
def get_addresses_within_distance(
    latitude: float,
    longitude: float,
    distance: float = 1.0,
    db: Session = Depends(get_db)
):
    addresses = db.query(Address).all()
    nearby_addresses = []

    for addr in addresses:
        # Calculate distance using Haversine formula
        distance_km = haversine_distance(
            latitude, longitude, addr.latitude, addr.longitude
        )
        if distance_km <= distance:
            nearby_addresses.append(addr)

    return nearby_addresses

# Function to calculate Haversine distance
def haversine_distance(lat1, lon1, lat2, lon2):

    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    # Differences in coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Calculate the distance
    distance = R * c

    return distance

# API route to update an address
@app.put("/addresses/{address_id}")
def update_adrs(address_id:int,
                update_data: AddressCreate, 
                db: Session = Depends(get_db)):
    db_address = db.query(Address).filter(Address.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(db_address, key, value)

    db.commit()
    db.refresh(db_address)
    return db_address

# API route to remove an address
@app.delete("/addresses/{address_id}")
def delete_address(address_id:int, db: Session = Depends(get_db)):
    db_address = db.query(Address).filter(Address.id == address_id).first()

    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    
    db.delete(db_address)
    db.commit()

    return {"message":"Address deleted successfully"}