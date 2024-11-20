import secrets
import string


class PasswordGenerator:
    def __init__(self, length, use_letters=True, use_digits=True, use_special=True):
        """
        Инициализация генератора паролей с параметрами.
        :param length: Длина пароля
        :param use_letters: Включать ли буквы в пароль
        :param use_digits: Включать ли цифры в пароль
        :param use_special: Включать ли спецсимволы в пароль
        """
        self.length = length
        self.use_letters = use_letters
        self.use_digits = use_digits
        self.use_special = use_special

    def generate_password(self):
        """
        Генерация случайного пароля на основе предпочтений.
        :return: Сгенерированный пароль
        """
        alphabet = ""
        if self.use_letters:
            alphabet += string.ascii_letters  # Добавляем буквы
        if self.use_digits:
            alphabet += string.digits  # Добавляем цифры
        if self.use_special:
            alphabet += string.punctuation  # Добавляем спецсимволы

        if not alphabet:
            raise ValueError("Нужно выбрать хотя бы один тип символов для пароля.")

        password = ''.join(secrets.choice(alphabet) for _ in range(self.length))
        return password

    def assess_password_strength(self, password):
        """
        Оценка сложности пароля (от 0 до 10).
        :param password: Пароль для оценки
        :return: Оценка сложности от 0 до 10
        """
        length_score = min(len(password) // 3, 3)  # Оценка по длине
        types_score = 0
        if any(c.islower() for c in password): types_score += 2
        if any(c.isupper() for c in password): types_score += 2
        if any(c.isdigit() for c in password): types_score += 2
        if any(c in string.punctuation for c in password): types_score += 2

        total_score = length_score + types_score
        return min(total_score, 10)  # Оценка сложности

    def save_passwords(self, passwords, filename="passwords.txt"):
        """
        Сохранение паролей в файл.
        :param passwords: Список паролей для сохранения
        :param filename: Имя файла
        """
        if not passwords:
            print("Нет паролей для сохранения.")
            return
        with open(filename, 'a') as file:
            for password in passwords:
                file.write(password + '\n')
        print(f"Пароли сохранены в файл: {filename}")


class UserInterface:
    def get_user_preferences(self):
        """
        Получение предпочтений пользователя для генерации пароля.
        :return: Данные о длине пароля и предпочтениях по символам
        """
        try:
            length = int(input("Введите длину пароля: "))
            if length <= 0:
                print("Длина пароля должна быть положительным числом.")
                return None, None, None, None
        except ValueError:
            print("Должно быть введено целое число.")
            return None, None, None, None

        use_letters = self.ask_user("Использовать буквы (a-z, A-Z)?")
        use_digits = self.ask_user("Использовать цифры (0-9)?")
        use_special = self.ask_user("Использовать спецсимволы (например, @, #, $)?")

        return length, use_letters, use_digits, use_special

    def ask_user(self, question):
        """
        Функция для получения ответа от пользователя.
        :param question: Вопрос, на который нужно ответить "1) Да" или "2) Нет"
        :return: True (если "Да"), False (если "Нет")
        """
        print(question)
        print("1) Да")
        print("2) Нет")
        while True:
            choice = input("Ваш выбор (1/2): ")
            if choice == "1":
                return True
            elif choice == "2":
                return False
            else:
                print("Неверный ввод, пожалуйста, выберите 1 или 2.")

    def mask_password(self, password):
        """
        Маскировка пароля для предотвращения нежелательного просмотра.
        :param password: Пароль для маскировки
        :return: Замаскированный пароль
        """
        return "*" * len(password)


def main():
    ui = UserInterface()
    length, use_letters, use_digits, use_special = ui.get_user_preferences()
    if length is None:
        return

    password_generator = PasswordGenerator(length, use_letters, use_digits, use_special)

    # Генерация пароля
    password = password_generator.generate_password()
    print(f"Сгенерированный пароль: {password}")

    # Оценка сложности пароля
    strength = password_generator.assess_password_strength(password)
    print(f"Сложность пароля (0-10): {strength}")

    # Запрашиваем у пользователя, маскировать ли пароль
    mask_choice = input("Хотите ли вы маскировать пароль при отображении? (1) Да 2) Нет): ").lower()
    if mask_choice == '1':
        password = ui.mask_password(password)
        print(f"Маскированный пароль: {password}")
    else:
        print(f"Пароль: {password}")

    # Сохранение пароля в файл
    save_choice = input("Хотите сохранить пароль в файл? (1) Да 2) Нет): ").lower()
    if save_choice == '1':
        password_generator.save_passwords([password])


if __name__ == "__main__":
    main()
