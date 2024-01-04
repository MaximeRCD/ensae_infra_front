from flask import Flask, render_template, request, redirect
from api import shopping_list_api_endpoints
from flask_cors import CORS  # Import the CORS extension
import requests

# Instantiation of a Flask application
app = Flask(__name__)

# Initialization of CORS with the Flask app
CORS(app, origins=['*'])  

# Initialisation of the dictionnary containning all the recipes
recipes = []

########### Display the home page #############
@app.route('/', methods=['GET', 'POST'])
def homepage():
     
    # Add the new recipe from the html home page
    if request.method == 'POST': 
        new_recipe = request.form['recipe']
        if new_recipe != "" : 
            recipes.append(str(new_recipe))
            
    return render_template('homepage.html', recipes=recipes) 

########### Delete one recipe in the home page #############
@app.route('/delete/<int:index_recipe>')
def delete(index_recipe) :
    del recipes[index_recipe]
    return redirect('/')

########### Display the aggregate list of ingredients ##########   
@app.route('/get_ingredient', methods=['POST'])
def get_ingredient():
    
    # Only if you click to the "Aggregate"
    if request.method == 'POST': 
        
        # Only if the number of person is specified and at least one recipe is specified
        if request.form["nbr_person"] !=  ""  and recipes != []:
            
            #---- 1 - RETRIVE THE DATA FORM THE HTML HOME PAGE -----#
            recipe_list = recipes
            nb_pers = int(request.form["nbr_person"])
            
            #----- 2 - FETCH THE DATA RELATED FROM THE API ------#
            # Endpoint to which the request will be forwarded
            url = shopping_list_api_endpoints
            
            # Headers for the request
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
                        }

            # Forward the request to the specified URL
            ingredients = requests.post(url,
                                        params={'nb_pers':nb_pers},
                                        headers=headers,
                                        json=recipe_list).json()
            
            # Formating the quantity and the unit
            ingredients_f = formating_ingredients(ingredients)
            
            #----- 4 - DISPLAY THE LIST OF INGREDIENTS ON the HTML INGREDIENTS -----#       
            return render_template('ingredients.html', list_ingredients=ingredients_f) 
    
        # Stay on the home page
        else :
            return redirect('/')
        
def formating_ingredients(ingredients : dict) -> dict:
    '''
         This function formats the quantities and units of the 
         aggregates list of ingredients.  
    '''
    
    for ingredient in ingredients : 
        #  Formating the quantity
        ingredient["quantity"] = round(ingredient["quantity"], 2) 
        if int(ingredient["quantity"]) == 0 : 
            ingredient["quantity"] = ""
             
        #  Formating the units
        if ingredient["unit"].lower() == "g" : 
            ingredient["unit"] = "gramme(s)" 
        if ingredient["unit"].lower()  == "kg" : 
            ingredient["unit"] = "kilogramme(s)" 
        if ingredient["unit"].lower()  == "l" : 
            ingredient["unit"] = "litre(s)"
        if ingredient["unit"].lower()  == "cl" : 
            ingredient["unit"] = "centilitre(s)" 
    return ingredients
          
if __name__ == "__main__" :
    app.run(debug= True)
     