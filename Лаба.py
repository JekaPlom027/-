import tokenize_uk as tok
import pymorphy3
import sqlite3
from sqlite3 import Error

class Sample:
    # Клас для обробки тексту: токенізації, отримання слів та їх частотності
    def __init__(self, text):
        self._text = text
        # Токенізуємо текст на слова
        self._tokens = tok.tokenize_words(self._text)
        # Залишаємо лише слова (алфавітні символи) та переводимо їх до нижнього регістру
        self._words_list = [s.lower() for s in self._tokens if s[0].isalpha()]

    def get_words(self):
        # Повертає список унікальних слів із частотністю
        words_set = set()   # Множина для уникнення повторів
        words = []          # Список слів

        for word_str in self._words_list:
            if word_str in words_set:
                continue    # Пропускаємо слово, якщо воно вже було

            num = self._words_list.count(word_str)   # Рахуємо частоту слова
            words.append(Word.from_token(word_str, num)) # Додаємо об'єкт Word

        return words

    def show(self, words):
        # Виводить інформацію про кожне слово у списку
        for word in words:
            word.show()

class SQL:
    # Клас для роботи з базою даних SQLite
    def __init__(self, file):
        self._connection = SQL.create_connection(file)  # Підключення до бази даних
        self._cursor = self._connection.cursor()         # Створення курсора

    @staticmethod
    def create_connection(db_file):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect('Жаба-гадюка.db')    # Підключення до файлу бази даних
            print(sqlite3.version)             # Виведення версії SQLite
        except Error as e:
            print(e)                           # Виведення помилки, якщо вона виникла

        return conn

    def insert_into_freq_table(self, word):
        # Додає запис про слово до таблиці WordFreq
        data_tuple = word.get_tuple()   # Отримує дані слова у вигляді кортежу
        result = f'''
           INSERT INTO WordFreq (form, lemma, pos, freq)
           VALUES(?, ?, ?, ?);
           '''
        self._cursor.execute(result, data_tuple)
        self._connection.commit()


    def create_word_freq_table(self):
        # Створює таблицю WordFreq
        create_word_freq = f'''
               CREATE TABLE WordFreq (
                   word_id INTEGER,
                   form TEXT,
                   lemma TEXT,
                   pos TEXT,
                   freq INTEGER,
                   PRIMARY KEY(word_id)
               );
               '''
        self._cursor.execute(create_word_freq)
        self._connection.commit()

    def generate_word_freq_table(self, words):
        # Генерує таблицю WordFreq та заповнює її словами
        self.create_word_freq_table()  # Створює таблицю

        for word in words:
            self.insert_into_freq_table(word)  # Додає кожне слово

    def select_pos_freq(self):
        # Вибирає частоту слів для кожної частини мови (pos)
        result = f'''
               SELECT
                   pos,
                   COUNT(word_id)
               FROM
                   WordFreq
               GROUP BY
                   pos;
               '''
        res = self._cursor.execute(result)
        for row in res:
            print(row)

# Підрахунок кількості унікальних лем для кожної частини мов
    def select_unique_lemmas_per_pos(self):
        result = f'''
               SELECT
                   pos,
                   COUNT(DISTINCT lemma) AS unique_lemmas
               FROM
                   WordFreq
               GROUP BY
                   pos;
               '''
        res = self._cursor.execute(result)
        for row in res:
            print(row)


class Word:
    # Клас для представлення слова та його властивостей
    s_morph = pymorphy3.MorphAnalyzer(lang='uk')  # Ініціалізує аналізатор MorphAnalyzer
    def __init__(self,form, lemma, pos, freq):
        self._form = form
        self._lemma = lemma
        self._pos = pos
        self._freq = freq

    @staticmethod
    def from_token(token, freq):
        # Створює об'єкт Word з токена
        parsed = Word.s_morph.parse(token)[0]   # Аналізує токен
        return Word(token, parsed.normal_form,  parsed.tag.POS, freq)


    def show(self):
        # Виводить інформацію про слово
        print(f"Словоформа : {self._form}                Лема : {self._lemma}                Частина мови : {self._pos}                Частота : {self._freq}")

    def get_tuple(self):
        # Повертає атрибути слова у вигляді кортежу
        return (self._form, self._lemma, self._pos, self._freq)

# Читання тексту з файлу, створення об'єктів Sample та Word
with open('text_i_chitach.txt',encoding = 'utf-8', mode= 'r') as f:
     text = f.read()

     sample = Sample(text)
     words = sample.get_words()
     sample.show(words)

# Робота з базою даних
sql = SQL('PycharmProjects\\pythonProject16\\Жаба-гадюка.db')

with open('text_i_chitach.txt',encoding = 'utf-8', mode= 'r') as f:
     text = f.read()
     sample = Sample(text)
     words = sample.get_words()
     sql.generate_word_freq_table(words)

# Виконання запитів до бази даних
sql = SQL('PycharmProjects\\pythonProject16\\Жаба-гадюка.db')
sql.select_pos_freq()

# Читання тексту з файлу, створення об'єктів Sample та Word
with open('Текст 2 чорна рада.txt',encoding = 'utf-8', mode= 'r') as f:
     text = f.read()

     sample = Sample(text)
     words = sample.get_words()
     sample.show(words)

# Робота з базою даних
sql = SQL('PycharmProjects\\pythonProject16\\Жаба-гадюка.db')

with open('Текст 2 чорна рада.txt',encoding = 'utf-8', mode= 'r') as f:
     text = f.read()
     sample = Sample(text)
     words = sample.get_words()
     sql.generate_word_freq_table(words)

# Виконання запитів до бази даних
sql = SQL('PycharmProjects\\pythonProject16\\Жаба-гадюка.db')
sql.select_pos_freq()
