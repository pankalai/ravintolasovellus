# Ravintolasovellus

Sovelluksessa näkyy tietyn alueen ravintolat, joista voi etsiä tietoa ja lukea arvioita. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.

Toteutetut toiminnallisuudet:

- Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen. <br>
- Käyttäjä voi antaa arvion (tähdet ja kommentti) ravintolasta ja lukea muiden antamia arvioita.<br>
- Käyttäjä voi etsiä kaikki ravintolat, joiden kuvauksessa on annettu sana.<br>
- Käyttäjä näkee myös listan, jossa ravintolat on järjestetty parhaimmasta huonoimpaan arvioiden mukaisesti.<br>
- Käyttäjä näkee ravintolat kartalla ja voi painaa ravintolasta, jolloin siitä näytetään lisää tietoa (kuten kuvaus ja aukioloajat).<br>
- Ylläpitäjä voi lisätä ja poistaa ravintoloita sekä määrittää ravintolasta näytettävät tiedot.<br>
- Ylläpitäjä voi tarvittaessa poistaa käyttäjän antaman arvion.<br>
- Ylläpitäjä voi luoda ryhmiä, joihin ravintoloita voi luokitella. Ravintola voi kuulua yhteen tai useampaan ryhmään.<br>

# Sovelluksen käyttö
Sovellus ei ole testattavissa Fly.iossa 

## Virtuaaliympäristön luominen
Komento: python3 -m venv venv

## Riippuvuudet
requirements.txt  
Komento: pip install -r requirements.txt

## Tietokannan rakenne
schema.sql  
Komento: psql < schema.sql

Tietokannan rakenteen luonnin yhteydessä luodaan admin-käyttäjä:

tunnus: admin <br>
salasana: admin

## Ympäristömuuttujat (.env)
DATABASE_URL  
SECRET_KEY

## Käynnistys
flask run

