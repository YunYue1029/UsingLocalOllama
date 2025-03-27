from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

class CalculatorTests(APITestCase):
    def setUp(self):
        self.url = '/api/calculator/calculate/'

    def test_addition(self):
        """測試加法運算"""
        data = {
            'num1': 10,
            'num2': 5,
            'operation': '+'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'], 15)
        self.assertEqual(response.data['num1'], 10)
        self.assertEqual(response.data['num2'], 5)
        self.assertEqual(response.data['operation'], '+')

    def test_subtraction(self):
        """測試減法運算"""
        data = {
            'num1': 10,
            'num2': 5,
            'operation': '-'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'], 5)

    def test_multiplication(self):
        """測試乘法運算"""
        data = {
            'num1': 10,
            'num2': 5,
            'operation': '*'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'], 50)

    def test_division(self):
        """測試除法運算"""
        data = {
            'num1': 10,
            'num2': 5,
            'operation': '/'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'], 2)

    def test_division_by_zero(self):
        """測試除以零的錯誤處理"""
        data = {
            'num1': 10,
            'num2': 0,
            'operation': '/'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Cannot divide by zero')

    def test_invalid_operation(self):
        """測試無效的運算符號"""
        data = {
            'num1': 10,
            'num2': 5,
            'operation': '%'  # 無效的運算符號
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Invalid operation. Use +, -, *, or /')

    def test_missing_parameters(self):
        """測試缺少參數的情況"""
        # 缺少 num2
        data = {
            'num1': 10,
            'operation': '+'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # 缺少 operation
        data = {
            'num1': 10,
            'num2': 5
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_number_format(self):
        """測試無效的數字格式"""
        data = {
            'num1': 'abc',  # 無效的數字
            'num2': 5,
            'operation': '+'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Please provide valid numbers')

    def test_decimal_numbers(self):
        """測試小數運算"""
        data = {
            'num1': 10.5,
            'num2': 5.2,
            'operation': '+'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertAlmostEqual(response.data['result'], 15.7)

    def test_negative_numbers(self):
        """測試負數運算"""
        data = {
            'num1': -10,
            'num2': 5,
            'operation': '*'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'], -50) 