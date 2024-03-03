import unittest
# Importuj funkcję, którą chcesz przetestować
from Funkcje_Baza import zamien_przecinek_na_kropke
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

    import unittest



class TestZamienPrzecinekNaKropkeFunction(unittest.TestCase):

    def test_zamien_przecinek_na_kropke(self):
        # Przygotuj dane wejściowe
        input_text_with_comma = "10,5"
        input_text_without_comma = "20.3"

        # Wywołaj funkcję, którą chcesz przetestować
        result_with_comma = zamien_przecinek_na_kropke(input_text_with_comma)
        result_without_comma = zamien_przecinek_na_kropke(input_text_without_comma)

        # Sprawdź, czy funkcja zwraca oczekiwane wyniki
        expected_result_with_comma = "10.5"
        expected_result_without_comma = "20.3"

        self.assertEqual(result_with_comma, expected_result_with_comma)
        self.assertEqual(result_without_comma, expected_result_without_comma)

    def test_zamien_przecinek_na_kropke_no_comma(self):
        # Przygotuj dane wejściowe bez przecinka
        input_text = "15.7"

        # Wywołaj funkcję, którą chcesz przetestować
        result = zamien_przecinek_na_kropke(input_text)

        # Sprawdź, czy funkcja zwraca dokładnie to samo, gdy nie ma przecinka
        self.assertEqual(result, input_text)




if __name__ == '__main__':
    unittest.main()
