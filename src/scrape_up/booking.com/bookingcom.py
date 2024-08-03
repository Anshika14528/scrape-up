import requests
from bs4 import BeautifulSoup

class BookingScraper:
    """
    A class to scrape data from Booking.com

    Create an instance of `BookingScraper` class

    ```python
    scraper = BookingScraper("London")
    ```

    | Method                   | Details                                                   |
    | ------------------------ | --------------------------------------------------------- |
    | `get_hotels()`           | Returns a list of hotels with their details.              |
    """

    def __init__(self, location):
        self.location = location
        self.url = f"https://www.booking.com/searchresults.html?ss={self.location.replace(' ', '+')}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

    def get_hotels(self):
        response = requests.get(self.url, headers=self.headers)
        if response.status_code != 200:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            return []

        soup = BeautifulSoup(response.content, "html.parser")
        hotels = []

        hotel_elements = soup.find_all("div", {"data-testid": "property-card"})

        if not hotel_elements:
            print("No hotel elements found. The structure of the page may have changed.")
            return hotels

        for hotel in hotel_elements:
            try:
                hotel_name = hotel.find("div", {"data-testid": "title"}).get_text(strip=True) if hotel.find("div", {"data-testid": "title"}) else "No name"
                hotel_reviews = hotel.find("div", {"data-testid": "review-score"}).get_text(strip=True) if hotel.find("div", {"data-testid": "review-score"}) else "No reviews"

                hotels.append({
                    "name": hotel_name,
                    "reviews": hotel_reviews
                })
            except Exception as e:
                print(f"Error parsing hotel: {e}")
                continue

        return hotels


