# Zadanie

## Uruchomienie serwera

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

---

## Rejestracja Użytkownika

```shell
curl -X POST http://localhost:8000/api/register/ \
-H "Content-Type: application/json" \
-d '{
    "username": "username",
    "password": "user_password",
    "email": "user@example.com"
}'
```

## Logowanie

Do testowania za pomocą komendy curl dodałem basic authentication, zatem logowanie do pozyskania id sesji lub tokena jwt jest niepotrzebne.

```shell
# curl -X POST http://localhost:8000/api/login/ \
# -H "Content-Type: application/json" \
# -d '{
#     "username": "username",
#     "password": "user_password",
# }'
```

---

## Zadania

### Listowanie wszystkich zadań

```shell
curl http://localhost:8000/api/tasks/
```

### Wyświetlanie zadania o id 1

```shell
curl http://localhost:8000/api/tasks/1/
```

### Wyświetlanie zadania w danym momencie

```shell
curl http://localhost:8000/api/tasks/1/\?as_of\=2025-03-04T15:52:23.997522Z
```

### Filtrowanie nieprzypisanych zadań

```shell
curl http://localhost:8000/api/tasks/1/?unassigned=true
```

### Filtrowanie nowych zadań

```shell
curl http://localhost:8000/api/tasks/?status=NOWY
```

### Filtrowanie zadań przypisanych do użytkownika o ID 3

```shell
curl http://localhost:8000/api/tasks/?user=3
```

---

### Wyświetlenie history wszystkich zadań

```shell
curl http://localhost:8000/api/history/
```

### Wyświetlenie history dla zadania o ID 3

```shell
curl http://localhost:8000/api/history/?id=1
```

### Wyświetlenie zadań do których był przypisany użytkownik o id 3

```shell
curl http://localhost:8000/api/history/?user=3
```

---

## Użytkownicy

### Listowanie użytkowników

```shell
curl http://localhost:8000/api/users/
```

### Pobieranie konkretnego użytkownika

```shell
curl http://localhost:8000/api/users/1/
```

### Aktualizacja profilu

- aktualizować profil może tylko jego własciciel oraz admin

```shell
curl -X PUT http://localhost:8000/api/users/1/ \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <your_token>" \
-d '{
    "first_name": "NewName",
    "email": "new@example.com"
}'
```
