import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db =  SQLAlchemy(app)

@app.route('/')
def index():
    sql = 'SELECT * FROM recipes'
    result = db.session.execute(text(sql))
    recipes = result.fetchall()
    return render_template('index.html', recipes=recipes)

@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if request.method = 'POST':
    	title = request.form['title']
    	description = request.form['description']
    	time_used = int[request.form['time_used']
    	sql = text('INSERT INTO recipes(title, description, time_used')
    	result = db.session.execute(sql, {'title': title, 'description': description, 'total_used': time_use})
        recipe_id = int(result.fetchone()[0])
        db.session.commit()
        flash('Recipe added !!!')
        return redirect(url_for('index')
    return render_template('add_recipe.html')


