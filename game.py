from datetime import datetime as dt
from random import randint


def access_control(func):
    def wrapper(*args, **kwargs):
        if kwargs.get('username') == Game.ADMIN_USERNAME:
            result = func(*args, **kwargs)
            return result
        else:
            print(Game.UNKNOWN_COMMAND)
    return wrapper


def write_to_file(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        with open('game_result.txt', 'a') as g:
            g.write(result)
        return result
    return wrapper


class Game:
    ADMIN_USERNAME = 'Admin'
    UNKNOWN_COMMAND = 'Неизвестная команда. Попробуйте ввести еще раз!'
    start_time = dt.now()
    total_games = 0

    @access_control
    @staticmethod
    def get_statistics(total_games: int, **kwargs) -> None:
        game_time = dt.now() - Game.start_time
        print(f'Общее время игры: {game_time}, текущая игра - №{total_games}')

    @access_control
    @staticmethod
    def get_right_answer(number: int, *args, **kwargs) -> None:
        return print(f'Правильный ответ: {number}')

    @staticmethod
    def check_number(username: str, guess: int, number: int) -> bool:
        # Если угадано...
        if guess == number:
            print(f'Отличная интуиция, {username}! Вы угадали число: :)')
            # Возвращаем True
            return True

        if guess < number:
            print('Ваше число меньше того, что загадано.')
        else:
            print('Ваше число больше того, что загадано.')
        return False

    @write_to_file
    @staticmethod
    def game(username: str, total_games: int) -> str:
        # Получаем случайное число в диапазоне от 1 до 100.
        number = randint(1, 100)
        print(
            '\nУгадайте число от 1 до 100.\n'
            'для выхода из текущей игры введите команду "stop"'
        )
        while True:
            # Получаем пользовательский ввод,
            # отрезаем лишние пробелы и переводим в нижний регистр.
            user_input = input('Введите чило или команду: ').strip().lower()

            match user_input:
                case 'stop':
                    break
                case 'stat':
                    Game.get_statistics(total_games, username=username)
                case 'answer':
                    Game.get_right_answer(number, username=username)
                case _:
                    try:
                        guess = int(user_input)
                    except ValueError:
                        print(Game.UNKNOWN_COMMAND)
                        continue
                    if Game.check_number(username, guess, number):
                        break
        return f'Загаданное число: {number}!'

    @staticmethod
    def get_username() -> str:
        username = input('Представтесь пожалуйста: ').strip()
        if username == Game.ADMIN_USERNAME:
            print('Добро пожаловать, создатель\n'
                  'Команды "stat", "answer" доступны для Вас.')
        else:
            print(f'\n{username}, добро пожаловать в игру.')
        return username

    @classmethod
    def guess_number(cls) -> None:
        username = cls.get_username()
        # Счетчик игр в текущей сессии
        while True:
            cls.total_games += 1
            cls.game(username, cls.total_games)
            play_again = input('\nхотите сыграть еще? (y/n)')
            if play_again.strip().lower() not in ('y', 'yes'):
                break
