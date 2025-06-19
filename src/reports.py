import logging
import os
from datetime import datetime
from typing import Optional
from dateutil.relativedelta import relativedelta

from project_sys import PATH_HOME
from src.utils import read_excels, PATCH_FILE_EXCEL
import pandas as pd
file = "report1.xlsx"
path_ = f"{PATH_HOME}/logs/reports.log"
logger = logging.getLogger("reports")
file_handler = logging.FileHandler(path_, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)



def report_file(file):
    '''Декоратор принимает имя файла в качестве параметра и записывает в него'''

    try:
        legend_s = " Функция: report_file -> "
        logger.info(f"{legend_s} Декоратор принимает имя файла  ")
        def my_decorator(func):
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                pachs = os.path.join(PATH_HOME, "report", file)
                result.to_excel(pachs, sheet_name='Sheet1', index=False)
                logger.info(f"{legend_s} Запись в файл успешна  ")
                return result
            return wrapper
        return my_decorator
    except Exception as eror:
        logger.critical(f"{legend_s}Критическая ошибка: {eror}")
        return []


def report(func):
    '''Декоратор без входных значений записывает результат в файл report.xlsx'''

    try:
        legend_s = " Функция: report -> "
        logger.info(f"{legend_s} Декоратор записывает в файл данные ")
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            pachs = os.path.join(PATH_HOME, "report", "report.xlsx")
            result.to_excel(pachs, sheet_name='Sheet1', index=False)
            logger.info(f"{legend_s} Запись в файл успешна  ")
            return result
        return wrapper
    except Exception as eror:
        logger.critical(f"{legend_s}Критическая ошибка: {eror}")
        return []


@report_file(file)
@report
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    '''Функция возвращает траты по заданной категории за последние три месяца (от переданной даты).'''

    try:
        legend_s = " Функция: spending_by_category -> "
        logger.info(f"{legend_s} начало сортировки ")
        if  date == None:
            end_date = datetime.now()
        else:
            end_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        start_date = end_date - relativedelta(months=3)
        mask = (pd.to_datetime(transactions["Дата операции"],dayfirst=True) >= start_date) & (pd.to_datetime(transactions["Дата операции"],dayfirst=True) <= end_date)
        df_filtered_0 = transactions[mask]
        mask_2 = (df_filtered_0['Категория'] == category) & (df_filtered_0['Сумма платежа'] < 0)
        df_filtered = df_filtered_0[mask_2]
        logger.info(f"{legend_s} Сортировка успешно завершена ")
        return df_filtered
    except Exception as eror:
        logger.critical(f"{legend_s}Критическая ошибка: {eror}")
        return []


if __name__ == "__main__":
    date_frame = read_excels(PATCH_FILE_EXCEL)
    print(spending_by_category(date_frame, "Переводы", "2018-12-30 15:45:00"))
