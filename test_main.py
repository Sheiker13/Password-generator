import unittest
from unittest.mock import patch, mock_open
from main import PasswordGenerator, UserInterface


class TestPasswordGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = PasswordGenerator(12, use_letters=True, use_digits=True, use_special=True)

    def test_generate_password_length(self):
        password = self.generator.generate_password()
        self.assertEqual(len(password), 12, "Пароль должен быть длиной 12 символов")

    def test_generate_password_characters(self):
        generator = PasswordGenerator(12, use_letters=True, use_digits=False, use_special=False)
        password = generator.generate_password()
        self.assertTrue(all(char.isalpha() for char in password), "Пароль должен содержать только буквы")

    def test_assess_password_strength(self):
        strong_password = "Aa1!Aa1!"
        strength = self.generator.assess_password_strength(strong_password)
        self.assertEqual(strength, 10, "Оценка сложности должна быть 10 для сильного пароля")

    def test_assess_password_strength_weak(self):
        weak_password = "123"
        strength = self.generator.assess_password_strength(weak_password)
        self.assertLess(strength, 4, "Оценка сложности должна быть низкой для слабого пароля")

    @patch("builtins.open", new_callable=mock_open)
    def test_save_passwords(self, mock_file):
        password = "testpassword123"
        self.generator.save_passwords([password])
        mock_file().write.assert_called_once_with("testpassword123\n")


class TestUserInterface(unittest.TestCase):
    def setUp(self):
        self.ui = UserInterface()

    @patch("builtins.input", side_effect=["12", "1", "1", "1"])
    def test_get_user_preferences(self, mock_input):
        length, use_letters, use_digits, use_special = self.ui.get_user_preferences()
        self.assertEqual(length, 12, "Длина пароля должна быть 12")
        self.assertTrue(use_letters, "Должны использоваться буквы")
        self.assertTrue(use_digits, "Должны использоваться цифры")
        self.assertTrue(use_special, "Должны использоваться спецсимволы")

    @patch("builtins.input", side_effect=["2"])
    def test_ask_user(self, mock_input):
        response = self.ui.ask_user("Использовать цифры?")
        self.assertFalse(response, "Ответ должен быть False для выбора '2'")

    def test_mask_password(self):
        password = "password123"
        masked_password = self.ui.mask_password(password)
        self.assertEqual(masked_password, "***********", "Пароль должен быть замаскирован звездочками")


if __name__ == "__main__":
    unittest.main()
