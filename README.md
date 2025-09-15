# FRONTEND PROSCRUM

## Aufbau der Webseite

Die Webseite ist Grundlegend auf zwei Teile aufgebaut. Die Navigationsleiste und den Inhalt

## Navigationsleiste

Links befindet sich das Logo und der Name der Website. Rechts kann zwischen Home und Login gewechselt werden. Je nach Auswahl ändert sich der Inhalt, die Navigation bleibt jedoch gleich.

## Inhalt:

## Home

Hier gibt es zwei Felder: Input und Output. Im Input werden die Daten für die Berechnung des Handicaps eingegeben. Im Output wird der Status der Berechnung angezeigt und das Ergebnis ausgegeben.

## Golfplätze

Hier werden alle Golfplätze angezeigt.
- Man kann mit filtern den richtigen Golfplatz finden.
- Man kann sich de Golfplatz genauer anschauen.
- Man kann einen Golfplatz hinzufügen

## Runden

Hier werden alle Runden angezeigt.
- Man kann die Runden Filtern
- Man kann sch Details der Runden anschauen.
- Man kann die Runden Updaten.
- Man kann sich Rechts den Vergeich seines Handicaps anschauen.

## Code Aufbau

Die Ordner struckur ist wie folgt:

```bash
src/
├── assets/          # Statische Dateien wie Bilder, Fonts oder Icons
├── components/      # Vue-Komponenten
├── composables/     # Logik(API Aufruf)
├── pages/           # Seitenkomponenten(Home, Courses, Rounds)
├── router/          # Routing-Konfiguration (z. B. index.js)
├── style/           # CSS-Dateien für das Styling
├── views/           # Ganze Webseite(Navbar, Inhalt)

```
## Pages

Pages sind die Schnittstellen der einzelnen Komponenten. Jeder API-Aufruf an das Backend wird von der entsprechenden Page ausgeführt. Zum Beispiel braucht die Ausgabe der Brechung alle Runden Wird in der HomePage eine Funktion aufgerufen und eine API-Anfrage an das Backend gestellt. Diese Anfrage gibt eine Liste von Runden zurück.
So wird es bei alle andern Komponenten auch gemacht


## Projekt Setup

```sh
--> package-lock.json Löschen
--> .npmrc im Fronend Ordner erstellen
--> mit: registry=https://registry.npmjs.org
--> npm i
```

### Starten mit
```sh
npm run dev
```

### Build mit
```sh
npm run build
```

### Team
Frontend Development:
    - [Jakob Fischer](https://github.com/JakobFischer2574)
Backend Development:
    - [Jan Brandenstein](https://github.com/JanBrandenstein)
    - [Martin](https://github.com/Moartin-Dev)
    - [Robin](https://github.com/notsambutrobin)
    - [Samuel Gerules](https://github.com/Sannynator)
Server Hosting:
    - [Jan Brandenstein](https://github.com/JanBrandenstein)
Team Lead and Scrum Master:
    - [Santino](https://github.com/Sanny64)

## Lizenz

[Jakob Fischer](https://github.com/JakobFischer2574)

