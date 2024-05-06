from datetime import datetime
from os import path
import os
import re
import time

class DataValidator:

    @classmethod
    def check_digit(self, val: str | int) -> bool:
        '''
        Вызывается без экземпляра
        Получает - строку или int
        Возвращает - true - значение является числом, иначе false
        '''
        if isinstance(val, int) or isinstance(val, float):
            return True
        if val.isdigit():
            return True
        try:
            val = float(val)
            return True
        except Exception as e:
            print(f"Ошибка {e}")

        return False
    
    @classmethod
    def check_date(self, date: str | int) -> bool:
        '''
        Вызывается без экземпляра
        Получает - строку
        Возвращает - true - значение является датой в нужном формате, иначе false
        '''
        format = r"[0-9]{4}-[0-9]{2}-[0-9]{2}"
        try: 
            date_format = "%Y-%m-%d"
            test_date = datetime.strptime(date, date_format)
            test_datetime = True
        except Exception as e:
            print(f'Ошибка: {e}')
            test_datetime = False
        return re.match(format, date) and test_datetime

class Wallet:

    def __new__(cls):
        print('Вы зашли в кошелек!')
        return super().__new__(cls)
    
    def __init__(self):
        '''
        Если файла с историей нет - создает его, запрашивает начальную сумму кошелька и вносит в класс и файл
        Иначе просто считывает баланс и историю из файла
        '''
        if path.exists('wallet_history.txt'):
            with open('wallet_history.txt', 
                      'r',
                      encoding='utf-8') as file:
                data = file.readlines()
                data = list(
                    map(
                        lambda x: x.replace('\n', ''), 
                        data
                    )
                    )
                
                self.balance = float(data[0])
                self.history = data[1:]
        else:
            with open('wallet_history.txt', 
                      'w', 
                      encoding='utf-8') as file:
                while True:
                    print('Введи начальный баланс: ')
                    balance = input()
                    if not DataValidator.check_digit(balance):
                        print('Введите целое или вещественное число через точку!')
                    else:
                        break
                self.balance = float(balance)
                file.write(balance)
                file.write('\n')
            self.history = []

    def clear(self):
        '''
        Очищает CLI
        '''
        return os.system('cls')

    def _save_changes(self):
        '''
        Сохраняет в файле wallet_history.txt в первой сторе баланс 
        В остальных строках сохраняет записи разделенные пустой строкой
        '''
        with open('wallet_history.txt', 
                  'w', 
                  encoding='utf-8') as file:
            file.write(str(self.balance) + '\n')
            self.history = list(
                map(
                    (lambda x: (x + '\n') if '\n' not in x else x), 
                    self.history
                    )
                )
            file.writelines(self.history)

    def _search_by_category(self, category: str) -> dict:
        '''
        Принимает - категорию в str
        Возвращает - Если данные найдены - словарь, где ключ - id, значение - запись,
        иначе ['NO DATA']
        '''
        response = dict()

        for row, data in enumerate(self.history):
            if (row % 5 != 1 or 
                category.lower() not in data.replace('\n', '').lower()):
                continue

            id = row // 5
            response[id] = [
                self.history[row - 1],
                self.history[row],
                self.history[row + 1],
                self.history[row + 2],
            ]
            
        return response

    def _search_by_money(self, money: float | int) -> dict:
        '''
        Принимает - сумму в float или int
        Возвращает - Если данные найдены - словарь, где ключ - id, значение - запись,
        иначе ['NO DATA']
        '''
        response = dict()

        for row, data in enumerate(self.history):
            if (row % 5 != 2 or 
                str(money) not in data.replace('\n', '')):
                continue

            id = row // 5
            response[id] = [
                self.history[row - 2],
                self.history[row - 1],
                self.history[row],
                self.history[row + 1],
            ]

        return response

    def _search_by_date(self, date: str) -> dict:
        '''
        Принимает - дату в str в формате YYYY-MM-DD
        Возвращает - Если данные найдены - словарь, где ключ - id, значение - запись,
        иначе ['NO DATA']
        '''
        response = dict()

        for row, data in enumerate(self.history):
            if (row % 5 != 0 or 
                date not in data.replace('\n', '')):
                continue

            id = row // 5
            response[id] = [
                self.history[row],
                self.history[row + 1],
                self.history[row + 2],
                self.history[row + 3],
            ]

        return response
    
    def _search_by_description(self, description: str) -> dict:
        '''
        Принимает - текст описания, или части описания, или ключевое слово в str
        Возвращает - Если данные найдены - словарь, где ключ - id, значение - запись,
        иначе ['NO DATA']
        '''
        response = dict()

        for row, data in enumerate(self.history):
            if (row % 5 != 3 or 
                description.lower() not in data.replace('\n', '').lower()):
                continue

            id = row // 5
            response[id] = [
                self.history[row - 3],
                self.history[row - 2],
                self.history[row - 1],
                self.history[row],
            ]
            
        return response

    def _searching(self, filter_kind: int) -> dict:
        '''
        Функция выбирает тип поиска
        Принимает - тип поиска
        Возвращает - Если данные найдены - словарь, где ключ - id, значение - запись,
        иначе ['NO DATA']
        '''
        match filter_kind:
            case 1:
                print('Введи категорию (Доход/Расход):')
                category = input()
                result = self._search_by_category(category)
            case 2:
                while True:
                    print('Введи сумму:')
                    
                    money = input()

                    if not DataValidator.check_digit(money):
                        print('Неверный формат')
                        time.sleep(3)
                        self.clear()
                        continue

                    money = int(money)

                    if money < 0:
                        print('Сумма не может быть отрицательмы числом')
                        time.sleep(3)
                        self.clear()
                        continue

                    result = self._search_by_money(money)
                    break
            case 3:
                while True:

                    print('Введите дату в формате YYYY-MM-DD')
                    date = input()

                    if not DataValidator.check_date(date):
                        print('Неверный формат даты')
                        time.sleep(3)
                        self.clear()
                        continue

                    result = self._search_by_date(date)
                    break

            case 4:
                print('Введите часть или полное описание:')
                request = input()
                result = self._search_by_description(request)

        return result

    def search(self):
        '''
        Запрашивает у пользователя тип поиска, выдает ему результат,
        а затем запрашивает на редактирование одной из найденных записей
        '''
        result = []

        while not result:

            print('Выберите критерий поиска:')
            print('1 - По категории')
            print('2 - По сумме')
            print('3 - По дате')
            print('4 - По описанию')
            filter_kind = input()

            if not DataValidator.check_digit(filter_kind):
                print("Неверный формат")
                time.sleep(3)
                self.clear()
                continue

            filter_kind = int(filter_kind)

            if filter_kind not in range(1, 5):
                print("Неверный номер фильтра")
                time.sleep(3)
                self.clear()
                continue

            result = self._searching(filter_kind)

            result = ['NO DATA'] if not result else result

            print(result)

        if result == ['NO DATA']:
            return
        
        while True:
            print('Редактировать?\n1 - Да\n2 - Нет')

            edit = input()

            if not DataValidator.check_digit(edit):
                print('Неверный формат')
                time.sleep(3)
                self.clear()
                continue

            edit = int(edit)

            if edit not in range(1, 3):
                print('Неверное действие, попробуйте еще раз')
                time.sleep(3)

            if edit == 1:
                self.edit_recording(result)
            break

    def add_recording(self):
        '''
        Запрашивает у пользователя категорию, сумму и описание,
        затем собирает и заносит эту запись в атрибут класса history,
        а после завершения программы все сохранияется в файле
        '''
        while True:
            date = datetime.now().date().strftime('%Y-%m-%d')
            print('=='*35)
            print('Выберите категорию')
            print('1 - Доход\n2 - Расход')

            category = input()

            if not DataValidator.check_digit(category):
                print("Неверный формат")
                time.sleep(3)
                self.clear()
                continue

            category = int(category)

            if category not in range(1, 3):
                print("Неверный номер категории")
                time.sleep(3)
                self.clear()
                continue

            print('Введите сумму:')

            money = input()

            if not DataValidator.check_digit(money):
                print("Неверный формат")
                time.sleep(3)
                self.clear()
                continue

            money = float(money)

            if money < 0:
                print("Сумма не может быть отрицательмы числом")
                time.sleep(3)
                self.clear()
                continue

            print('Добавьте описание к записи:')

            description = input()

            break

        match category:
            case 1:
                category = 'Доход'
                self.balance += money
            case 2:
                category = 'Расход'
                self.balance -= money

        recording = [
            'Дата: ' + date + '\n',
            'Категория: ' + category + '\n',
            'Сумма: ' + str(money) + '\n',
            'Описание: ' + description + '\n\n',
        ]
        self.history.extend(recording)

    def edit_recording(self, records: dict):
        '''
        Принимает - словари с найденными записями
        Возвращает - None
        Запрашивает у пользователя id, потом, если id найден, тип поиска, выдает ему результат,
        а затем запрашивает на редактирование одной из найденных записей
        После этого данные заменяются новыми
        '''
        while True:
            print('Выбери один id из найденных записей')
            id = input()

            if not DataValidator.check_digit(id):
                print('Неверный формат')
                time.sleep(3)
                self.clear()
                continue

            id = int(id) 

            if id not in records.keys():
                print('Нет такого id из поиска, выберите другой :(')
                print('Доступные id -', records.keys())
                time.sleep(3)
                self.clear()
                continue

            id *= 5

            print('Выберите категорию')
            print('1 - Доход\n2 - Расход')

            category = input()

            if not DataValidator.check_digit(category):
                print("Неверный формат")
                time.sleep(3)
                self.clear()
                continue

            category = int(category)

            if category not in range(1, 3):
                print("Неверный номер категории")
                time.sleep(3)
                self.clear()
                continue

            print('Введите сумму:')

            money = input()

            if not DataValidator.check_digit(money):
                print("Неверный формат")
                time.sleep(3)
                self.clear()
                continue

            money = float(money)

            if money < 0:
                print("Сумма не может быть отрицательмы числом")
                time.sleep(3)
                self.clear()
                continue

            print('Добавьте описание к записи:')

            description = input()

            match category:
                case 1:
                    category = 'Доход'
                    diff = float(self.history[id + 2].replace('Сумма: ', '').replace('\n', '')) - money
                    self.balance -= diff
                case 2:
                    category = 'Расход'
                    diff = float(self.history[id + 2].replace('Сумма: ', '').replace('\n', '')) - money
                    self.balance += diff
            
            self.history[id + 1] = 'Категория: ' + category
            self.history[id + 2] = 'Сумма: ' + str(money)
            self.history[id + 3] = 'Описание: ' + description + '\n'
            break

    def _operation_choice(self, operation: int):
        '''
        Принимает - тип операции в int
        Выбирает дальнейшее действие для поданной операции
        '''
        match operation:
            case 1:
                self.search()
            case 2:
                print(f'Ваш баланс составляет {self.balance} руб.')
            case 3:
                self.add_recording()
            case 4:
                self.search()
            case _:
                print(f'Нет такого действия - {operation}')

    def loop(self):
        '''
        Запускает все приложение личного финансового кошелька
        '''
        while True:

            editable = 0
            print('Выберите действие:')
            print('0 - Выйти')
            print('1 - Поиск записей')
            print('2 - Узнать баланс')
            print('3 - Добавить запись')
            if self.history:
                print('4 - Редактировать запись')
                editable = 1

            choice = input()

            if not DataValidator.check_digit(choice):
                print('Неверный формат')
                time.sleep(3)
                self.clear()
                continue

            choice = int(choice)

            if choice not in range(0, 4 + editable):
                print('Неверное действие, попробуйте еще раз')
                time.sleep(3)
                self.clear()
                continue

            if not choice:
                self._save_changes()
                print('==  До встречи :)  ==')
                break
            self._operation_choice(choice)
            print('=/'*35)



if __name__ == '__main__':

    my_wallet = Wallet()
    my_wallet.loop()
