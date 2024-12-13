# Import necessary modules
import os
from hotels_crawler.models import Base, Hotel  # Import database model classes
from scrapy.pipelines.images import ImagesPipeline  # Import Scrapy's built-in image pipeline
from scrapy.exceptions import DropItem  # Exception to discard items
from scrapy import Request  # Request to download images
from sqlalchemy import create_engine  # SQLAlchemy to connect to the database
from sqlalchemy.orm import sessionmaker  # SQLAlchemy session to interact with the database
from config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME  # Database credentials (imported from config file)

# Set up the database URL (PostgreSQL with psycopg2 driver)
# DATABASE_URL = f'postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
DATABASE_URL = f'postgresql+psycopg2://aa_nadim:aa_nadim123@postgres:5432/scraping_db'


class HotelScraperPipeline:
    # This pipeline is responsible for saving hotel data to the database

    def __init__(self):
        # Initialize the pipeline by setting up the database connection
        db_url = DATABASE_URL
        if not db_url:
            raise ValueError("DATABASE_URL not properly configured")  # Raise an error if the database URL is not provided

        # Create an engine to interact with the PostgreSQL database
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)  # Create the necessary tables if they don't exist already
        self.Session = sessionmaker(bind=self.engine)  # Create a sessionmaker to handle database sessions

    def process_item(self, item, spider):
        # Process each item (hotel data) and save it to the database
        session = self.Session()  # Create a new session for this operation
        try:
            # Create a new Hotel object from the scraped item data
            hotel = Hotel(
                country=item.get('country'),
                title=item.get('title'),
                img_src_list=item.get('img_src_list'),
                rating=item.get('rating'),
                room=item.get('room'),
                price=item.get('price'),
                location=item.get('location'),
                latitude=item.get('latitude'),
                longitude=item.get('longitude'),
                image_paths=', '.join(item.get('image_paths', []))  # Store image paths as a comma-separated string
            )

            # Add the new hotel object to the session and commit it to the database
            session.add(hotel)
            session.commit()
        except Exception as e:
            # If there's an error, log the exception and roll back the transaction
            spider.log(f"Failed to process item: {e}")
            session.rollback()
        finally:
            session.close()  # Ensure the session is closed, whether successful or not

        return item  # Return the item after processing

class HotelImagePipeline(ImagesPipeline):
    # This pipeline is responsible for downloading and saving images associated with the hotel

    def get_media_requests(self, item, info):
        # Generate requests for each image URL in the img_src_list field
        for image_url in item.get('img_src_list', '').split(','):
            yield Request(image_url.strip())  # Send a request to download the image

    def item_completed(self, results, item, info):
        # This method is called when image downloads are completed
        # Extract the file paths of the successfully downloaded images
        image_paths = [x['path'] for ok, x in results if ok]

        # If no images were downloaded, drop the item
        if not image_paths:
            raise DropItem("Item contains no images")

        # Save the paths of the downloaded images to the item
        item['image_paths'] = image_paths
        return item  # Return the item with updated image paths
