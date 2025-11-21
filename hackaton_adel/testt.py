import unittest
from message_handlers import generation_litresponse
from filtrr import contains_bad_words


class TestBot(unittest.TestCase):

    def test_generation_litresponse(self):
        """Тест статических ответов"""
        self.assertEqual(
            generation_litresponse("привет"),
            'Привет! я Литературный помощник, чем могу помочь?'
        )
        self.assertEqual(
            generation_litresponse("перескажи"),
            "Я готов сделать краткий перессказ произведения, пришлите название произведения или книги."
        )
        self.assertIsNone(generation_litresponse("случайный текст"))

    def test_bad_words_filter(self):
        """Тест фильтра плохих слов"""
        self.assertTrue(contains_bad_words("ты дурак"))
        self.assertFalse(contains_bad_words("привет"))


if __name__ == '__main__':
    unittest.main()