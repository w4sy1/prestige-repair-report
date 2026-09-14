# Użycie

`python app.py template --template-file zlecenie.json`
Uzupełnij JSON, następnie: `python app.py generate --input zlecenie.json --directory reports`

Wszystkie pola ze specyfikacji są w szablonie, serial opcjonalny. Czas pracy podawaj
w minutach; części jako listę opisów. Wymagane są numer, klient, urządzenie, problem,
diagnoza, wykonane czynności i test końcowy. Technik domyślnie Dominik Wasilak — Prestige Tech.
HTML jest gotowy do otwarcia/przeglądu i wydruku w przeglądarce. PDF celowo nie jest generowany.
Program nie wysyła raportu do klienta. Przed przekazaniem sprawdź treść i dane osobowe.
