# Yatzy

Sovellus on Yatzy-peli yhdestä neljään pelaajalle. (Tehty HY:n kurssille Ohjelmistotekniikka syksyllä 2021)  
[Lopullinen Release](https://github.com/theJSZ/ot-harjoitustyo/releases/tag/Loppupalautus)

## Dokumentaatio
- [Lopullinen vaatimusmäärittely](./dokumentaatio/vaatimusmaarittely.md)
- [Työaikakirjanpito](./dokumentaatio/tuntikirjanpito.md)
- [Käyttöohje](./dokumentaatio/kayttoohje.md)
- [Ohjelman arkkitehtuuri](./dokumentaatio/arkkitehtuuri.md)

## Asennus ja käynnistys
1. Asenna riippuvuudet projektin juurihakemistossa:  

       poetry install


2. Käynnistä peli:

       poetry run invoke start

    Katso [käyttöohje](./dokumentaatio/kayttoohje.md)

## Testaus
Testit suoritetaan komennolla

    poetry run invoke test


Html-muotoisen testikattavuusraportin <i>htmlcov</i>-hakemistoon voi generoida komennolla


    poetry run invoke coverage-report


Koodin tyyliseikat tarkistetaan komennolla


    poetry run invoke pylint

#### TODO
Refaktorointia voisi vielä tehdä. Toiminnallisuus on muuten hyvä mutta olisi hienoa jos tulosnäkymästä voisi suoraan käynnistää uuden pelin.
