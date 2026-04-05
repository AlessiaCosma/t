from utils.geocoding import Geocoding
from utils.currency_converter import currency_converter

class HotelService:
    def __init__(self, client):
        self.client = client
        self.geocoder = Geocoding()
        self.mock_hotel = {
            "name_list": ["Hotel Demo 1", "Hotel Demo 2"],
            "price_list": [120.0, 150.0],
            "contact_list": ["+40123456789", None],
            "price": 135.0,
            "hotels_found": 2,
            "room_description": ['Prepay Non-refundable, prepay in full, non-refundable Deluxe King Room, 1 King', 'ADVANCE SAVER-Room only Room for 1 or 2 persons'],
            "room_category": ['DELUXE_ROOM', 'STANDARD_ROOM'],
            "bed_type": ['DOUBLE', None],
            "bed_number": [1, None],
        }

    def get_hotel_info(self, check_in, check_out, address, price_range=None,  ratings=None, adults=1, currency="EUR",
                       room_quantity=None, board_type=None, radius=5):
        """
        This method attempts to convert the given address into geographic coordinates
        using a geocoding service. If successful, it searches for hotels using the
        geographic location; otherwise, it falls back to searching by city name.

        Args:
            check_in (str): Check-in date in YYYY-MM-DD format.
            check_out (str): Check-out date in YYYY-MM-DD format.
            address (str): Location of the hotel (city, address, or place name).
            price_range (str | None): Desired price range for hotels (optional).
            ratings (list[int] | int | None): Desired hotel star ratings (optional).
            adults (int): Number of adult guests. Default is 1.
            currency (str): Currency code for hotel prices (e.g., "EUR").
            radius (int): Search radius in kilometers around the given location. Default is 5 km.
            room_quantity (int | None): Number of rooms required.
            board_type (str | None): Type of board (meal plan) for the hotel stay.
                Possible values may include: "ROOM_ONLY", "BED_AND_BREAKFAST", "HALF_BOARD", "FULL_BOARD", "ALL_INCLUSIVE"
                If None, no filtering based on board type is applied.

        Returns:
            dict | None:
                - dict: A dictionary containing:
                    - "name_list": List of hotel names
                    - "price_list": List of hotel prices
                    - "contact_list": List of contact phone numbers (0 if unavailable)
                    - "price": Average price of the found hotels
                    - "hotels_found": Total number of hotels found
                    - "room_description": Room descriptions
                    - "room_category": Room categories
                    - "bed_type": Bed types (if available)
                    - "bed_number": Number of beds (if available)
                - None: If no results are found or the API request fails.
        """
        new_address = self.geocoder.geocode(address)
        if new_address is not None:
            try:
                result = self.client.get_hotels(check_in=check_in, check_out=check_out, geocode=new_address,
                                                    price_range=price_range, ratings=ratings, adults=adults, currency=currency,
                                                    room_quantity=room_quantity, board_type=board_type, radius=radius)

            except KeyError:
                result = self.client.get_hotels(check_in=check_in, check_out=check_out, city_name=address,
                                              price_range=price_range, ratings=ratings, adults=adults, currency=currency,
                                              room_quantity=room_quantity, board_type=board_type, radius=radius)

        else:
            result = self.client.get_hotels(check_in=check_in, check_out=check_out, city_name=address,
                                          price_range=price_range, ratings=ratings, adults=adults, currency=currency,
                                          room_quantity=room_quantity, board_type=board_type, radius=radius)
        if result is None:
            return self.mock_hotel
        else:
            info, room = result
            return self.format_result(info, room, currency)

    @staticmethod
    def format_result(info, rooms, currency):
        """
        Formats raw hotel data into a structured and user-friendly format.
        """

        information = {
            "name_list": [],
            "price_list": [],
            "contact_list": [],
            "price": 0.0,
            "hotels_found": 0,
            "room_description": [],
            "room_category": [],
            "bed_type": [],
            "bed_number": [],
        }
        for room in rooms:
            if room is not None:
                information["room_description"].append(' '.join(room[0].split()))
                information["room_category"].append(' '.join(room[1].split()))
                information["bed_type"].append(' '.join(room[2].split()) if len(room) > 2 else None)
                information["bed_number"].append(room[3] if len(room) > 2 else None)
            else:
                information["room_description"].append(None)
                information["room_category"].append(None)
                information["bed_type"].append(None)
                information["bed_number"].append(None)


        for hotel in info:
            information["name_list"].append(hotel[0])
            if hotel[2] == currency:
                information["price_list"].append(float(hotel[1]))
            else:
                price = float(hotel[1])
                new_price = currency_converter(price, hotel[2], currency)
                if new_price is not None:
                    price = new_price
                information["price_list"].append(price)
            information["contact_list"].append(hotel[3] if len(hotel) > 3 else None)
        if not information["price_list"]:
            return None
        information["price"] = round(sum(information["price_list"])/len(information["price_list"]),2)
        information["hotels_found"] = len(information["price_list"])
        return information
