from dotenv import load_dotenv

load_dotenv()

from app.bot import run_bot

if __name__ == "__main__":
    run_bot()
