# The name of the bot, used in the User-Agent string for requests
BOT_NAME = 'hotels_crawler'

# Modules where Scrapy will look for spiders
SPIDER_MODULES = ['hotels_crawler.spiders']

# The module where Scrapy will look for new spider definitions
NEWSPIDER_MODULE = 'hotels_crawler.spiders'

# Robots.txt policy: Set to False to ignore robots.txt rules and scrape all pages
ROBOTSTXT_OBEY = False

# Maximum number of concurrent requests that Scrapy will make (default is 16)
CONCURRENT_REQUESTS = 32  # This will allow Scrapy to make up to 32 concurrent requests

# Disable cookies for all requests (since it's not needed in this case)
COOKIES_ENABLED = False

# Delay between requests to avoid overwhelming the server and to mimic human behavior
DOWNLOAD_DELAY = 3  # 3 seconds delay between each request to avoid being too aggressive

# Randomize the download delay for each request to avoid being detected as a bot
RANDOMIZE_DOWNLOAD_DELAY = True  # Randomizes the delay between requests to make it less predictable

# Enable AutoThrottle to automatically adjust the crawling speed based on server load
AUTOTHROTTLE_ENABLED = True

# Initial download delay before AutoThrottle starts adjusting
AUTOTHROTTLE_START_DELAY = 1  # Start with a 1-second delay for the first request

# Maximum delay between requests when AutoThrottle is active
AUTOTHROTTLE_MAX_DELAY = 10  # Maximum 10 seconds delay if the server is slow

# Target concurrency for AutoThrottle (requests per second)
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0  # Scrapy will aim to send 1 request per second

# Defining the order in which pipelines will be executed
# 'HotelImagePipeline' runs first to handle image downloads, then 'HotelScraperPipeline' to store hotel data
ITEM_PIPELINES = {
   'hotels_crawler.pipelines.HotelImagePipeline': 1,  # First, handle image downloads
   'hotels_crawler.pipelines.HotelScraperPipeline': 300,  # Then, save the hotel data to the database
}

# Directory where the images will be stored after being downloaded
IMAGES_STORE = 'images'  # All downloaded images will be saved in the 'images' folder
