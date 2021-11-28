from pprint import pprint

import psycopg2

import time

class Timer:
    def __init__(self, name=None):
        self.name = name

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, *args):
        self.end = time.perf_counter()
        self.interval = self.end - self.start
        print(f'----{self.name}---- \n time {self.interval}')



connection = psycopg2.connect(
    user='flaskapp',
    password='flaskapp',
    host='127.0.0.1',
    port='5432',
    database='flaskapp_dev'
)

cursor = connection.cursor()

select = (
    "select pracownicy.id, wizyty.id,"
    "(SELECT pacjenci.nazwisko from pacjenci where pacjenci.id = wizyty.pacjent)"
    "from wizyty "
    "inner join pracownicy "
    "on wizyty.dentysta=pracownicy.id "
    "where wizyty.czy_sie_odbyla = false "
    "and pracownicy.imie = 'Anna' " 
    "and pracownicy.nazwisko = 'Dobra';"
    )

with Timer('Select 2'):
    result = cursor.execute(select)
    print(result)

pprint(cursor.fetchall())

insert=(
    "insert into wizyty (godzina_rozpoczecia, godzina_zakonczenia, czy_sie_odbyla, dentysta, pacjent) "
    "SELECT godzina_rozpoczecia, godzina_zakonczenia, TRUE, dentysta, pacjent "
    "FROM wizyty "
    "WHERE wizyty.dentysta = 1; "
)

with Timer('Insert 1'):
    result = cursor.execute(insert)
    connection.commit()
    print(result)

