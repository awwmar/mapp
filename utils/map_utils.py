import folium
from folium import plugins
from typing import List, Dict, Tuple, Optional
import branca.colormap as cm
from streamlit_folium import folium_static
import streamlit as st

def create_base_map(center_lat: float = 0, center_lon: float = 0, zoom_start: int = 2) -> folium.Map:
    """Create a base map with OpenStreetMap tiles."""
    return folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom_start,
        tiles='OpenStreetMap',
        control_scale=True
    )

def add_location_marker(
    m: folium.Map,
    lat: float,
    lon: float,
    popup: str = "",
    color: str = "red",
    icon: str = "info-sign"
) -> folium.Map:
    """Add a marker to the map."""
    folium.Marker(
        location=[lat, lon],
        popup=popup,
        icon=folium.Icon(color=color, icon=icon)
    ).add_to(m)
    return m

def add_location_circle(
    m: folium.Map,
    lat: float,
    lon: float,
    radius: float,
    color: str = "blue",
    fill: bool = True,
    popup: str = ""
) -> folium.Map:
    """Add a circle to the map."""
    folium.Circle(
        location=[lat, lon],
        radius=radius,
        color=color,
        fill=fill,
        popup=popup
    ).add_to(m)
    return m

def add_heatmap(
    m: folium.Map,
    data: List[Tuple[float, float, float]],
    radius: int = 15,
    blur: int = 10,
    max_zoom: int = 10
) -> folium.Map:
    """Add a heatmap layer to the map."""
    plugins.HeatMap(
        data,
        radius=radius,
        blur=blur,
        max_zoom=max_zoom
    ).add_to(m)
    return m

def add_polyline(
    m: folium.Map,
    locations: List[Tuple[float, float]],
    color: str = "blue",
    weight: int = 2,
    opacity: float = 0.8
) -> folium.Map:
    """Add a polyline to the map."""
    folium.PolyLine(
        locations,
        color=color,
        weight=weight,
        opacity=opacity
    ).add_to(m)
    return m

def add_location_history(
    m: folium.Map,
    history: List[Dict],
    color: str = "blue",
    weight: int = 2,
    opacity: float = 0.8
) -> folium.Map:
    """Add location history as a polyline with markers."""
    if not history:
        return m
    
    # Create polyline
    locations = [(point['latitude'], point['longitude']) for point in history]
    add_polyline(m, locations, color, weight, opacity)
    
    # Add markers for start and end points
    start_point = history[0]
    end_point = history[-1]
    
    add_location_marker(
        m,
        start_point['latitude'],
        start_point['longitude'],
        popup=f"Start: {start_point['timestamp']}",
        color="green",
        icon="play"
    )
    
    add_location_marker(
        m,
        end_point['latitude'],
        end_point['longitude'],
        popup=f"End: {end_point['timestamp']}",
        color="red",
        icon="stop"
    )
    
    return m

def add_nearby_places(
    m: folium.Map,
    places: List[Dict],
    category_colors: Dict[str, str] = None
) -> folium.Map:
    """Add nearby places as markers with category-based colors."""
    if category_colors is None:
        category_colors = {
            'restaurant': 'red',
            'cafe': 'orange',
            'bar': 'purple',
            'hotel': 'blue',
            'shop': 'green',
            'default': 'gray'
        }
    
    for place in places:
        color = category_colors.get(place.get('category', 'default'), 'gray')
        popup = f"""
            <b>{place.get('name', 'Unknown')}</b><br>
            Category: {place.get('category', 'Unknown')}<br>
            Distance: {place.get('distance', 'Unknown')}m
        """
        
        add_location_marker(
            m,
            place['latitude'],
            place['longitude'],
            popup=popup,
            color=color
        )
    
    return m

def display_map(m: folium.Map, height: int = 600):
    """Display the map in Streamlit."""
    folium_static(m, height=height)

def create_geoguesser_map(
    target_lat: float,
    target_lon: float,
    guess_lat: float,
    guess_lon: float,
    distance: float
) -> folium.Map:
    """Create a map for the GeoGuesser game showing target and guess locations."""
    m = create_base_map(
        center_lat=(target_lat + guess_lat) / 2,
        center_lon=(target_lon + guess_lon) / 2,
        zoom_start=4
    )
    
    # Add target location
    add_location_marker(
        m,
        target_lat,
        target_lon,
        popup="Target Location",
        color="red",
        icon="flag"
    )
    
    # Add guess location
    add_location_marker(
        m,
        guess_lat,
        guess_lon,
        popup=f"Your Guess (Distance: {distance:.2f} km)",
        color="blue",
        icon="user"
    )
    
    # Add line between points
    add_polyline(
        m,
        [(target_lat, target_lon), (guess_lat, guess_lon)],
        color="gray",
        weight=2,
        opacity=0.5
    )
    
    return m 