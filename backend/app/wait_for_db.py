import logging

from app.db import engine
from sqlalchemy import Engine, text
from sqlalchemy.orm import Session
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init(db_engine: Engine) -> None:
    try:
        with Session(db_engine) as session:
            session.execute(text("SELECT 1"))
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    logger.info("Waiting for database")
    init(engine)
    logger.info("Database ready!")


if __name__ == "__main__":
    main()
