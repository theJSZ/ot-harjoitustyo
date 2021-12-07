# Yatzy

Sovellus on Yatzy-peli yhdestä neljään pelaajalle.

## Dokumentaatio
- [Vaatimusmäärittely](./dokumentaatio/vaatimusmaarittely.md)
- [Työaikakirjanpito](./dokumentaatio/tuntikirjanpito.md)
- [Käyttöohje](./dokumentaatio/kayttoohje.md)

## Käynnistys

Komento 'poetry run invoke start' käynnistää pelin. Katso [käyttöohje](./dokumentaatio/kayttoohje.md)

## Testaus

Komento 'poetry run invoke test' suorittaa testit

Komento 'poetry run invoke coverage-report' generoi kattavuusraportin html-muodossa

Komento 'pylint src' tarkistaa koodin tyyliseikat annettujen määritelmien mukaan

#### TODO
Tulokset eivät päivity näkyviin käyttöliittymään vaan vasta pelin päätyttyä terminaaliin. Koodin rakenteessa todennäköisesti huonoja ratkaisuja
