import psycopg2
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Svelte dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_params = {
    'dbname': 'recipe_db',
    'user': 'jacksonsutherland',
    'host': 'localhost'
}

@app.get("/random_recipe")
async def get_recipe():
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        cur.execute(
            """
            SELECT * 
            FROM recipes
            ORDER BY RANDOM()
            LIMIT 1;
            """
            
        )
        res = cur.fetchall()
        return {"recipes": res}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cur.close()


@app.post("/search_recipe")
async def get_recipe():
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        cur.execute(
            """
            SELECT * 
            FROM recipes;
            """
        )
        res = cur.fetchall()
        return {"recipes": res}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cur.close()
