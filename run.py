import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Debug prints for environment variables
print("HOST:", os.getenv("HOST"))
print("PORT:", os.getenv("PORT"))
print("LOG_LEVEL:", os.getenv("LOG_LEVEL"))

if __name__ == "__main__":
    # Set defaults if environment variables are not set
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    log_level = os.getenv("LOG_LEVEL", "info").lower()

    # Debug print for log level
    print("Log level:", log_level)

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        log_level=log_level,
        reload=True  # Enable hot reload in development
    )