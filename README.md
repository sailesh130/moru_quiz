
#  Flask Quiz App

It is a simple quiz app based on flask restful api.




## Requirements
- python v3
- postgres 12



## Setup
- cp .env_sample .env
- assign SQLALCHEMY_DATABASE_URI,SECRET_KEY ,JWT_SECRET_KEY in .env file




## Run
- Run export FLASK_ENV=development for development  and export FLASK_ENV=production for production.
- Run the flask app using python3 run.py







## Endpoints
### 1) /signup
- to register user, this endpoint is used
- post request with body data as below
```
{
    "user_data":
    {
        "username":"ram",
        "email":"ram@gmail.com",
        "password":"1234567svsd",
        "first_name":"ram",
        "last_name":"hari
    }
    ,
    "is_admin":false
}
```
### 2) /login
- to login user, this endpoint is used
- post request with body data as below
```
{
        "email":"ram@gmail.com",
        "password":"1234567svsd",
}
```
### 3) /category/id
- only accessableto admin user
- to create,edit and delete category this endpoint is used.
- id is category id in above route
- to create category, post request to endpoint /category  with body data as below 

```
{
"name":"national"
}
```
### 4) /question/id
- only accessable to admin user
- to create,edit and delete question this endpoint is used.
- id is question id in above route
- to create question , post requestto endpoint /question with body data as below 

```
{
    "category":"category_id",
    "question_text":"actual question",
     "marks":"marks for each question"
}
```
### 5) /choice/id
- only accessable to admin user
- to create,edit and delete choice this endpoint is used.
- id is choice id in above route
- to create choice , post request to endpoint /choice  with body data as below 

```
{
    "choice_text":"actual choice value",
    "question" :"question_id",
    "is_correct" :"boolean value fro each choice"
}
```
### 6) /list_questions/id
- only accessable to both normal user and normal user
- given category id, to view question in each category this endpoint is used 

### 7) /play/id
- given category id, to view unattempt question in each category this endpoint is used 
- post request to end point /play with body data as below to play quiz

```
{
        "question_pk" :"question id",
        "category_pk" :"category id",
        "choice_pk" :"choice id"
}
```

### 8) /score
- to view score this endpoint is used




