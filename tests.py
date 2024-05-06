'''
Тест методов Wallet
'''
import unittest
from main import Wallet

class TestWalletClass(unittest.TestCase):
    def setUp(self):
        # Тестовые данные
        self.wallet = Wallet()
        self.wallet.balance = 1000
        self.wallet.history = [
            'Дата: 2024.05.03',
            'Категория: Расход',
            'Сумма: 400.5',
            'Описание: купил курицу',
            '',
            'Дата: 2024.05.06',
            'Категория: Доход',
            'Сумма: 250.5',
            'Описание: нашел на скамейке',
        ]

    def test_search_category(self):

        result = self.wallet._search_by_category('Расход')
        test_result = {
            0: [
                'Дата: 2024.05.03',
                'Категория: Расход',
                'Сумма: 400.5',
                'Описание: купил курицу',
            ]
        }
        self.assertEqual(len(result), 1)
        self.assertEqual(result, test_result)

    def test_search_money(self):
        
        result = self.wallet._search_by_money(250.5)
        test_result = {
            1: [
                'Дата: 2024.05.06',
                'Категория: Доход',
                'Сумма: 250.5',
                'Описание: нашел на скамейке',
            ]
        }
        self.assertEqual(len(result), 1)
        self.assertEqual(result, test_result)

    def test_search_date(self):
        
        result = self.wallet._search_by_date('2024.05.06')
        test_result = {
            1: [
                'Дата: 2024.05.06',
                'Категория: Доход',
                'Сумма: 250.5',
                'Описание: нашел на скамейке',
            ]
        }
        self.assertEqual(len(result), 1)
        self.assertEqual(result, test_result)

    def test_search_full_description(self):
        
        result = self.wallet._search_by_description('нашел на скамейке')
        test_result = {
            1: [
                'Дата: 2024.05.06',
                'Категория: Доход',
                'Сумма: 250.5',
                'Описание: нашел на скамейке',
            ]
        }
        self.assertEqual(len(result), 1)
        self.assertEqual(result, test_result)
    
    def test_search_part_description(self):
        
        result = self.wallet._search_by_description('нашел')
        test_result = {
            1: [
                'Дата: 2024.05.06',
                'Категория: Доход',
                'Сумма: 250.5',
                'Описание: нашел на скамейке',
            ]
        }
        self.assertEqual(len(result), 1)
        self.assertEqual(result, test_result)

    def test_search_many_results(self):
        
        result = self.wallet._search_by_description('к')
        test_result = {
            0: [
                'Дата: 2024.05.03',
                'Категория: Расход',
                'Сумма: 400.5',
                'Описание: купил курицу',
            ],
            1: [
                'Дата: 2024.05.06',
                'Категория: Доход',
                'Сумма: 250.5',
                'Описание: нашел на скамейке',
            ]
        }
        self.assertEqual(len(result), 2)
        self.assertEqual(result, test_result)

if __name__ == '__main__':
    unittest.main()