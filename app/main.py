import subprocess
import threading
import time
from app.common.logger import get_logger
from app.config.settings import settings
from app.common.custom_exception import CustomException

from dotenv import load_dotenv
logger = get_logger(__name__)
load_dotenv()

def run_backend():
    try:
        logger.info("Starting backend API service...")
        subprocess.run(["uvicorn", "app.backend.api:app", "--host", "127.0.0.1", "--port", "9999"], check=True)

    except CustomException as e:
        logger.error(f"Failed to start backend API service: {e}")
        raise CustomException("Backend service failed to start.") from e

def run_frontend():
    try:
        logger.info("Starting frontend UI service...")
        subprocess.run(["streamlit", "run", "app/frontend/ui.py", "--server.port", "8501"], check=True)

    except CustomException as e:
        logger.error(f"Failed to start frontend UI service: {e}")
        raise CustomException("Frontend service failed to start.") from e

if __name__ == "__main__":
    try:
        backend_thread = threading.Thread(target=run_backend)
        backend_thread.start()
        time.sleep(5)  # Ensure backend starts before frontend

        run_frontend()
    except CustomException as e:
        logger.exception(f"An error occurred: {e}")


