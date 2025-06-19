import datetime
import json
import logging
from typing import AnyStr

from project_sys import PATH_HOME
from src.utils import operation_filter, user_settings_read

path_ = f"{PATH_HOME}/logs/views.log"
logger = logging.getLogger("views")
file_handler = logging.FileHandler(path_, "w", encoding="utf-8")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def greetings() -> str:
    """Функция приветствия в зависимости от времени суток
    «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи»"""

    try:
        legend_s = " Функция: greetings -> "
        logger.info(f"{legend_s} Получает данные о текущем времени")
        current_date_time = datetime.datetime.now()
        current_hours = int(current_date_time.hour)
        greeting = "Доброй ночи"
        if 5 < current_hours < 12:
            greeting = "Добрый утро"
        if 11 < current_hours < 19:
            greeting = "Добрый день"
        if 17 < current_hours:
            greeting = "Добрый вечер"
        return greeting
    except ValueError as eror:
        logger.critical(f"{legend_s}Критическая ошибка: {eror}")
        return "Ошибка запроса времени"


def for_each_card(transactions: list, cashback_rate: float = 100) -> list:
    """Функция возвращающая список словорей по каждой карте(последние 4 цифры карты; общая сумма расходов;
    кешбэк (1 рубль на каждые установленое значение в переменной cashback_rate ))"""

    try:
        legend_s = " Функция: or_each_card -> "
        logger.info(f"{legend_s} Обработка списка словарей")
        each_card = []
        cards = []
        for transaction in transactions:
            if isinstance(transaction["Номер карты"], str):
                each_card.append(transaction["Номер карты"])
        transactions_unicom = set(each_card)
        for card_unicom in transactions_unicom:
            cashback = 0.0
            transactions_sum_expenses = 0.0
            card_num = card_unicom[-4:]
            for transactions_one in transactions:
                if transactions_one["Номер карты"] == card_unicom:
                    transaction_n = float(transactions_one["Сумма платежа"])
                    if transaction_n < 0:
                        transactions_sum_expenses += abs(transaction_n)
            cashback += round(transactions_sum_expenses / cashback_rate, 2)
            my_dict = {
                "last_digits": card_num,
                "total_spent": round(transactions_sum_expenses, 2),
                "cashback": round(cashback, 2),
            }
            cards.append(my_dict)
            logger.info(f"{legend_s} Обработка списка словарей выполнена успешно")
        return cards
    except Exception as eror:
        logger.critical(f"{legend_s}Критическая ошибка: {eror}")
        return []


def top_transactions_amount(transactions: list) -> list:
    """Функция выводит Топ-5 транзакций по сумме платежа."""

    try:
        legend_s = " Функция: top_transactions_amount -> "
        logger.info(f"{legend_s} Обработка списка словарей")
        top_transactions = []
        sorted_transactions = sorted(
            transactions, key=lambda x: x["Сумма платежа"], reverse=True
        )
        sorted_top_5 = sorted_transactions[:5]
        for top_n in sorted_top_5:
            my_dict = {
                "date": top_n["Дата операции"],
                "amount": top_n["Сумма операции"],
                "category": top_n["Категория"],
                "discription": top_n["Описание"],
            }
            top_transactions.append(my_dict)
        logger.info(f"{legend_s} Обработка списка словарей выполнена успешно")
        return top_transactions
    except Exception as eror:
        logger.critical(f"{legend_s}Критическая ошибка: {eror}")
        return []


def list_currencies_user(currencies_user: list) -> list:
    """Функция возвращает словарь с курсами валют, на основе пользовательских настроек через запрос API"""

    try:
        legend_s = " Функция: list_currencies_use -> "
        logger.info(f"{legend_s} Обработка словаря курса валют")
        current_rates = []
        xxx = {"USD": "78.49", "EUR": "90.14"}
        for currencies in currencies_user["user_currencies"]:
            curr = {"currency": currencies, "rate": xxx[currencies]}
            current_rates.append(curr)
        logger.info(f"{legend_s} Обработка словаря выполнена успешно")
        return current_rates
    except Exception as eror:
        logger.critical(f"{legend_s}Критическая ошибка: {eror}")
        return []


def list_stock_user(currencies_user: list[AnyStr]) -> list:
    """Функция возвращает словарь с курсами акций, на основе пользовательских настроек через запрос API"""

    try:
        legend_s = " Функция: list_stock_user -> "
        logger.info(f"{legend_s} Обработка словаря курса акций")
        stock_rates = []
        xxx = {
            "AAPL": "150.12",
            "AMZN": "3173.18",
            "GOOGL": "2742.39",
            "MSFT": "296.71",
            "TSLA": "1007.08",
        }
        for currencies in currencies_user["user_stocks"]:
            # Блок получения курса акций
            stock = {"stock": currencies, "price": xxx[currencies]}
            stock_rates.append(stock)
        logger.info(f"{legend_s} Обработка словаря выполнена успешно")
        return stock_rates
    except Exception as eror:
        logger.critical(f"{legend_s}Критическая ошибка: {eror}")
        return []


def views(date_taim: str) -> str:
    """функция принимает дату в формате Приветствие в формате:YYYY-MM-DD HH:MM:SS и возвращает
    приветствие в зависимости от текущего времени,
    По каждой карте: последние 4 цифры карты; общая сумма расходов; кешбэк (1 рубль на каждые 100 рублей).
    Топ-5 транзакций по сумме платежа.
    Курс валют.
    Стоимость акций из S&P500."""

    try:
        legend_s = " Функция: views -> "
        logger.info(f"{legend_s} Обработка основной логики")
        greet: str
        transactions_period = operation_filter(date_taim)
        greet = greetings()
        for_each = for_each_card(transactions_period)
        top_transactions = for_each_card(transactions_period)
        sss_json = user_settings_read()
        list_currencies = list_currencies_user(sss_json)
        list_stock = list_stock_user(sss_json)
        views_date = {
            "greeting": greet,
            "cards": for_each,
            "top_transactions": top_transactions,
            "currency_rates": list_currencies,
            "stock_price": list_stock,
        }
        views_date_json = json.dumps(views_date, ensure_ascii=False)
        logger.info(f"{legend_s} Обработка основной логики выполнена успешна.")
        return views_date_json
    except Exception as eror:
        logger.critical(f"{legend_s}Критическая ошибка: {eror}")
        return ""


if __name__ == "__main__":
    print("-------------------------")
    list_stock_user(user_settings_read())
