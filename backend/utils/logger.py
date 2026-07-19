import logging


def configure_logger() -> None:
    """Configure the application logger for structured backend logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


logger = logging.getLogger("nexus_ai")
configure_logger()
