# Recipe Recommender

A project that fetches recipes from an API (e.g., Spoonacular) and stores them in a PostgreSQL database. The recipes are then indexed for fast similarity search using **Pinecone** (optional). This project demonstrates basic integration with APIs, databases, and vector search.

## Features

- Fetches recipes from Spoonacular API.
- Stores recipes in a PostgreSQL database.
- (Optional) Uses Pinecone for vector-based recipe recommendations.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/recipe-recommender.git
   cd recipe-recommender

# Conda Env

    conda create --name recipe-recommender python=3.10
    conda activate recipe-recommender

## Install Dependencies

    pip install -r requirements.txt
