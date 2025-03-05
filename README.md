# Zadanie

Zgodnie z treścią zadania pola w modelu Task są w języku polskim.

- zadania może tworzyć dowolny zalogowany użytkownik i przy jego tworzeniu domyślnie jest przypisany użytkownik który je tworzy
- zadania może usuwać tylko administrator
- zadania może edytować adminstrator i użytkownik przypisany do niego, ale tylko administrator może przypisywać innego użytkownika (przypisany użytkownik może zmieniać nazwe, opis ale nie pole 'user')
- aby uzyskać snapshot zadania z dowolnego momentu, trzeba filtrować dla końcówki /api/tasks/?as_of=<timestamp>

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
   - aby edytować zadanie użytkownik musi być administratorem, lub być do niego przpyisanym
   - Zwykły może edytować zadanie, ale nie może przypisać do niego innego użytkownika, lub NULL'a (sprawić że zadanie nie będzie przypisane do nikogo)

   ```shell
       curl -u ash:ash -X PATCH http://localhost:8000/api/tasks/4/ \
       -H "Content-Type: application/json" \
       -d '{
            "status": "W_TOKU",
        }'
   ```

### Usuwanie zadania

- Tylko administrator może usuwać zadania

  ```shell
      curl -u admin:admin -X DELETE http://localhost:8000/api/tasks/4/
  ```

### Listowanie wszystkich zadań

```shell
curl http://localhost:8000/api/tasks/
```

### Wyświetlanie zadania o id 1 (jego szczegółów)

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

### Filtrowanie zadań do których przypisany użytkownik zawiera w nicku 'ash'

```shell
curl http://localhost:8000/api/tasks/?username=ash
```

### Wyświetlenie zadań zawierających w opisie "gotowanie" (bez względu na wielkość liter)

```shell
curl -X GET http://localhost:8000/api/tasks/\?opis\=gotowanie
```

### Wyświetlenie zadań zawierających w nazwie "brock" (bez względu na wielkość liter)

```shell
curl -X GET http://localhost:8000/api/tasks/\?nazwa\=brock
```

---

### Wyświetlenie historii wszystkich zadań

```shell
curl http://localhost:8000/api/history/
```

### Wyświetlenie historii dla zadania o ID 3

```shell
curl http://localhost:8000/api/history/?id=1
```

### Wyświetlenie zadań do których był przypisany użytkownik o id 3

```shell
curl http://localhost:8000/api/history/?user=3
```

> [!NOTE]
> Aby wyświetlic jak wyglądało zadanie w danym momencie, trzeba skorzystać z filtru as_of dla /api/tasks/:pk/

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
