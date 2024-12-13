# hotels_crawler/spiders/hotels_crawler.py
import scrapy
import json
import re
from hotels_crawler.items import HotelItem
from pathlib import Path

class NewHotelSpider(scrapy.Spider):
    name = "hotels_crawler"

    # Starting URL to begin the crawling process
    def start_requests(self):
        start_url = "https://uk.trip.com/hotels/?locale=en-GB&curr=GBP"
        
        # Custom headers to mimic a real browser request
        headers = {
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        
        # Initiating the first request to the start URL with custom headers
        yield scrapy.Request(start_url, headers=headers, callback=self.parse_locations)

    def parse_locations(self, response):
        # Extracting the JavaScript variable that contains hotel data from the webpage
        script_text = response.xpath('//script[contains(text(), "window.IBU_HOTEL")]/text()').get()

        try:
            # Using regex to extract the JSON data embedded in the JavaScript variable
            json_data = re.search(r'window\.IBU_HOTEL\s*=\s*(\{.*?\});', script_text, re.DOTALL).group(1)
            data = json.loads(json_data)  # Parsing the extracted JSON string into a Python dictionary
        except (AttributeError, json.JSONDecodeError) as e:
            # Logging an error if the JSON parsing fails
            self.log(f"Error parsing JSON data: {e}")
            return

        # Iterating over the different city groups (inbound and outbound cities)
        for city_group in ['inboundCities', 'outboundCities']:
            if city_group in data['initData']['htlsData']:
                for city in data['initData']['htlsData'][city_group]:
                    if city['type'] == "City":  # Ensure we're only processing city entries
                        if 'recommendHotels' in city:
                            for hotel in city['recommendHotels']:
                                # Extracting relevant hotel data and yielding it as an item
                                hotel_item = HotelItem(
                                    title=hotel['hotelName'],  # Hotel name
                                    rating=hotel.get('rating', 'N/A'),  # Hotel rating (default to 'N/A' if not available)
                                    location=city['cityUrl'],  # URL for the city (used as a reference)
                                    latitude=hotel.get('lat', 'N/A'),  # Latitude of the hotel (default to 'N/A' if not available)
                                    longitude=hotel.get('lon', 'N/A'),  # Longitude of the hotel (default to 'N/A' if not available)
                                    room=[amenities['name'] for amenities in hotel.get('hotelFacilityList', [])],  # Amenities available in the hotel
                                    price=hotel.get('displayPrice', {}).get('price', 'N/A'),  # Price of the hotel (default to 'N/A' if not available)
                                    img_src_list=f"https://ak-d.tripcdn.com/images{hotel.get('imgUrl', '')}"  # Image URL for the hotel
                                )
                                
                                # Printing the hotel data to the console (for debugging purposes)
                                self.log(f"Scraped Hotel Data: {hotel_item}")
                                
                                # Yield the hotel item to be processed further (e.g., saved to a database or file)
                                yield hotel_item

    # This method will be called when the spider is closed
    def close(self, reason):
        # Log the reason for the spider closure
        self.log("Spider closed: " + reason)
