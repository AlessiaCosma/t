from bs4 import BeautifulSoup
import lxml
import heapq

class TrainClient:
    def __init__(self):
        # BeautifulSoup / XML
        self.price = 0.30 # RON / km
        self.routes = self.get_routes()
        self.stations = self.get_train_stations()
        self.graph = {}
        self.create_station_graph()

    # BeautifulSoup / XML methods

    @staticmethod
    def get_routes():
        """
        Parses the XML file containing train routes and extracts all route elements.

        Returns:
            list[bs4.element.Tag]:
                A list of XML elements representing train routes.
        """
        with open("data/trenuri-2025-2026_sntfc.xml", "r", encoding="utf-8") as f:
            xml_content = f.read()
        soup = BeautifulSoup(xml_content, "xml")
        return soup.find_all("ElementTrasa")

    def get_train_stations(self):
        """
        Extracts all unique train station names from the available routes.

        Returns:
            set[str]:
                A set containing the names of all valid train stations.
        """
        stations = set()
        for route in self.routes:
            if route.get("TipOprire")!="N":
                origin = route.get("DenStaOrigine", "").strip()
                destination = route.get("DenStaDestinatie", "").strip()
                if origin:
                    stations.add(origin)
                if destination:
                    stations.add(destination)

        return stations

    def create_station_graph(self):
        """
        Builds a graph representation of the train network.

        Each station is treated as a node, and connections between stations
        are stored as edges containing distance (in km) and travel time (in hours).
        """
        for route in self.routes:
            origin = route["DenStaOrigine"].strip()
            destination = route["DenStaDestinatie"].strip()

            km = float(route["Km"]) / 1000 # m->km
            ora_p = float(route["OraP"])
            ora_s = float(route["OraS"])
            if ora_s < ora_p:
                ora_s += 24 * 3600
            time = (ora_s - ora_p) / 3600
            stop = float(route["StationareSecunde"])/3600
            time +=stop

            if origin not in self.graph:
                self.graph[origin] = []
            if destination not in self.graph:
                self.graph[destination] = []

            self.graph[origin].append((destination, km, time))
            self.graph[destination].append((origin, km, time))

    def shortest_distance(self, start, end):
        """
        Calculates the shortest route (by distance) between two stations using Dijkstra's algorithm.

        Args:
            start (str): Name of the departure station.
            end (str): Name of the destination station.

        Returns:
            tuple[float, float] | None:
                - tuple: (distance_in_km, travel_time_in_hours) for the shortest route.
                - None: If one or both stations are invalid or no route exists.
        """
        if start not in self.graph or end not in self.graph:
            print("Oras invalid.")
            return None

        pq = [(0, start, 0)] # (distance, node, time)
        distances = {node: float('inf') for node in self.graph}
        distances[start] = 0

        while pq:
            dist, node, time = heapq.heappop(pq)

            if dist > distances[node]:
                continue

            if node == end:
                return dist, time

            for neighbor, km, hours in self.graph[node]:
                new_dist = dist + km
                new_time = time + hours
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    heapq.heappush(pq, (new_dist, neighbor, new_time))
        return None

    def shortest_time(self, start, end):
        """
        Calculates the fastest route (by travel time) between two stations using Dijkstra's algorithm.

        Args:
            start (str): Name of the departure station.
            end (str): Name of the destination station.

        Returns:
            tuple[float, float] | None:
                - tuple: (distance_in_km, travel_time_in_hours) for the fastest route.
                - None: If one or both stations are invalid or no route exists.
        """
        if start not in self.graph or end not in self.graph:
            return None

        pq = [(0, start, 0)] # (time, node, dist)
        times = {node: float('inf') for node in self.graph}
        times[start] = 0

        while pq:
            time, node, dist = heapq.heappop(pq)

            if time > times[node]:
                continue

            if node == end:
                return dist, time

            for neighbor, km , hours in self.graph[node]:
                new_dist = dist + km
                new_time = time + hours
                if new_time < times[neighbor]:
                    times[neighbor] = new_time
                    heapq.heappush(pq, (new_time, neighbor, new_dist))
        return None
