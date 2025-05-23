import requests
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

# Database connection parameters
db_params = {
    'dbname': 'recipe_db',   # Your PostgreSQL database name
    'user': 'jacksonsutherland',      # Your PostgreSQL user
    'host': 'localhost'      # Change to your host if using remote DB
}

# Function to connect to the database
def get_db_connection():
    return psycopg2.connect(**db_params)

# Fetch random recipes from the Spoonacular API
def fetch_recipes():
    API_KEY = os.getenv('SPOONCULAR_API_KEY') 
    API_URL = f'https://api.spoonacular.com/recipes/random?apiKey={API_KEY}&includeNutrition=true&number=5'

    response = requests.get(API_URL)
    
    if response.status_code == 200:
        return response.json()['recipes']
    else:
        print(f"Error fetching recipes: {response.status_code}")
        return []

# Insert recipe data into the database
def insert_recipe(conn, recipe):
    cur = conn.cursor()
    
    # Insert recipe details
    cur.execute(
        """
        INSERT INTO recipes (title, image, ready_in_minutes, servings, source_url, price_per_serving, vegan, vegetarian, gluten_free, dairy_free, spoonacular_score)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING recipe_id
        """,
        (
            recipe['title'],
            recipe['image'],
            recipe['readyInMinutes'],
            recipe['servings'],
            recipe['sourceUrl'],
            recipe['pricePerServing'],
            recipe['vegan'],
            recipe['vegetarian'],
            recipe['glutenFree'],
            recipe['dairyFree'],
            recipe['spoonacularScore']
        )
    )
    recipe_id = cur.fetchone()[0]
    conn.commit()

    # Insert ingredients
    for ingredient in recipe['extendedIngredients']:
        insert_ingredient(conn, recipe_id, ingredient)

    # Insert instructions
    for step in recipe['analyzedInstructions'][0]['steps']:
        insert_instruction(conn, recipe_id, step)

    cur.close()

# Insert ingredients data into the database
def insert_ingredient(conn, recipe_id, ingredient):
    cur = conn.cursor()
    
    cur.execute(
        """
        INSERT INTO ingredients (recipe_id, name, amount, unit)
        VALUES (%s, %s, %s, %s)
        """,
        (
            recipe_id,
            ingredient['name'],
            ingredient['amount'],
            ingredient['unit']
        )
    )
    conn.commit()
    cur.close()

# Insert instruction data into the database
def insert_instruction(conn, recipe_id, step):
    cur = conn.cursor()
    
    cur.execute(
        """
        INSERT INTO instructions (recipe_id, step_number, instruction)
        VALUES (%s, %s, %s)
        """,
        (
            recipe_id,
            step['number'],
            step['step']
        )
    )
    conn.commit()
    cur.close()

# Main function to fetch recipes and insert into the database
def main():
    conn = get_db_connection()

    recipes = fetch_recipes()
    
    if recipes:
        for recipe in recipes:
            insert_recipe(conn, recipe)
            print(f"Inserted recipe: {recipe['title']}")

    conn.close()

if __name__ == "__main__":
    main()
