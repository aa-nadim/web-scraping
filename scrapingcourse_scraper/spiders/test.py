import scrapy
import json
import re
import random
import os
import requests


class RandomCityHotelsSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["uk.trip.com"]
    start_urls = ["https://uk.trip.com/hotels/?locale=en-GB&curr=GBP"]

    def parse(self, response):
        # Extract and parse `window.IBU_HOTEL` data
        script_data = response.xpath("//script[contains(text(), 'window.IBU_HOTEL')]/text()").get()
        if script_data:
            # Use regex to extract JSON-like data
            match = re.search(r"window\.IBU_HOTEL\s*=\s*(\{.*?\});", script_data, re.DOTALL)
            if match:
                json_data = match.group(1)
                try:
                    # Parse the JSON data
                    ibu_hotel_data = json.loads(json_data)
                    
                    # Extract `inboundCities` from `initData.htlsData`
                    inbound_cities = ibu_hotel_data.get("initData", {}).get("htlsData", {}).get("inboundCities", [])


                    # Extract `outboundCities` from `initData.htlsData`
                    outbound_cities = ibu_hotel_data.get("initData", {}).get("htlsData", {}).get("outboundCities", [])

                    cities_to_search = [inbound_cities, outbound_cities]

                    random_location_to_search = random.choice(cities_to_search)
                    
                    # Randomly select a city with recommendHotels
                    valid_cities = [
                        city for city in random_location_to_search 
                    ]
                    
                    if not valid_cities:
                        self.logger.warning("No cities with recommend hotels found")
                        return
                    
                    # Randomly select a city
                    selected_city = random.choice(valid_cities)
                    
                    # Extract city details
                    city_name = selected_city.get("name", "Unknown")
                    city_id = selected_city.get("id", "")
                    
                    if not city_id:
                        self.logger.warning(f"No ID found for city: {city_name}")
                        return
                    
                    # Construct city hotels list URL
                    city_hotels_url = f"https://uk.trip.com/hotels/list?city={city_id}"
                    
                    # Yield a request to the city's hotel list page
                    yield scrapy.Request(
                        url=city_hotels_url, 
                        callback=self.parse_city_hotels, 
                        meta={'city_name': city_name}
                    )
                
                except json.JSONDecodeError as e:
                    self.logger.error(f"Failed to parse JSON: {e}")
                except Exception as e:
                    self.logger.error(f"An unexpected error occurred: {e}")

    def parse_city_hotels(self, response):
        # Extract and parse `window.IBU_HOTEL` data from city hotels page
        script_data = response.xpath("//script[contains(text(), 'window.IBU_HOTEL')]/text()").get()
        city_name = response.meta.get('city_name', 'Unknown')
        
        # Create images directory if it doesn't exist
        images_dir = os.path.join(os.getcwd(), 'hotel_images', city_name.lower().replace(' ', '_'))
        os.makedirs(images_dir, exist_ok=True)
        
        if script_data:
            # Use regex to extract JSON-like data
            match = re.search(r"window\.IBU_HOTEL\s*=\s*(\{.*?\});", script_data, re.DOTALL)
            if match:
                json_data = match.group(1)
                try:
                    # Parse the JSON data
                    ibu_hotel_data = json.loads(json_data)
                    
                    # Extract hotel list from initData.firstPageList.hotelList
                    hotel_list = ibu_hotel_data.get("initData", {}).get("firstPageList", {}).get("hotelList", [])
                    
                    # Process and yield each hotel
                    city_hotels = []
                    for hotel in hotel_list:
                        # Extract hotel details
                        hotel_id = hotel.get("hotelBasicInfo", {}).get("hotelId", "")
                        hotel_name = hotel.get("hotelBasicInfo", {}).get("hotelName", "").replace(" ", "_")
                        image_url = hotel.get("hotelBasicInfo", {}).get("hotelImg", "")
                        
                        # Prepare hotel info
                        hotel_info = {
                            "city_name": city_name,
                            "property_title": hotel.get("hotelBasicInfo", {}).get("hotelName", ""),
                            "hotel_id": hotel_id,
                            "price": hotel.get("hotelBasicInfo", {}).get("price", ""),
                            "rating": hotel.get("commentInfo", {}).get("commentScore", ""),
                            "address": hotel.get("positionInfo", {}).get("positionName", ""),
                            "latitude": hotel.get("positionInfo", {}).get("coordinate", {}).get("lat", ""),
                            "longitude": hotel.get("positionInfo", {}).get("coordinate", {}).get("lng", ""),
                            "room_type": hotel.get("roomInfo", {}).get("physicalRoomName", ""),
                            "image": image_url  # Keep original image URL
                        }
                        
                        # Download and save image
                        if image_url:
                            try:
                                # Create a unique filename
                                image_filename = f"{hotel_id}_{hotel_name}.jpg"
                                image_path = os.path.join(images_dir, image_filename)
                                
                                # Download the image
                                response = requests.get(image_url)
                                if response.status_code == 200:
                                    with open(image_path, 'wb') as f:
                                        f.write(response.content)
                                    
                                    # Add local image path (using forward slashes for consistency)
                                    relative_image_path = os.path.join('hotel_images', city_name.lower().replace(' ', '_'), image_filename).replace('\\', '/')
                                    hotel_info['local_image_path'] = relative_image_path
                                    
                                    self.logger.info(f"Saved image for {hotel_name} at {image_path}")
                                else:
                                    self.logger.warning(f"Failed to download image for {hotel_name}")
                            except Exception as e:
                                self.logger.error(f"Error saving image for {hotel_name}: {e}")
                        
                        city_hotels.append(hotel_info)
                        yield hotel_info
                    
                    # Save to a JSON file
                    if city_hotels:
                        output_filename = f"{city_name.lower().replace(' ', '_')}_hotels_list.json"
                        with open(output_filename, "w", encoding="utf-8") as f:
                            json.dump(city_hotels, f, ensure_ascii=False, indent=4)
                        self.logger.info(f"Saved hotels list data for {city_name} to {output_filename}")
                
                except json.JSONDecodeError as e:
                    self.logger.error(f"Failed to parse JSON: {e}")
                except Exception as e:
                    self.logger.error(f"An unexpected error occurred: {e}")