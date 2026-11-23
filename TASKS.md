\# TASKS.md - Tasks\_app



\## Increment 1: MVP - Creació i Llistat de Tasques

Objectiu: Tenir una versió CLI funcional per afegir i consultar tasques en JSON.



\### Tasques d'Execució:

\- \[x] Tasca 1.1: Crear estructura de directoris (`src/`, `test/`, `data/`) i fitxer `data/tasks.json` inicial. (Requisits RF-01 i RF-02) 

\- \[x] Tasca 1.2: Implementar model de dades `Task` a `src/models.py` amb mètodes de serialització JSON.

\- \[x] Tasca 1.3: Desenvolupar Tasks\_app a `src/tasks\_app.py` amb opcions `add` i `list`.(Requisits RF-03 i RF-04)

\- \[x] Tasca 1.4: Crear test d'integració a `test/test\_tasks\_app.py` segons els escenaris GS-01, GS-02 i GS-03.

\- \[x] Tasca 1.5: Validar execució amb OpenCode i verificar que tots els tests passen (`python3 -m pytest test`).

## Increment 2 (Part A): Dates Límit i Alertes
Objectiu: Permetre indicar `--due YYYY-MM-DD` en crear tasques i mostrar `[CADUCADA]` o `[URGENT]` al llistat.

### Tasques d'Execució (Part A):
- [x] Tasca 2.1: Actualitzar el model `Tasca` a `src/models.py` i el comandament `add` a `src/tasks_app.py` per suportar l'argument opcional `--due YYYY-MM-DD`. (Requisit RF-05)
- [x] Tasca 2.2: Actualitzar el comandament `list` a `src/tasks_app.py` per mostrar les etiquetes `[CADUCADA]` i `[URGENT]` segons la data actual en tasques pendents. (Requisits RF-06 i RF-07)
- [x] Tasca 2.3: Afegir tests d'integració a `test/test_tasks_app.py` per als escenaris GS-04, GS-05 i GS-06 i verificar que tots els tests passen (`python3 -m pytest test`).

## Increment 2 (Part B): Edició i Completat de Tasques
Objectiu: Permetre modificar atributs d'una tasca per ID (`edit --id`) i marcar tasques com a completades (`complete --id`).

### Tasques d'Execució (Part B):
- [x] Tasca 2.4: Implementar el comandament `edit --id <ID>` a `src/tasks_app.py` per modificar qualsevol atribut (`--title`, `--subject`, `--due`, `--status`). (Requisit RF-08)
- [x] Tasca 2.5: Implementar el comandament `complete --id <ID>` a `src/tasks_app.py` per canviar l'estat d'una tasca a `'completada'`. (Requisit RF-09)
- [x] Tasca 2.6: Afegir tests d'integració a `test/test_tasks_app.py` per als escenaris GS-07 i GS-08 i verificar que tots els tests passen (`python3 -m pytest test`).

## Increment 3 (Part A): Mode Resum Estadístic
Objectiu: Implementar `list --summary` per mostrar el recompte global de tasques.

### Tasques d'Execució (Part A):
- [x] Tasca 3.1: Actualitzar el comandament `list` a `src/tasks_app.py` per suportar l'opció `--summary` i mostrar el total de tasques, pendents, completades, caducades i urgents. (Requisit RF-10)
- [x] Tasca 3.2: Afegir test d'integració a `test/test_tasks_app.py` per a l'escenari GS-09 i verificar que tots els tests passen (`python3 -m pytest test`).


## Increment 3 (Part B): Filtres de Llistat
Objectiu: Implementar `list --subject` i `list --keyword` per filtrar tasques.

### Tasques d'Execució (Part B):
- [x] Tasca 3.3: Actualitzar el comandament `list` a `src/tasks_app.py` per suportar els filtres `--subject <assignatura>` i `--keyword <paraula>`. (Requisits RF-11 i RF-12)
- [ ] Tasca 3.4: Afegir tests d'integració a `test/test_tasks_app.py` per als escenaris GS-10 i GS-11 i verificar que tots els tests passen (`python3 -m pytest test`).

