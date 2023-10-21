
from flask import Flask
from flask import redirect, render_template, request, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.sql import text
from dotenv import load_dotenv
from os import getenv

app = Flask(__name__)
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL')
db = SQLAlchemy(app)

@app.route('/')
def index():
    sql = 'SELECT * FROM recipes'
    result = db.session.execute(text(sql))
    recipes = result.fetchall()
    return render_template('index.html', recipes=recipes)

@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        instructions = request.form['instructions']
        time_used = int(request.form['time_used'])
        sql = text('INSERT INTO recipes(title, description, instructions, time_used) VALUES (:title, :description, :instructions, :time_used)')
        result = db.session.execute(sql, {'title': title, 'description': description, 'total_used': time_use})
        recipe_id = int(result.fetchone()[0])
        db.session.commit()
        flash('Recipe added !!!')
        return redirect(url_for('index'))
    return render_template('recipes/add_recipe.html')
