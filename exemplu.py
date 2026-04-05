from clients.amadeus_client import AmadeusClient
from services.flight_service import FlightService
from services.hotel_service import HotelService
from services.car_service import CarService
from services.train_service import TrainService

amadeus_client = AmadeusClient() # pentru flight_service si hotel_service

# flight
# Optionale: return_date, adult_number, currency_code, travel_class, nonstop

flight_service = FlightService(amadeus_client)
print(flight_service.get_flight_info(original_city="Bucharest", destination_city="Budapest",
                                     departure_date="2026-04-12", return_date="2026-04-14",
                                     adult_number=1, currency_code='EUR', nonstop="true", travel_class= None))

# currency_code: "EUR:, "RON" sau altele
# travel class o valoare (string) din lista:  [ ECONOMY, PREMIUM_ECONOMY, BUSINESS, FIRST ]
# nonstop: "true", "false"


# hotel
# Optionale: price_range, ratings, adults, currency, room_quantity, board_type, radius

hotel_service = HotelService(amadeus_client)
print(hotel_service.get_hotel_info(check_in="2026-05-05", check_out="2026-05-07", address="Bucharest", price_range=None,
                                   ratings=None, adults=1, currency="EUR", room_quantity=None, board_type=None, radius=5))

# currency
# roomQuantity - number of rooms requested
# boardType: ROOM_ONLY = Room Only, BREAKFAST = Breakfast, HALF_BOARD = Diner & Breakfast (only for Aggregators), FULL_BOARD = Full Board (only for Aggregators), ALL_INCLUSIVE = All Inclusive (only for Aggregators)
# radius: default=5
# acum returneaza si room_description, room_category, bed_type si bed_number

# car
# Optionale: car_type, consumption, currency_code

car_service = CarService()
print(car_service.get_car_info(start="Bucharest", end="Suceava", car_type=None, consumption=None, currency_code="RON"))

# consumption: cat consuma masina
# currency code
# acum returneaza si viteza


# train
#
train_service = TrainService()
print(train_service.get_train_info(start="Bucharest", end="Suceava", currency_code="EUR"))

# acum returneaza 2 preturi + viteza medie
# currency code
