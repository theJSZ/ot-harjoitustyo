# Yatzy

Sovellus on Yatzy-peli yhdestä neljään pelaajalle.
[Vko 6 Release](https://github.com/theJSZ/ot-harjoitustyo/releases/tag/viikko6)

## Dokumentaatio
- [Vaatimusmäärittely](./dokumentaatio/vaatimusmaarittely.md)
- [Työaikakirjanpito](./dokumentaatio/tuntikirjanpito.md)
- [Käyttöohje](./dokumentaatio/kayttoohje.md)
- [Alustava arkkitehtuuri](./dokumentaatio/arkkitehtuuri.md)

## Käynnistys
1. Asenna riippuvuudet projektin juurihakemistossa komennolla 'poetry install'
2. Komento 'poetry run invoke start' käynnistää pelin. Katso [käyttöohje](./dokumentaatio/kayttoohje.md)

## Testaus

Komento 'poetry run invoke test' suorittaa testit

Komento 'poetry run invoke coverage-report' generoi kattavuusraportin html-muodossa

Komento 'pylint src' tarkistaa koodin tyyliseikat annettujen määritelmien mukaan

#### TODO
Refaktorointi!!
Pelin pitäisi loppua nätimmin, nyt se vain sulkee itsensä kun viimeinen pelaaja lopettaa viimeisen vuoronsa
