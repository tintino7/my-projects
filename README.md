# THARMARAJAN
#### Linkedin :  <https://www.linkedin.com/in/tharmarajan/>
#### Leet code:
It's a web based application for finding recipies by the main ingredient you have in your cupboard.

I used [Meal db API](https://www.themealdb.com/api.php) for the data i needed for this project. It's __free API__ if you want some extra features or you want to make your site publicaly available you have join their supporter.

### Build with
* Flask (python)
* Java script
* Bootstrap 
* css
* html

## Getting started 
If you're a new user you have to register. I used [werkzeug security's](https://werkzeug.palletsprojects.com/en/2.2.x/utils/)  generate_password_hash to create hash while user registering and check_password_hash for checking password while user login.

In the index page we have nav bar at top.
search bar searching recipies by main ingredient.

To search we have to contact API with user input.

### Contacting API

To contact API we have two functions in helpers.py
* lookup

#### lookup

```python
    def lookup(ingredient)
```
This function contact API with user inputed __KEY__ as main ingredient in this url 
```python
 url = f"https://www.themealdb.com/api/json/v1/1/filter.php?i={ingredient}"
 ```
 it will return a dict with a key of "meals" with a list of values
 ```
 {"meals":[{"strMeal":"Chick-Fil-A Sandwich","strMealThumb":"https:\/\/www.themealdb.com\/images\/media\/meals\/sbx7n71587673021.jpg","idMeal":"53016"},{"strMeal":"Chicken Couscous","strMealThumb":"https:\/\/www.themealdb.com\/images\/media\/meals\/qxytrx1511304021.jpg","idMeal":"52850"},{"strMeal":"Chicken Fajita Mac and Cheese","strMealThumb":"https:\/\/www.themealdb.com\/images\/media\/meals\/qrqywr1503066605.jpg","idMeal":"52818"}]}
 ```
 with a use of for loop append all the ids of possible recipes in a list
 ```python
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
```

Then with all the ids find full meal information by contacting this url
```python
url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={id}"
```
return information to calling function in a dict with only necessary information by appending them in a list.
```python
mealitems = {
                "name": quoted["meals"][0]["strMeal"],
                "instr": quoted["meals"][0]["strInstructions"],
                "img": quoted["meals"][0]["strMealThumb"],
                "yt": quoted["meals"][0]["strYoutube"],
                "id": quoted["meals"][0]["idMeal"] 
            }
            meals.append(mealitems)
        
        return meals
``` 
### Quoted
The index route("/) will send the informmation.
In quoted it will show the meals you can cook with the ingredient in __bootstrap__ cards.

For every meal in the list it will create card.
```html
{% for meal in mealinfo %}

  <div class="card bg-dark" style="width: 25rem;">
    <img src="{{ meal['img'] }}" class="card-img-top" alt="meal image">
    <div class="card-body">
      <h5 class="card-title">{{ meal["name"] }}</h5>
      
      <p class="card-text"></p>
      <button type="button" class="btn" id="{{ meal['id'] }}" onclick="addMealDb(this.id)">Save</button>
      <button type="button" class="btn" id="{{ meal['id'] }}" data-toggle="modal" data-target="#dynamicModal" onclick="loadDynamicContent(this.id)">
        View recipe
      </button>
    </div>
  </div>

 {% endfor %}
```
And the view recipe button will open a __popup modal__ is

#### Problem while using bootstrap modal
Even though jinja for loop create modals for every card because of 
```
data-target='#dynamicModal'
```
data-target = #dynamicmodel even you click different card's view recipe button it will always open the first card's model 
##### solution 
I used javascript __fetch__ to add data dynamically to the card and took modal code out of for loop.
```javascript
<script>
 function loadDynamicContent(id) {
    // Retrieve the input data from the form
    
    const data = {"name": id};
    // Send an AJAX POST request to the Flask route with the data
    fetch('/get_dynamic_content', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
        
    })
        .then(response => response.json())
        .then(dynamicContent => {
         console.log(dynamicContent)
            // Update the modal title, body, thumpnail, youtube link  with the received data
            document.getElementById('modalTitle').innerHTML = dynamicContent.title;
            document.getElementById('modalBody').innerHTML = dynamicContent.body;    
            document.getElementById('modalimg').src = dynamicContent.img;
            document.getElementById('modallink').href = dynamicContent.yt;
        })
        .catch(error => console.error(error));
}
```
And i set id of view recipe button to meal's id sent the id as a parameter to this function
```html
 <button type="button" class="btn" id="{{ meal['id'] }}" data-toggle="modal" data-target="#dynamicModal" onclick="loadDynamicContent(this.id)">
        View recipe
      </button>
```
it will fetch from route called __/get_dynamic_content__ .

get_dynamic_content call an fuction in helpers.py called lookup_id
```python
recipeinfo = lookup_id(data['name'])

# Return the dynamic content as JSON
        return jsonify(dynamic_content) 
```
and return the data got from lookup_id __JSON__.

lookup_id function return meal's info by contacting the url with id as prameter.
```python
url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={id}"
```
With the save button you can save meals for later use.

save button triggers the function called __addMealDb__ with  id of the meal as a parameter
```javascript
function addMealDb(id) {
  const mealid = {"id": id};

  fetch('/bookmark_meal', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(mealid)     
    })
        .then(response => response.json())  
        .catch(error => console.error(error));
}
</script>
```
it send the data to a route called __bookmark_meal__.

bookmark_meal call lookup_id to get necessary information add the database table called __meals__.

## Index with saved meals
In index page it will show all the saved meals by just quering the data base with meal's id and calling lookup_id for data.

Index page cards and modal work same as quote.

### profile
The profile section show user information and a button to change password.

it uses the [werkzeug security's](https://werkzeug.palletsprojects.com/en/2.2.x/utils/) generate_password_hash to generate hash and it will rewrite the hash in the table users in data base meals.db.

## Things to improve
* lookup and lookup_id take very long time to load. so i limited the meals to
7 for speed.
* The profile section don't have any use other than change password.
* saved meals only let you remove meals. 













