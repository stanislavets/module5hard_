import time
from hashlib import sha256

class UrTube:
    def __init__(self):
        self.users = []
        self.videos = []
        self.current_user = None

    def log_in(self, nickname, password):
        for user in self.users:
            if user.nickname == nickname and user.password == password:
                self.current_user = user
                print("Вы вошли")
                return  # Выйти после успешного входа
        print("Данные не верны")

    def hash_password(self, password):
        return sha256(password.encode()).hexdigest()

    def register(self, nickname, password, age):
        if any(user.nickname == nickname for user in self.users):
            print("Пользователь {nickname} уже существует".format(nickname=nickname))
        else:
            hashed_password = self.hash_password(password)  # Хешируем пароль перед сохранением
            new_user = User(nickname, hashed_password, age)
            self.users.append(new_user)
            self.current_user = new_user
            print("Добро  пожаловать, {nickname} ".format(nickname=nickname))

    def log_out(self):
        self.current_user = None

    def add(self, *videos):
        for video in videos:
            if not any(v.title == video.title for v in self.videos):
                self.videos.append(video)

    def get_videos(self, search_word):
        return [v.title for v in self.videos if search_word.lower() in v.title.lower()]

    def watch_video(self, video_title):

        for v in self.videos:
            if v.title == video_title:
                if self.current_user is not None:
                    time.sleep(1)  # Пауза в 1 секунду перед следующим выводом
                    v.time_now += 1
                    if v.adult_mode and self.current_user.age < 18:
                        print("Вам нет 18 лет, пожалуйста покиньте страницу")
                        return

                else:
                    print("Войдите в аккаунт, чтобы смотреть видео")
                    if v.time_now >= v.duration:
                        v.time_now = 0
                    found_video = next((v for v in self.videos if v.title == video_title), None)

                    if found_video is not None:
                        while found_video.time_now < found_video.duration:
                            print(found_video.time_now + 1)  # Вывод следующей секунды просмотра
                            found_video.time_now += 1
                    if found_video.time_now >= found_video.duration:
                        found_video.time_now = 0
                    print("Конец видео")

                    break
                break


class Video:
    def __init__(self, title, duration, time_now=0, adult_mode=False):
        self.title = title
        self.duration = duration
        self.time_now = time_now
        self.adult_mode = adult_mode


class User:
    def __init__(self, nickname, password, age):
        self.nickname = nickname
        self.password = password
        self.age = age

ur = UrTube()
v1 = Video('Лучший язык программирования 2024 года', 200)
v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)

# Добавление видео
ur.add(v1, v2)

# Проверка поиска
print(ur.get_videos('лучший'))
print(ur.get_videos('ПРОГ'))

# Проверка на вход пользователя и возрастное ограничение
ur.watch_video('Для чего девушкам парень программист?')
ur.register('vasya_pupkin', 'lolkekcheburek', 13)
ur.watch_video('Для чего девушкам парень программист?')
ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)
ur.watch_video('Для чего девушкам парень программист?')

# Проверка входа в другой аккаунт
ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55)
print(ur.current_user)

# Попытка воспроизведения несуществующего видео
ur.watch_video('Лучший язык программирования 2024 года!')
