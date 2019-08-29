# Maths Test

This is my submission for the maths test application. I didn't end up writing 
a front end for this and focussed more on the expandability of the backend a 
JSON REST api first. The API should be able to support an SPA frontend to deliver
the features requested in the project spec.

## Quick-start

The app can be deployed straight away with the docker-compose file present in the repo. Docker
isn't a technology I was familiar with before (I am currently deploying with IIS) so but I was keen to use this task
 as an opportunity to learn something new so I spent a bit of time researching how to use it before starting this repo.

Citation on what I based docker set up on: 

```
https://medium.com/@smirnov.am/running-flask-in-production-with-docker-1932c88f14d0
```

This setup seemed to be the best setup as lot of online resources still use the Flask debug web server which is
not suitable for production.

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
the tables in postgres and create the admin user.

There will also be an adminer image running as well so you can inspect the status of the database.

There is a postman collection included in this repo which should go through the whole process of:

1. Adding a test as a teacher
2. Adding a question to that test
3. Enabling the test for use by students
4. Taking the test as a student
5. Getting your mark.

You may find you need to refresh the {{adm_jwt}} and the {{student_jwt}} tokens in the postman collection variables and
{{host}} should be set to 'http://localhost:80' if you are running the docker containers.

## Running Tests

The tests can be run using pytest:

```
 pytest maths_app
```

## Authentication

Authentication is done using JSON Web tokens via flask-praetorian. Students or teachers can register using the 
register route and an admin can then promote them to teacher via the PATCH method on their user id.

## Data Model

### User

The user represents a registered user to the app. It contains the username, hashed password and contact details of
the user. It has a simple 1->1 relationship with the Role table as well to restrict permissions.

### Test

A test is defined as having a name such as "Algebra" and a pass fraction which is the percentage needed for an
attempt to be considered a pass. A test has N questions. A tests enabled state determines if it is "live" in the
application. An enabled app can be seen and taken by students. A disabled one is hidden from them.

### Question

A question has one test. It has a body which I imagined in any front-end could support some kind of 
equation type-setting library such as MATHJAX in order to make the questions display nicely.

### Option

An option has 1 question. An option is one choice in the multiple choice question. It can be correct or 
incorrect. I haven't yet had time to add validation that there must be one correct/incorrect answer to a test
but that would happen when a test is enabled.

### Attempt

An attempt represents a student 'taking' the test. The start and end time is logged and when the student has 
submitted all their answers the "mark" field is filled in. I didn't have time to include a pass/fail but this could be
very easily added by adding another field to the Attempt model

### Answer

An answer is a chosen option for a given test attempt and is used to mark the test once each question has an answer.

