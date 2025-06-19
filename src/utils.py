import datetime
import json
import logging
import os
import pandas as pd
from pandas.core.interchange.dataframe_protocol import DataFrame

from project_sys import PATH_HOME

PATCH_FILE_EXCEL = os.path.join(PATH_HOME, "data", "operations.xlsx")
path_ = f"{PATH_HOME}/logs/utils.log"
logger = logging.getLogger("utils")
file_handler = logging.FileHandler(path_, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def read_excels(path_file: str) -> pd.DataFrame:
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

    try:
        legend_s = " Функция: convert_dataf_listd -> "
        list_dict = []
        logger.info(f"{legend_s}Принимаем data_freme для конвертации")
        date_files = data_freme.to_dict("records")
        for dicts in date_files:
            list_dict.append(dicts)
        logger.info(f"{legend_s}Конвертация закончена успешно")
        return list_dict
    except Exception as eror:
        logger.error(f"{legend_s}Ошибка: {eror}")
        return []

def operation_filter(dates_end:str)-> list:
    ''' Функция принимает на вход строку с датой и временем в формате
        YYYY-MM-DD HH:MM:SS  и возвращает данные с начала месяца, на который
        выпадает входящая дата, по входящую дату.'''


    try:
        legend_s = " Функция: operation_filter -> "
        logger.info(f"{legend_s} Принимаем data_freme для фильтрации по дате")
        data_freim = read_excels(PATCH_FILE_EXCEL)
        print(type(data_freim))
        transaction_date = convert_dataf_listd(data_freim)
        dates_filtr = []
        date_obj = datetime.datetime.strptime(dates_end, "%Y-%m-%d %H:%M:%S")
        # опредилить месяц и дать дату начала фильтрации
        for dates_n in transaction_date:
            time_date = datetime.datetime.strptime(dates_n['Дата операции'], "%d.%m.%Y %H:%M:%S")
            if date_obj.year == time_date.year:
                if date_obj.month == time_date.month:
                    if date_obj.day >= time_date.day:
                        dates_filtr.append(dates_n)
        return dates_filtr
    except Exception as eror:
        logger.error(f"{legend_s}Ошибка: {eror}")
        return []

def user_settings_read(fails:str = 'user_settings.json')->json:
    '''Чтение файла пользовательских настроек по умолчанию: user_settings.json в корневом катологе'''

    try:
        legend_s = " Функция: user_settings_read -> "
        list_dict = []
        logger.info(f"{legend_s} Чтение файла пользовательских настроек")
        path_ = f"{PATH_HOME}/{fails}"
        with open(path_) as f:
            data = json.load(f)
        return data
    except FileNotFoundError as eror:
        logger.critical(f"{legend_s} Ошибка с файлом: {eror}")
        return []
    except Exception as eror:
        logger.error(f"{legend_s}Ошибка: {eror}")
        return []

