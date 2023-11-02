from flask import Flask
from flask import redirect, render_template, request, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.sql import text
from dotenv import load_dotenv
from os import getenv
from werkzeug.urls import url_encode
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
db = SQLAlchemy(app)
# login_manager = LoginManager()
# login_manager.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():

    if request.method == 'POST':
       title = request.form['title']
       description = request.form['description']
       cooking_time = int(request.form['cooking_time'])
       give_rating = int(request.form['give_rating'])
       tot_rating = 1
       sql = text('INSERT INTO recipes(title, description, cooking_time, give_rating, tot_rating) VALUES (:title, :description, :cooking_time, :give_rating, :tot_rating) RETURNING id')
       result = db.session.execute(sql, {'title': title, 'description': description, 'cooking_time': cooking_time, 'give_rating': give_rating, 'tot_rating': tot_rating})
       db.session.commit()
       return redirect(url_for('all_recipes'))
       
    return render_template('add_recipe.html')

@app.route('/recipes')
def all_recipes(): 
 
    sql = text('SELECT * FROM recipes')
    result = db.session.execute(sql)
    recipes = result.fetchall()
    return render_template('all_recipes.html', recipes=recipes)

@app.route('/recipe/<int:recipe_id>', methods=['GET', 'POST'])
def recipe(recipe_id):

    sql = text('SELECT * FROM recipes WHERE id = :recipe_id;')
    result = db.session.execute(sql, {"recipe_id" : recipe_id})
    recipe = result.fetchone()     
    db.session.commit()
    return render_template('recipe.html', recipe=recipe)

@app.route('/rate_recipe/<int:recipe_id>', methods=['GET','POST'])
def rate_recipe(recipe_id):
    
    sql = text('SELECT * FROM recipes WHERE id = :recipe_id;')
    result = db.session.execute(sql, {"recipe_id" : recipe_id})
    recipe = result.fetchone()     
    db.session.commit()
    
    if request.method == 'POST':
    	give_rating = int(request.form['give_rating'])
    	sql = text('UPDATE recipes SET give_rating = :give_rating WHERE id=:recipe.id;')
    	result = db.session.execute(sql, {'give_rating': rate_recipe})
    	db.session.commit()    	
    	return redirect(url_for('recipe', recipe_id=recipe_id))
    
    return render_template('rate_recipe.html', recipe=recipe)
    
@app.route('/add_ingredient/<int:recipe_id>', methods=['GET', 'POST'])
def add_ingredient(recipe_id):

    sql = text('SELECT * FROM recipes WHERE id = :recipe_id;')
    result = db.session.execute(sql, {"recipe_id" : recipe_id})
    recipe = result.fetchone() 
    db.session.commit()

    sql2 = text('SELECT * FROM ingredients WHERE recipe_id=:recipe_id;')
    result2 = db.session.execute(sql2, {"recipe_id": recipe_id})
    ingredients = result2.fetchall()
    
    if request.method == 'POST':
    	ingredient = request.form['ingredient']
    	unit = request.form['unit']
    	amount = request.form['amount']
    	sql3 = text('INSERT INTO ingredients (recipe_id, ingredient, unit, amount) VALUES (:recipe_id, :ingredient, :unit, :amount);')
    	db.session.execute(sql3, {'recipe_id': recipe_id, 'ingredient': ingredient, 'unit': unit, 'amount': amount})
    	db.session.commit()
    	return redirect(url_for('recipe', recipe_id=recipe_id))
    
    return render_template('add_ingredient.html', recipe=recipe, recipe_id=recipe_id, ingredients=ingredients)
        
@app.route('/instructions/<int:recipe_id>/', methods=['GET', 'POST'])
def instructions(recipe_id):
    if request.method == 'POST':
    	instructions = request.form['instructions']
    	sql = text("INSERT INTO instructions (recipe_id, intructions) VALUES (:recipe_id, :instructions;")
    	db.session.execute(sql, {"recipe_id": recipe_id, "instructions": instruction})
    	db.session.commit()
    	return redirect(url_for('recipe', recipe_id=recipe_id))

if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)
