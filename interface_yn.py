from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from api import shopping_list_api_endpoints
from flask_cors import CORS  # Import the CORS extension
import requests

# Initialisation of the datebase and the 
db = SQLAlchemy() # db intitialized here
app = Flask(__name__)

CORS(app, origins=['*'])  # Initialize CORS with the Flask app

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db.init_app(app)

# Definition of the database : our list of ingredients 
class Ingredients(db.Model) : 
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self): 
        return '<Task %r>' %self.id


# ######### POST NEW #########    
@app.route('/', methods= ['POST', 'GET'])
def index():
    # if we want to upload a new task 
    if request.method == 'POST': 
        task_content = request.form['content']
        new_task = Ingredients(content=task_content)
        
        try: 
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        
        except: 
            return 'There was an issue adding your task'
    # show the current values in the database
    else : 
        tasks = Ingredients.query.order_by(Ingredients.date_created).all()
        return render_template('index.html', tasks=tasks) 
# no need to specify the name of the folder since we named it "templates"

######### DELETE #########
@app.route('/delete/<int:id>')
def delete(id) : 
    task_to_delete = Ingredients.query.get_or_404(id) 
    try : 
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except : 
        return 'There was a problem deleting our task'
    
######### UPDATE #########
@app.route('/update/<int:id>', methods= ['POST', 'GET'])
def update(id) : 
    task = Ingredients.query.get_or_404(id)
    # if we want to upload the changes
    if request.method == 'POST' : 
        task.content = request.form['content']
        try : 
            db.session.commit()
            return redirect('/')
        except : 
            return "There was an issue updatding your task"
    # if you click on the button update of the home page
    else :
        return render_template('update.html', task=task)
    

########### Get Ingredient list from list of recipe ##########   
@app.route('/get_ingredient', methods=['POST', 'GET'])
def get_ingredient(nb_pers=4, recipe_list=["pizza", "gateau au chocolat"]):
    data = recipe_list
    
    # Endpoint to which the request will be forwarded
    url = shopping_list_api_endpoints
    
    # Headers for the request
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    # Forward the request to the specified URL
    response = requests.post(url,params={'nb_pers':nb_pers}, headers=headers, json=data)
    
    # Return the response back to the client
    return response.json()
        

if __name__ == "__main__" :
    app.run(debug= True)
     