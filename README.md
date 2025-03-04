# Zadanie

Uruchomienie serwera:

```bash
# Sklonowanie repozytorium
git clone https://github.com/Serp-ent/zadanie_28_02_2025.git
cd zadanie_28_02_25

# Zainstalowanie pakietkow
pip install -r requirements.txt
# Uruchomienie aplikacji oraz serwera bazy danych
docker-compose up --build
# stworzenie tabel w bazie danych
docker exec -it zadanie_28_02_2025-mgazadanie-1 python manage.py migrate
```

## Korzystanie z Api

- Wyświetlenie wszystkich zadań
- TODO

```shell
curl [...]
```