from geopy.geocoders import Nominatim

class Geocoding:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="my_app")
    def geocode(self, address):
        address = self.geolocator.geocode(address, timeout=10)
        if address is None:
            return None
        return address.latitude, address.longitude
