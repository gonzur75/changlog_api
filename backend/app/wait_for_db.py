import logging

from sqlalchemy import text, Engine
from sqlalchemy.orm import Session
from tenacity import retry, stop_after_attempt, wait_fixed, before_log, after_log

from app.db import engine

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
