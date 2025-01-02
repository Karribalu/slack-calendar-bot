import logging
from fastapi import FastAPI
from app.routes import router
from dotenv import load_dotenv

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

app = FastAPI(title="Chatbot Agent")

app.include_router(router)


@app.get("/")
def root():
    return {"message": "Chatbot Agent is running!"}
