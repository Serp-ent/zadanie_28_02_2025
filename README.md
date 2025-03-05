# Zadanie

Zgodnie z treścią zadania, zadanie posiada pola w języku polskim.

// TODO: zadania mogą tworzyć administratorzy oraz zalogowaniu użytkownicy

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

### Dodawanie zadania

1. Tworzenie zadania z o nazwie "Code refactor",

   - domyślnie przypisany jest użytkownik, który utworzył te zadanie
   - domyślnie nowe zadanie mają pole status równe "NOWY"
   - login/hasło jest podane po fladze -u (tutaj admin:admin)

   ```shell
   curl -u admin:admin -X POST http://localhost:8000/api/tasks/ \
   -H "Content-Type: application/json" \
   -d '{
       "nazwa": "Code refactor"
       }'
   ```

2. Tworzenie zadania z przypisanym użytkownikiem, i ustalonym statusem

   - przypisane do użytkownika o ID 10
   - status o wartości "W_TOKU"
   - tylko admin może tworzyć zadania z dowolnym przypisanym użytkownikiem

   ```shell
       curl -u admin:admin -X POST http://localhost:8000/api/tasks/ \
       -H "Content-Type: application/json" \
       -d '{
           "nazwa": "Assigned Task",
           "opis": "description of task",
           "status": "W_TOKU",
           "user": 10
           }'
   ```

3. Tworzenie zadania jako dowolny użytkownik

   - użytkownik jest automatycznie przypisany jako ten tworzący zadanie
   - status o wartości "W_TOKU"
   - tylko admin może tworzyć zadania z dowolnym przypisanym użytkownikiem
   - jeśli użytkownik określi innego użytkownika to pole jest ignorowane, i zadanie jest przypisane do tworzącego

   ```shell
       curl -u ash:ash -X POST http://localhost:8000/api/tasks/ \
       -H "Content-Type: application/json" \
       -d '{
           "nazwa": "Assigned Task",
           "opis": "description of task",
           "status": "W_TOKU"
           }'
   ```

### Edycja zadania

1. Edycja jako admin

   - Administrator może dowolnie edytować zadania
   - przypisanie do zadania 4
   - przypisanie użytkownika o id 10

   ```shell
       curl -u admin:admin -X PATCH http://localhost:8000/api/tasks/4/ \
       -H "Content-Type: application/json" \
       -d '{
            "status": "W_TOKU",
            "user": 10
        }'
   ```

2. Edycja jako zwykły użytkownik

   - edycja zadania o id 4
   - autoryzacja za pomocą <login>:<hasło> tutaj ash:ash
   - Użytkownik może edytować zadanie, ale nie może przypisać do niego innego użytkownika, lub NULL'a (sprawić że zadanie nie będzie przypisane do nikogo)

   ```shell
       curl -u ash:ash -X PATCH http://localhost:8000/api/tasks/4/ \
       -H "Content-Type: application/json" \
       -d '{
            "status": "W_TOKU",
            "user": 10
        }'
   ```

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
