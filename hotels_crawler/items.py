# hotels_crawler/items.py
import scrapy

class HotelItem(scrapy.Item):
    # The name of the hotel (e.g., "Hilton London")
    title = scrapy.Field()
    
    # The rating of the hotel (e.g., "4.5 stars"). Defaults to 'N/A' if not available
    rating = scrapy.Field()
    
    # The location of the hotel, typically the city or region where it is located (e.g., "London, UK")
    location = scrapy.Field()
    
    # A list of room amenities offered at the hotel (e.g., "Free WiFi", "Gym", "Swimming Pool")
    room = scrapy.Field()
    
    # The price of the hotel, typically displayed on the website (e.g., "$200 per night")
    price = scrapy.Field()
    
    # A list of image URLs associated with the hotel (e.g., images of the hotel's exterior, rooms, etc.)
    img_src_list = scrapy.Field()
    
    # The actual image URLs to be downloaded. These URLs are usually populated through a pipeline.
    image_urls = scrapy.Field()
    
    # The paths where the images will be saved locally once downloaded (populated by Scrapy's Image Pipeline).
    image_paths = scrapy.Field()
    
    # Latitude of the hotel's location (e.g., 51.5074), can be used for mapping or geographic analysis
    latitude = scrapy.Field()
    
    # Longitude of the hotel's location (e.g., -0.1278), also useful for mapping or geographic analysis
    longitude = scrapy.Field()
