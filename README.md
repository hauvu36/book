### BookStore API

## Prerequisites
- Docker (required)
- Docker Compose (required)


## Installation
# 1. Clone source code
- git clone https://github.com/hauvu36/book.git

# 2. Access source code and install
- Run: cd book
- Create logs folder inside book/api/ folder
- Create .env file inside book folder, refer to the .env.template file
- Create .env file inside book/api/config/settings folder, refer to the book/api/config/settings/.env.template file
- Create JWT key,
  Run: cd api
  Run: openssl genrsa -out jwt_api_key 1024
  Run: openssl rsa -in jwt_api_key -pubout -out jwt_api_key.pub
- Inside book folder
  Run: docker compose build
  Run: docker compose up


### Description of the API's functionality
 - POST v1/auth/registration/ : Allows new user registration
 - POST v1/auth/login/ : Allow users to log in
 - POST v1/auth/refresh/ : Allow users to use refresh token to generate new access token and new refresh token.
 - POST v1/auth/password/change/ : Allow users to change their password
 - POST v1/book/ : Allow users to create a new book
 - PATCH v1/book/{book_id}/ : Allow users to update existing book, including title, author, publish_date, ISBN, and price
 - PATCH v1/book/cover-image/{book_id}/ : Allow users to update cover image for the particular book
 - GET v1/book/ : Allow users to get list of existing books
 - GET v1/book/{book_id}/ : Allows users to get detailed information of a book
 - DELETE v1/book/{book_id}/ : Allows users to delete the particular book


### How to use API endpoint
- Go to swagger site: http://13.251.169.198/docs/
- After getting access token from response of api login, please click "Authorize" button (refer to Image 1)
  and pass "Bearer + access token"(there is a space between Bearer character and access token) into
  "Available authorizations" section(refer to Image 2) , click "Authorize" button to login.
  Done. You are authenticated, Now you can test other apis
  Image 1: https://drive.google.com/file/d/1YkLzONaAtYpQW_beiEwsJm68IEdmbbrm/view
  Image 2: https://drive.google.com/file/d/1FpX5W-GC40l3-rj93woeGVapO8apr0pG/view
- You can test any GET method without authenticated permission (this is requirement from your side)


### Technical choices
- Python 3.8
- Django Rest Framework 3.10.3
- JWT token
- Django 2.2.7
- Docker/Docker compose
- Postgres 14
- Redis
- Nginx

### Schema database
https://drive.google.com/file/d/179dgiUuqhDQDBsRPL-oDHSFIqnLlOM0j/view


