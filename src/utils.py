import logging

import pandas
import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame

from project_sys import PATH_HOME


path_ = f"{PATH_HOME}/logs/utils.log"
logger = logging.getLogger("utils")
file_handler = logging.FileHandler(path_, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def read_excels(path_file: str) -> DataFrame:
    """Функция принимает путь к файлу в виде строки. И возвращает объект: DataFrame."""

    try:
        legend_s = " Функция: read_excels -> "
        logger.info(f"{legend_s}Принимаем путь к файлу: {path_file}")
        date_freme = pd.read_excel(path_file)
        logger.info(f"{legend_s}Читаем файл: {path_file}")
        return date_freme

    except FileNotFoundError as eror:
        logger.error(f"{legend_s}Ошибка: {eror}")
        return []
    except ValueError as eror:
        logger.error(f"{legend_s}Ошибка: {eror}")
        return []
    else:
        eror = Exception
        logger.critical(f"{legend_s}Критическая ошибка: {eror}")
        return []


def convert_dataf_listd(data_freme: DataFrame) -> list[dict]:
    """Функция конвертирует DataFrame в список словарей"""

    legend_s = " Функция: convert_dataf_listd -> "
    list_dict = []
    lists = {}
    try:
        logger.info(f"{legend_s}Принимаем data_freme для конвертации")
        date_files = data_freme.to_dict("records")
        lists_key = list(date_files[0].keys())
        for dicts in date_files:
            for keys in lists_key:
                lists[keys] = str(dicts[keys])
            list_dict.append(lists)
        logger.info(f"{legend_s}Конвертация закончена успешно")
        return list_dict
    except ValueError as eror:
        logger.error(f"{legend_s}Ошибка: {eror}")
        return []
    else:
        eror = Exception
        logger.critical(f"{legend_s}Критическая ошибка: {eror}")
        return []


