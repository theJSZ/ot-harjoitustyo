# Lopullista julkaisua vastaava vaatimusmäärittely  
## Sovelluksen tarkoitus  
Sovellus on tietokoneversio Yatzy-pelistä.  

## Käyttöliittymä
Pelaajia voi olla yhdestä neljään.  
Vanhoja tuloksia voi katsella.  
Käyttäjä nimeää jokaisen pelaajan.  
Sovelluksen päänäkymä esittää viittä noppaa ja pistetaulukkoa.

<img src="./images/Yatzy_gui.png" width="300">  

Tuloslistassa näkyy sekä merkatut tulokset että heitetyillä nopilla tarjolla olevat tulokset. Pitoon laitetut nopat on merkitty vihreällä kehyksellä.

## Toiminnallisuus  
Ohjelma toimii oikein, esim. jokaisella vuorolla pelaajalla on yhdestä
kolmeen heittoa.  
Heitoilla 2 ja 3 voi valita mitä noppia pyörittää.  
Tuloksen sijoittaminen pistetaulukkoon antaa oikeita tuloksia.  
Olemassaolevan tuloksen päälle ei voi sijoittaa uutta, muutenkaan väärissä paikoissa klikkaaminen ei aiheuta vääriä tapahtumia.  

Pelattujen pelien tuloksia säilytetään tietokannassa; vanhoja tuloksia voi nähdä heti käynnistyksen jälkeen tai pelin loputtua. Vanhojen tulosten yhteydessä kerrotaan koko tietokannan paras tulos ja Grand Championiksi nimetään sen pelannut pelaaja. Tuloslistoja voi selata nuolinäppäimillä vasemmalle ja oikealle.

<img src="./images/result_view.png" width="200">
