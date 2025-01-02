import logging
from fastapi import FastAPI
from app.routes import router
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import asyncpg
from urllib.parse import urlparse
import os
load_dotenv()
# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set logging level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Logs to console
        logging.FileHandler("app.log", mode="a"),  # Logs to a file
    ],
)
tmpPostgres = urlparse(os.getenv("DATABASE_URL"))
DATABASE_CONFIG = {
    'user': tmpPostgres.username,
    'password': tmpPostgres.password,
    'host': tmpPostgres.hostname,
    'port': 5432,
    "database": "neondb"
}
DATABASE_URL = os.getenv("DATABASE_URL")


app = FastAPI(title="Chatbot Agent")

app.include_router(router)


@app.on_event("startup")
async def startup():
    app.state.db = await asyncpg.create_pool(**DATABASE_CONFIG)

    await db_setup()


@app.on_event("shutdown")
async def shutdown():
    await app.state.db.close()


@app.get("/")
async def root():
    async with app.state.db.acquire() as conn:
        result = await conn.fetchrow("SELECT 'Hello, NeonDB!' AS message;")
        return {"message": result["message"]}
    # return {"message": "Chatbot Agent is running!"}


async def db_setup():
    create_query ='CREATE TABLE IF NOT EXISTS playing_with_neon(id SERIAL PRIMARY KEY, name TEXT NOT NULL, value REAL)'
    
    pass
