import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps





def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function



# Contact API
def lookup(ingredient):
    """Look up quote for ingredient."""
    
    # getting all the meal id for ingredient
    try:  
        url = f"https://www.themealdb.com/api/json/v1/1/filter.php?i={ingredient}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response to get id's
    try:
        mealid = []
        quote = response.json()

        # limit the id's to 7
        # for more than 7 id's
        if len(quote["meals"]) > 7:
            for i in range(7):
                ids = quote["meals"][i]
                id = ids["idMeal"]
                mealid.append(id)

        # for less than 7 id's
        else:
            for i in quote["meals"]:
                id = i["idMeal"]
                mealid.append(id)
    
    except (KeyError, TypeError, ValueError):
        return None

    
    # parse for necessary info
    try:

        meals = []

        # for every id contact API for meal info
        for id in mealid:
            url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={id}"
            response = requests.get(url)
            quoted = response.json()
            mealitems = {
                "name": quoted["meals"][0]["strMeal"],
                "instr": quoted["meals"][0]["strInstructions"],
                "img": quoted["meals"][0]["strMealThumb"],
                "yt": quoted["meals"][0]["strYoutube"],
                "id": quoted["meals"][0]["idMeal"]
            
            }
            meals.append(mealitems)
        
        return meals
    except (KeyError, TypeError, ValueError):
        return None
    

def lookup_id(id):

    try:
        url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={id}"
        response = requests.get(url)
        quoted = response.json()
        recipeinfo = {
            "name": quoted["meals"][0]["strMeal"],
            "instr": quoted["meals"][0]["strInstructions"],
            "img": quoted["meals"][0]["strMealThumb"],
            "yt": quoted["meals"][0]["strYoutube"],
            "id": quoted["meals"][0]["idMeal"]
        }
        return recipeinfo
    except (KeyError, TypeError, ValueError):
        return None
        


