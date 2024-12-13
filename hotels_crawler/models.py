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
    id = Column(Integer, primary_key=True)  # Primary key for the hotel (auto-incremented integer)
    country = Column(String)  # The country where the hotel is located (text field)
    title = Column(String)  # The name or title of the hotel (text field)
    img_src_list = Column(String)  # The image URL(s) of the hotel (stored as a string, could be JSON or comma-separated list)
    rating = Column(Float)  # The rating of the hotel (floating-point number)
    room = Column(String)  # Room types or amenities (stored as a string, could be a comma-separated list)
    price = Column(Float)  # Price of the hotel (floating-point number, representing the cost)
    location = Column(String)  # The location or URL of the hotel (text field)
    image_paths = Column(String)  # Path(s) to the image files on disk (stored as a string)
    latitude = Column(Float)  # Latitude of the hotel's location (floating-point number)
    longitude = Column(Float)  # Longitude of the hotel's location (floating-point number)

