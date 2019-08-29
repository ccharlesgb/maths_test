# Maths Test

This is my submission for the maths test application. I didn't end up writing 
a front end for this and focussed more on the expandability of the backend a 
JSON REST api first. The API should be able to support an SPA frontend to deliver
the features requested in the project spec.

## Quick-start

The app can be deployed straight away with the docker-compose file present in the repo. I will admit Docker
isn't a technology I was familiar with before so but I was keen to use this task as an opportunity to learn
something new so I spent a bit of time researching how to use it before starting this repo.

The docker-compose setup here is more to aid in enabling you to inspect the applications behaviour than 
a production deploy as the passwords are mostly left as defaults and I just used the default postgres user 
and table.

In order to run the app just run:

```
docker-compose build
docker-compose up
docker exec -it mathstest_web_1 /bin/bash
:/srv/maths_test# maths-test initdb
```

This will build and run the image and then invoke the initdb command in the applications CLI to create
the tables in postgres and create the admin user 

## Authentication

Authentication is done using JSON Web tokens via flask-praetorian. Students can register using the register route
and an admin can then promote them to teacher via the PATCH method on their user id