# Ravintolasovellus

Sovelluksessa näkyy tietyn alueen ravintolat, joista voi etsiä tietoa ja lukea arvioita. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.
+ = toteutettu toiminto
- = toteuttamaton toiminto

+ Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.
- Käyttäjä näkee ravintolat kartalla ja voi painaa ravintolasta, jolloin siitä näytetään lisää tietoa (kuten kuvaus ja aukioloajat).
+ Käyttäjä voi antaa arvion (tähdet ja kommentti) ravintolasta ja lukea muiden antamia arvioita.
+ Ylläpitäjä voi lisätä ja poistaa ravintoloita sekä määrittää ravintolasta näytettävät tiedot.
+ Käyttäjä voi etsiä kaikki ravintolat, joiden kuvauksessa on annettu sana.
+ Käyttäjä näkee myös listan, jossa ravintolat on järjestetty parhaimmasta huonoimpaan arvioiden mukaisesti.
+ Ylläpitäjä voi tarvittaessa poistaa käyttäjän antaman arvion.
- Ylläpitäjä voi luoda ryhmiä, joihin ravintoloita voi luokitella. Ravintola voi kuulua yhteen tai useampaan ryhmään.

# Sovelluksen käyttö

Riippuvuudet:
requirements.txt

Tietokannan rakenne: 
schema.sql 

Tietokannan luonnin yhteydessä luodaan kaksi käyttäjää: 

Peruskäyttäjä
tunnus: user
salasana: user

Admin-käyttäjä
tunnus: admin
salasana: admin
