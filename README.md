Service for watching movies and series
===========

Features
--------

* System of subscriptions, likes, rating, reviews
* Search videos by name and tags
* Ability to watch videos with different quality
* Realized feedback functions
* Creating news, text pages
* Internationalization
* Personal customization: styles for video pages, navigation

___

Setup .env fields
------------

```
DEBUG=0
ALLOWED_HOSTS=*
SECRET_KEY=ewnc=your_project_secret_key

REDIS_HOST=redis
REDIS_PORT=6379

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_LOGIN=test@gmail.com
PASSWORD=testpassword
FROM_EMAIL=test@gmail.com

# You can ignore SQL params, when SQLLite will be used

SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=testbase
SQL_USER=testuser
SQL_PASSWORD=testpass
SQL_HOST=127.0.0.1
SQL_PORT=5432

```
___
Docker compose setup
-------------------
Before running __docker-compose up__ create __.env.db__ file with psql environment

```
POSTGRES_USER=testuser
POSTGRES_PASSWORD=testpass
POSTGRES_DB=testbase
```

---
__Project review https://youtu.be/Eqie1PW7sCM__