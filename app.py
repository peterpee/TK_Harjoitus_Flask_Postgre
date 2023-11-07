from flask import Flask
from flask import redirect, render_template, abort, request, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.sql import text
from dotenv import load_dotenv
from os import getenv
# from werkzeug.urls import url_encode
from werkzeug.security import check_password_hash, generate_password_hash
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

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
       give_rating = float(request.form['give_rating'])
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
    
    	new_rating = int(request.form['give_rating'])
    	sql2 = text('UPDATE recipes SET give_rating = ((SELECT give_rating FROM recipes WHERE id=:recipe_id) + :new_rating) WHERE id=:recipe_id;')
    	db.session.execute(sql2, {'new_rating': new_rating, 'recipe_id': recipe_id})
    	db.session.commit()  
 
    	tot_add = 1
    	sql3 = text('UPDATE recipes SET tot_rating = ((SELECT tot_rating FROM recipes WHERE id=:recipe_id) + :tot_add) WHERE id=:recipe_id;')
    	db.session.execute(sql3, {'tot_add': tot_add, 'recipe_id': recipe_id})
    	db.session.commit()  
    	
    	#sql4 = text('SELECT DIV((SELECT give_rating FROM recipes WHERE id=:recipe_id),(SELECT tot_rating FROM recipes WHERE id=:recipe_id)) AS avg_ratings;')
    	#db.session.execute(sql4, {'recipe_id' : recipe_id})
    	#avg_ratings = result.fetchone()
    	# db.session.commit()
    	
    	sql5 = text('SELECT give_rating::numeric /  tot_rating::numeric FROM recipes WHERE id=:recipe_id;')
    	db.session.execute(sql5, {'recipe_id' : recipe_id})
    	avg_ratings = result.fetchone()
    	
    	sql6 = text('UPDATE recipes SET avg_ratings = :avg_ratings WHERE id=:recipe_id;')
    	db.session.execute(sql6, {'avg_ratings' : avg_ratings, 'recipe_id' : recipe_id})
    	db.session.commit()
    	
    	#sql4 = text('UPDATE recipes SET avg_ratings = (SELECT avg_ratings FROM recipes WHERE id=:recipe_id) WHERE id=:recipe_id);')
    	#db.session.execute(sql4, {'avg_ratings': avg_ratings, 'recipe_id': recipe_id})
    	#db.session.commit()      	 
    	  	
    	return redirect(url_for('recipe', recipe_id=recipe_id))   
    return render_template('rate_recipe.html', recipe=recipe, recipe_id=recipe_id)
    
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
        
@app.route('/add_instruction/<int:recipe_id>/', methods=['GET', 'POST'])
def add_instruction(recipe_id):
    
    sql = text('SELECT * FROM recipes WHERE id = :recipe_id;')
    result = db.session.execute(sql, {"recipe_id" : recipe_id})
    recipe = result.fetchone() 
    db.session.commit()

    sql2 = text('SELECT * FROM instructions WHERE recipe_id=:recipe_id;')
    result2 = db.session.execute(sql2, {"recipe_id": recipe_id})
    instructions = result2.fetchall()
    
    if request.method == 'POST':
    	instruction = request.form['instruction']
    	sql3 = text('INSERT INTO instructions (recipe_id, instruction) VALUES (:recipe_id, :instruction);')
    	db.session.execute(sql3, {'recipe_id': recipe_id, 'instruction': instruction})
    	db.session.commit()
    	return redirect(url_for('recipe', recipe_id=recipe_id))   
    return render_template('add_instruction.html', recipe=recipe, recipe_id=recipe_id, instructions=instructions)

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == "POST":
    	username = request.form['username']
    	password = request.form['password']
  
    	sql = text('SELECT * FROM users WHERE username=:username;')
    	result = db.session.execute(sql, {'username': username})
    	user = result.fetchone()
        
    	if not user:
            flash('No such Username')
            return redirect(url_for('login'))
    	else:
    	    hashed = user.password
    	    if user and check_password_hash(hashed, password):
    	        flash('Cool')
    	        session['username'] = username
    	        return redirect(url_for('home'))
    	    else:
    	        flash('Invalid Password')
    	        return redirect(url_for('login'))
    	        
    return render_template('login.html')    

@app.route('/logout')
def logout():
    del session['username']
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        username = request.form['username']       
        password = request.form['password']
        password_again = request.form['password_again']
        
        sql = text('SELECT username FROM users WHERE username=:username;')
        result = db.session.execute(sql, {'username':username})
        user = result.fetchone()
        
        if user and user._asdict():
            flash('Username taken')
            return render_template('register.html')
        
        if password != password_again:
            flash('Different Passwords')
            return render_template('register.html')
            
        hashed = generate_password_hash(password, method='scrypt')
        sql2 = text('INSERT INTO users (username, password) VALUES (:username, :password);')
        db.session.execute(sql2, {'username':username, 'password':hashed})
        db.session.commit()
        
        return redirect(url_for('login'))
    return render_template('register.html')
    
@app.route('/recipe/<int:recipe_id>/delete', methods=['GET', 'POST'])
def delete_recipe(recipe_id):
    
    sql = text("DELETE FROM ingredients WHERE recipe_id=:recipe_id;")
    db.session.execute(sql, {"recipe_id": recipe_id})

    sql2 = text("DELETE FROM instructions WHERE recipe_id=:recipe_id;")
    db.session.execute(sql2, {"recipe_id": recipe_id})
    
    sql3 = text("DELETE FROM recipes WHERE id=:recipe_id;")
    db.session.execute(sql3, {"recipe_id": recipe_id})
    
    db.session.commit()
    return redirect(url_for('all_recipes'))
    
if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)

