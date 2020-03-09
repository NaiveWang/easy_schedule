# Easy Schedule Deployment Manual

Through this manual you can deploy this project. Usually it should be deployed on a GNU/Linux PC or Dev Board. If you do not know what project you are going to deploy, read [User Manual](https://github.com/NaiveWang/easy_schedule/blob/master/manual.md) first.

Firstly, clone this repo:

> $ git clone https://github.com/NaiveWang/easy_schedule.git

## Enviroment

As we use `SQLite` as database, there is no need to configure a large stand-alone database. `uWSGI` is used as a server.

### Python & Pips

`Python3` and it's `Pip` is needed, and you may want to use dediceted `virtualenv`. Install these pipes with `pip`:

> $ pip install Flask Flask-Misaka Jinja2 uwsgi

### SQLite

Assume you have installed `sqlite3` on your GNU/Linux host, you will initialize the db file.

> $ sqlite3 db.db3 < db.sql

Now a DB file is created as `db.db3`.

## uWSGI Configuration

### HTTP (Lan)

Http is fit for LAN use.

Open `uwsgi.ini`, delete `https` row and add HTTP config like:

> http = `<IP>`:`<PORT>`

then you can start server by:

> $ uwsgi uwsgi.ini

### HTTPS (Public)

If you want to listen on Public, HTTP could be intercepted by ISP ~especially in China~, so HTTPS is much safer.

Generate a ssl key:

**You May Install `openssl` first**

> $ openssl genrsa -out local.key 2048
> $ openssl req -new -key local.key -out local.csr
> $ openssl x509 -req -days 365 -in local.csr -signkey local.key -out local.crt

Starting steps are the same.
