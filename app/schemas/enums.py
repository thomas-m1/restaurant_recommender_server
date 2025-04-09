from enum import Enum

class SortByEnum(str, Enum):
    best_match = "best_match"
    highest_rated = "highest_rated"
    popularity = "popularity"
    distance = "distance"

class PriceEnum(str, Enum):
    dollar = "$"
    double_dollar = "$$"
    triple_dollar = "$$$"
    quadruple_dollar = "$$$$"

class MealTagEnum(str, Enum):
    breakfast = "breakfast"
    brunch = "brunch"
    lunch = "lunch"
    dinner = "dinner"
    dessert = "dessert"
    latenight = "latenight"
