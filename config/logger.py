import sys
import logging

logger = logging.getLogger("api-estoque")

#Serão registrados logs a partir do nível Info
logger.setLevel(logging.INFO)

if not logger.handlers: 

    formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    #Por enquanto, logs registrados apenas no terminal
    #Possível registrar em arquivo com "logging.FileHandler("logs.log")"
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
