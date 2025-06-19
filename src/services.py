import json
import logging
import re

from project_sys import PATH_HOME
from src.utils import operation_filter

path_ = f"{PATH_HOME}/logs/services.log"
logger = logging.getLogger("services")
file_handler = logging.FileHandler(path_, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

def search_for_transfers_to_individuals(transactions:list) -> json:
    '''Функция сервиса «Поиск переводов физическим лицам»'''

    try:
        legend_s = " Функция: search_for_transfers_to_individuals -> "
        logger.info(f"{legend_s} Поиск переводов физическим лицам")
        transactions_filtrs = []
        for recordings in transactions:
            if recordings["Категория"] =="Переводы":
                text = str(recordings["Описание"])
                if re.fullmatch(r'[А-ЯЁ][а-яё]+\s+[А-ЯЁ]{1}[.]', text):
                    transactions_filtrs.append(recordings)
        individuals_json = json.dumps(transactions_filtrs, ensure_ascii=False)
        logger.info(f"{legend_s} Поиск выполнен успешно.")
        return individuals_json
    except Exception as eror:
        logger.critical(f"{legend_s}Критическая ошибка: {eror}")
        return json.dumps([], ensure_ascii=False)


if __name__ == "__main__":
    transactions_period = operation_filter('2021-12-30 15:45:00')
    print("---------------------------------------------------")
    print(search_for_transfers_to_individuals(transactions_period))