# Zadanie

Uruchomienie serwera:

```bash
# Sklonowanie repozytorium
git clone https://github.com/Serp-ent/zadanie_28_02_2025.git
cd zadanie_28_02_25

# Przygotowanie środowiska
python -m venv .venv
source ./.venv/bin/activate

# Zainstalowanie pakietkow
pip install -r requirements.txt
# Uruchomienie aplikacji oraz serwera bazy danych
docker-compose up --build
```

## Korzystanie z Api

- Wyświetlenie wszystkich zadań
- TODO

```shell
curl [...]
```