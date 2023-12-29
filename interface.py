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
        recipes.append(str(new_recipe))
        print(recipes)
        
    return render_template('homepage.html', recipes=recipes) 

########### Delete one recipe in the home page #############
@app.route('/delete/<int:index_recipe>')
def delete(index_recipe) :
    del recipes[index_recipe]
    return redirect('/')

########### Display the aggregate list of ingredients ##########   
@app.route('/get_ingredient', methods=['POST'])
def get_ingredient():
    
    if request.method == 'POST': 
        
        #---- 1 - RETRIVE THE DATA FORM THE HTML HOME PAGE -----#
        recipe_list = recipes
        print(recipe_list)
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
        ingredients = requests.post(url,params={'nb_pers':nb_pers}, headers=headers, json=recipe_list).json()
        
        print(ingredients)
        
        #----- 4 - DISPLAY THE LIST OF INGREDIENTS ON the HTML INGREDIENTS -----#       
        return render_template('ingredients.html', list_ingredients=ingredients) 
          

if __name__ == "__main__" :
    app.run(debug= True)
     