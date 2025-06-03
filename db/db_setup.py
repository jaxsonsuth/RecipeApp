import psycopg2

db_params = {
    'dbname': 'recipe_db',   # Your PostgreSQL database name
    'user': 'jacksonsutherland',      # Your PostgreSQL user
    'host': 'localhost'      # Change to your host if using remote DB
}

# Establish a connection to the database
try:
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    print("Connected to the database.")
except Exception as e:
    print(f"Error: {e}")
    exit(1)

def create_tables():
    create_recipe_table = """
    CREATE TABLE IF NOT EXISTS recipes (
        recipe_id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        image TEXT,
        ready_in_minutes INTEGER,
        servings INTEGER,
        source_url TEXT,
        price_per_serving DECIMAL,
        vegan BOOLEAN,
        vegetarian BOOLEAN,
        gluten_free BOOLEAN,
        dairy_free BOOLEAN,
        spoonacular_score DECIMAL
    );
    """
    create_ingredient_table = """
    CREATE TABLE IF NOT EXISTS ingredients (
        ingredient_id SERIAL PRIMARY KEY,
        recipe_id INTEGER REFERENCES recipes(recipe_id),
        name TEXT NOT NULL,
        amount DECIMAL,
        unit TEXT
    );
    """
    create_instructions_table = """
    CREATE TABLE IF NOT EXISTS instructions (
        instruction_id SERIAL PRIMARY KEY,
        recipe_id INTEGER REFERENCES recipes(recipe_id),
        step_number INTEGER,
        instruction TEXT
    );
    """

    # Execute the SQL commands to create the tables
    try:
        cur.execute(create_recipe_table)
        cur.execute(create_ingredient_table)
        cur.execute(create_instructions_table)
        conn.commit()
        print("Tables created successfully.")
    except Exception as e:
        print(f"Error creating tables: {e}")
        conn.rollback()

# Run the table creation function
create_tables()

# Close the connection
cur.close()
conn.close()
