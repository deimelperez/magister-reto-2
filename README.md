# magister-reto-2

## Challenge

    A partir de esta web <http://www.madrid.org/cs/Satellite?pagename=ICMFramework/Comunes/Logica/ICM_WrapperGetion&op=PCIU_&language=es&c=CM_ConvocaPrestac_FA&cid=1354822557475&nombreVb=listas&other=1> se necesita:

    - Por cada fila obtener el PDF que enlaza
    - Crear una funcionalidad que extraiga de cada PDF el listado de personas diferentes junto con el resto de datos y que se creen normalizados en tantas tablas como sean necesarios.

## WARNING: This install it's for demostration and development purposes, it's not intended for deploy

## Install and Config

    pip install -r requirements.txt

### It's necessary to install java and added to path

### It's necessary to install PostgreSQL up and running in localhost:5432 with the following config:

    DB name: reto2,
    DB user: postgres,
    PASSWORD: 1234,

## Método de uso

    python manage.py runserver
