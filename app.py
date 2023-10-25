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
       give_rating =float(request.form['give_rating'])
       sql = text('INSERT INTO recipes(title, description, cooking_time, give_rating) VALUES (:title, :description, :cooking_time, :give_rating) RETURNING id')
       result = db.session.execute(sql, {'title': title, 'description': description, 'cooking_time': cooking_time, 'give_rating': give_rating})
       recipe_id = int(result.fetchone()[0])
       db.session.commit()
       flash('Recipe added')
       return redirect(url_for('home'))
    return render_template('add_recipe.html')

@app.route('/recipes', methods=['GET', 'POST'])
def all_recipes():  
    sql = text('SELECT * FROM recipes')
    result = db.session.execute(sql)
    recipes = result.fetchall()
    return render_template('all_recipes.html', recipes=recipes)

@app.route('/recipe/<int:recipe_id>')
def recipe(recipe_id):
    sql = text('SELECT * FROM recipes WHERE id=:recipe_id;')
    result = db.session.execute(sql, {"recipe_id" : recipe_id})
    recipe = result.fetchone()
    db.session.commit()
    return render_template('recipe.html', recipe=recipe)
    
if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)
