def map_price_to_yelp(price_str: str) -> str:
    mapping = {'$': '1', '$$': '2', '$$$': '3', '$$$$': '4'}
    return ",".join([mapping.get(p.strip()) for p in price_str.split(",") if mapping.get(p.strip())])

def map_cuisine_to_yelp_category(cuisine: str) -> str:
    mapping = {
        "Italian": "italian", "Japanese": "japanese", "French": "french",
        "Steakhouse": "steak", "Indian": "indpak", "Thai": "thai",
        "Mexican": "mexican", "Middle Eastern": "mideastern", "Chinese": "chinese"
    }
    return mapping.get(cuisine, "")

def map_ambiance_to_term(ambiance: str) -> str:
    mapping = {
        "Quiet": "quiet", "Trendy": "trendy", "Romantic": "romantic",
        "Rooftop": "rooftop", "Patio": "patio", "Classic": "classic"
    }
    return mapping.get(ambiance, "")

def map_distance_to_radius_km(distance_str: str) -> int:
    mapping = {
        "Within 1 km": 1000, "Within 2 km": 2000,
        "Within 5 km": 5000, "Walking Distance (<15 mins)": 1200
    }
    return mapping.get(distance_str, 2000)

def map_liked_by_to_yelp(liked_by_str: str) -> str:
    mapping = {
        "Young Professionals": "liked_by_young_professionals",
        "Travelers": "liked_by_travelers",
        "Wine Lovers": "liked_by_wine",
        "Beer Lovers": "liked_by_beer"
    }
    return mapping.get(liked_by_str, "")

def format_liked_by_for_display(yelp_liked_by_key: str) -> str:
    mapping = {
        "liked_by_young_professionals": "Popular with Young Professionals",
        "liked_by_travelers": "Popular with Travelers",
        "liked_by_wine": "Loved by Wine Lovers",
        "liked_by_beer": "Loved by Beer Lovers"
    }
    return mapping.get(yelp_liked_by_key, "")
