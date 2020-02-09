# World Cup Challenger

![badge](coverage.svg)

## Intro
This API was built to manage a World Cup, described as Tournament.

## Running with Docker

First, check that you have a docker and a docker-compose on your machine with these commands:

```shell
docker -v
docker-compose -v
```

If not, check this [tutorial](https://docs.docker.com/compose/install/) for installation from the official Docker Docs documents

After the complete installation, you can build the project with this command at the root of the project

```shell
docker build .
```

Warning: This project uses PostgreSQL, so you may have to turn off your local instance of postgresql

To run and access [localhost:8000](localhost:8000):

```shell
docker-compose up
```

If you want to run in the background:

```shell
docker-compose up -d
```

To perform the tests (with the docker in the background):

```shell
docker-compose exec web python manage.py test
```

## Endpoint documentation

All documentation of endpoints are described and built with Postman

You can check [here](https://documenter.getpostman.com/view/6289333/SWTHaaeA?version=latest#intro)
