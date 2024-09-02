## Changelog REST API

This application lets you easli manage changelogs for your products.
🧐 Features

Here're some of the project's best features:
- Create user 'http://0.0.0.0:8000/api/v1/
- Listing and creating users 'http://0.0.0.0:8000/api/v1/users'
- Listing and creating products 'http://0.0.0.0:8000/api/v1/products'
- Get all updates for your product 'http://127.0.0.1:8000/api/v1/products/{product_id}/updates/'
- Listing and creating updates 'http://0.0.0.0:8000/api/v1/updates'
- Creating points for update 'http://0.0.0.0:8000/api/v1/updates/{update_id}/points'
- Listing points 'http://0.0.0.0:8000/api/v1/points'
🛠️ Installation Steps:

1. Requirements

-docker

-docker-compose

-python 3.11

4. Envs
clon project on to your machine 

rename .env-default => .env 

fill your .env file with your info

6. Run

in your terminal run docker-compose up --build 

7. Run test

docker-compose exec backend pytest

🛡️ License:
This project is licensed under the Beerware licence
