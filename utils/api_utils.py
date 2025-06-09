import requests
import os
from typing import Dict, List, Optional, Tuple
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import json
from datetime import datetime
import time

# API Keys (should be in .env file)
GEOAPIFY_KEY = os.getenv("GEOAPIFY_KEY", "")

def get_current_location() -> Optional[Dict]:
    """Get current location using browser geolocation API."""
    # This function will be called from JavaScript in the frontend
    return None

def reverse_geocode(lat: float, lon: float) -> Optional[Dict]:
    """Get address information from coordinates using Nominatim."""
    try:
        geolocator = Nominatim(user_agent="location_services_app")
        location = geolocator.reverse(f"{lat}, {lon}")
        
        if location:
            address = location.raw.get('address', {})
            return {
                'address': location.address,
                'city': address.get('city', address.get('town', '')),
                'state': address.get('state', ''),
                'country': address.get('country', ''),
                'postcode': address.get('postcode', '')
            }
    except Exception as e:
        print(f"Error in reverse geocoding: {e}")
    
    return None

def search_nearby_places(
    lat: float,
    lon: float,
    radius: int = 1000,
    category: str = None
) -> List[Dict]:
    """Search for nearby places using Overpass API."""
    try:
        # Overpass API query
        query = f"""
        [out:json][timeout:25];
        (
          node["amenity"](around:{radius},{lat},{lon});
          node["shop"](around:{radius},{lat},{lon});
          node["leisure"](around:{radius},{lat},{lon});
        );
        out body;
        >;
        out skel qt;
        """
        
        response = requests.get(
            "https://overpass-api.de/api/interpreter",
            params={'data': query}
        )
        
        if response.status_code == 200:
            data = response.json()
            places = []
            
            for element in data.get('elements', []):
                tags = element.get('tags', {})
                place_type = tags.get('amenity', tags.get('shop', tags.get('leisure', 'other')))
                
                if category and place_type != category:
                    continue
                
                place = {
                    'name': tags.get('name', 'Unknown'),
                    'type': place_type,
                    'latitude': element.get('lat'),
                    'longitude': element.get('lon'),
                    'distance': calculate_distance(
                        lat, lon,
                        element.get('lat'),
                        element.get('lon')
                    )
                }
                
                # Add additional details if available
                if 'opening_hours' in tags:
                    place['opening_hours'] = tags['opening_hours']
                if 'phone' in tags:
                    place['phone'] = tags['phone']
                if 'website' in tags:
                    place['website'] = tags['website']
                
                places.append(place)
            
            # Sort by distance
            places.sort(key=lambda x: x['distance'])
            return places
            
    except Exception as e:
        print(f"Error searching nearby places: {e}")
    
    return []

def calculate_distance(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float
) -> float:
    """Calculate distance between two points in meters."""
    return geodesic((lat1, lon1), (lat2, lon2)).meters

def get_route(
    start_lat: float,
    start_lon: float,
    end_lat: float,
    end_lon: float
) -> Optional[Dict]:
    """Get route between two points using OSRM."""
    try:
        url = f"http://router.project-osrm.org/route/v1/driving/{start_lon},{start_lat};{end_lon},{end_lat}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('code') == 'Ok':
                route = data['routes'][0]
                return {
                    'distance': route['distance'],  # meters
                    'duration': route['duration'],  # seconds
                    'geometry': route['geometry']
                }
    except Exception as e:
        print(f"Error getting route: {e}")
    
    return None

def get_random_location() -> Tuple[float, float]:
    """Get a random location for the GeoGuesser game."""
    # This is a simple implementation that returns random coordinates
    # In a real application, you might want to use a more sophisticated approach
    import random
    
    # Generate random coordinates within reasonable bounds
    lat = random.uniform(-60, 70)  # Avoid polar regions
    lon = random.uniform(-180, 180)
    
    return lat, lon

def get_location_details(lat: float, lon: float) -> Optional[Dict]:
    """Get detailed location information using Geoapify."""
    if not GEOAPIFY_KEY:
        return None
    
    try:
        url = "https://api.geoapify.com/v1/geocode/reverse"
        params = {
            'lat': lat,
            'lon': lon,
            'apiKey': GEOAPIFY_KEY,
            'format': 'json'
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('results'):
                result = data['results'][0]
                return {
                    'address': result.get('formatted'),
                    'city': result.get('city'),
                    'state': result.get('state'),
                    'country': result.get('country'),
                    'postcode': result.get('postcode'),
                    'timezone': result.get('timezone', {}).get('name'),
                    'country_code': result.get('country_code')
                }
    except Exception as e:
        print(f"Error getting location details: {e}")
    
    return None

def get_weather_info(lat: float, lon: float) -> Optional[Dict]:
    """Get weather information for a location using OpenWeatherMap API."""
    # Note: This is a placeholder. In a real application, you would need an OpenWeatherMap API key
    return None

def get_timezone_info(lat: float, lon: float) -> Optional[Dict]:
    """Get timezone information for a location."""
    try:
        url = f"https://api.timezonedb.com/v2.1/get-time-zone"
        params = {
            'key': os.getenv('TIMEZONE_API_KEY', ''),
            'format': 'json',
            'by': 'position',
            'lat': lat,
            'lng': lon
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'OK':
                return {
                    'timezone': data.get('zoneName'),
                    'offset': data.get('gmtOffset'),
                    'dst': data.get('dst')
                }
    except Exception as e:
        print(f"Error getting timezone info: {e}")
    
    return None 