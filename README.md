
# B&C serviceformulier
Description

## Tech Stack
[Turbo JS](https://turbo.hotwired.dev/), [SCSS](https://sass-lang.com/)

## Get Started 🚀
To get started, install [Docker](https://www.docker.com/)

### Start MOR core application
https://github.com/forza-mor-rotterdam/mor-core

### Create local dns entry
Add '127.0.0.1  mbc.mor.local' to your hosts file

### create docker networks
~~~bash
    docker network create mbc_network
    docker network create mor_bridge_network
~~~

### Build and run Docker container
~~~bash
    docker compose build

    docker compose up
~~~

This will start a webserver.

In terminal go to 'app/frontend' and start front-end and watcher by typing

~~~
    npm run watch
~~~


Authorize via the Django admin: http://mbc.mor.local:8001/admin/
You can view the website on http://mbc.mor.local:8001.
