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
    '''--'''

    transactions_filtrs = []
    for recordings in transactions:
        if recordings["Категория"] =="Переводы":
            text = str(recordings["Описание"])
            if re.fullmatch(r'[А-ЯЁ][а-яё]+\s+[А-ЯЁ]{1}[.]', text):
                #print(text)
                transactions_filtrs.append(recordings)
    individuals_json = json.dumps(transactions_filtrs, ensure_ascii=False)

    return individuals_json


if __name__ == "__main__":
    transactions_period = operation_filter('2021-12-30 15:45:00')
    #ss = 0
    #for transactions in transactions_period:
    #    ss += 1
    #    if ss > 9 :
    #        print(transactions)

    print("---------------------------------------------------")
    wwwww = search_for_transfers_to_individuals(transactions_period)
    print(wwwww)
    #print(search_for_transfers_to_individuals(transactions_period))