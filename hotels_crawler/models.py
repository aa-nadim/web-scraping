# hotels_crawler/models.py

# Import necessary components from SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

# Create a base class for model definition
Base = declarative_base()

# Define the Hotel model class, which represents the 'hotels' table in the database
class Hotel(Base):
    # Define the table name in the database
    __tablename__ = 'hotels'

    # Define columns for the 'hotels' table
    id = Column(Integer, primary_key=True)  # Primary key for the hotel, will be set to hotel_id
    property_title = Column(String)  # The name or title of the hotel (text field)
    hotel_id = Column(Integer, unique=True)  # External hotel identifier
    image = Column(String)  # The image URL of the hotel
    rating = Column(Float)  # The rating of the hotel (floating-point number)
    room_type = Column(String)  # Room type (text field)
    price = Column(Float)  # Price of the hotel (floating-point number, representing the cost)
    address = Column(String)  # The address of the hotel
    latitude = Column(Float)  # Latitude of the hotel's location (floating-point number)
    longitude = Column(Float)  # Longitude of the hotel's location (floating-point number)
    city_name = Column(String)  # The name of the city where the hotel is located