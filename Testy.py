import unittest

# Importuj funkcję, którą chcesz przetestować
from Funkcje_Baza import convert_to_dict

class TestConvertToDictFunction(unittest.TestCase):

    def test_convert_to_dict(self):
        # Przygotuj dane wejściowe
        input_data = [(1, 'Product1', 10, 50.0), (2, 'Product2', 20, 30.0)]

        # Wywołaj funkcję, którą chcesz przetestować
        result = convert_to_dict(input_data)

        # Sprawdź, czy funkcja zwraca oczekiwane wyniki
        expected_result = [
            {"tow_kod": 1, "tow_name": 'Product1', "ilo_is": 10, "ce": 50.0},
            {"tow_kod": 2, "tow_name": 'Product2', "ilo_is": 20, "ce": 30.0},
        ]
        self.assertEqual(result, expected_result)

class TestConvertToDictFunction2(unittest.TestCase):

    def test_convert_to_dict2(self):
        # Przygotuj dane wejściowe
        input_data = [[1, 'Product1', 10, 50.0], [2, 'Product2', 20, 30.0]]

        # Wywołaj funkcję, którą chcesz przetestować
        result = convert_to_dict(input_data)

        # Sprawdź, czy funkcja zwraca oczekiwane wyniki
        expected_result = [
            {"tow_kod": 1, "tow_name": 'Product1', "ilo_is": 10, "ce": 50.0},
            {"tow_kod": 2, "tow_name": 'Product2', "ilo_is": 20, "ce": 30.0},
        ]
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
