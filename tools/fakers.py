from faker import Faker

from clients.v1.statistic.statistic_schema import StatisticV1Schema


class Fake:
    """
    Класс для генерации случайных тестовых данных с использованием библиотеки Faker.
    """

    def __init__(self, faker: Faker):
        """
        :param faker: Экземпляр класса Faker, который будет использоваться для генерации данных.
        """
        self.faker = faker

    def name(self) -> str:
        """
        Генерирует случайное имя.

        :return: Случайное имя.
        """
        return self.faker.first_name()

    def integer(self, start: int = 1, end: int = 100) -> int:
        """
        Генерирует случайное целое число в заданном диапазоне.

        :param start: Начало диапазона (включительно).
        :param end: Конец диапазона (включительно).
        :return: Случайное целое число.
        """
        return self.faker.random_int(start, end)

    def seller_id(self) -> int:
        """
        Генерирует случайный ID продавца в диапазоне от 111111 до 999999.

        :return: Случайный ID продавца.
        """
        return self.integer(111111, 999999)

    def price(self) -> int:
        """
        Генерирует случайную цену в диапазоне от 1 до 1000000.

        :return: Случайная цена.
        """
        return self.integer(1, 1000000)

    def likes(self) -> int:
        """
        Генерирует случайное количество лайков в диапазоне от 1 до 300.

        :return: Случайное количество лайков.
        """
        return self.integer(1, 300)

    def view_count(self) -> int:
        """
        Генерирует случайное количество просмотров в диапазоне от 1 до 10000.

        :return: Случайное количество просмотров.
        """
        return self.integer(1, 10000)

    def contacts(self) -> int:
        """
        Генерирует случайное количество контактов в диапазоне от 1 до 300.

        :return: Случайное количество контактов.
        """
        return self.integer(1, 300)

    def statistics(self) -> StatisticV1Schema:
        """
        Генерирует случайную статистику.

        :return: Случайная статистика.
        """
        return StatisticV1Schema(likes=self.likes(),
                                 view_count=self.view_count(),
                                 contacts=self.contacts())

    def uuid(self) -> str:
        """
        Генерирует случайный uuid.

        :return: Случайный uuid.
        """
        return self.faker.uuid4()


fake = Fake(faker=Faker())
