
__Using project root dir /var/www/animeservice.pp.ua/__
___


AnimeService WSGI Socket: /etc/systemd/system/animeservice.socket
```
[Unit]
Description=animeservice gunicorn socket

[Socket]
ListenStream=/run/animeservice.sock

[Install]
WantedBy=sockets.target
```

AnimeService WSGI service: /etc/systemd/system/animeservice.service
```
[Unit]
Description=animeservice gunicorn daemon
Requires=animeservice.socket
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/var/www/animeservice.pp.ua/
ExecStart=/var/www/animeservice.pp.ua/.venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/animeservice.sock \
          app.wsgi:application

[Install]
WantedBy=multi-user.target
```

AnimeService ASGI socket: /etc/systemd/system/animeservice_asgi.socket
```
[Unit]
Description=animeservice daphne socket

[Socket]
ListenStream=/run/animeservice_asgi.sock

[Install]
WantedBy=sockets.target
```
AnimeService ASGI service: /etc/systemd/system/animeservice_asgi.service
```
[Unit]
Description=animeservice daphne daemon
After=network.target


[Service]
User=root
Group=www-data
WorkingDirectory=/var/www/animeservice.pp.ua
ExecStart=/var/www/animeservice.pp.ua/.venv/bin/daphne -u /run/animeservice_asgi.sock  app.asgi:application

[Install]
WantedBy=multi-user.target
```

NGINX Settings: /etc/nginx/sites-available/animeservice.pp.ua
```

upstream websocket {
    server unix:/run/animeservice_asgi.sock;
}

server {
  listen 80;
  server_name animeservice.pp.ua www.animeservice.pp.ua;
    location = /favicon.ico { access_log off; log_not_found off; }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/animeservice.sock;
        client_max_body_size 10G;
    }

    location /static/ {
        alias /var/www/animeservice.pp.ua/staticfiles/;
    }

    location /media/ {
        alias /var/www/animeservice.pp.ua/media/;
    }

    location /ws/ {
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_redirect off;
        proxy_pass http://websocket;
    }

}
```

Celery service: /etc/systemd/system/animeservice_celery.service
```
[Unit]
Description=animeservice celery daemon
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/var/www/animeservice.pp.ua
ExecStart=/var/www/animeservice.pp.ua/.venv/bin/celery -A app worker --loglevel=INFO

[Install]
WantedBy=default.target
```