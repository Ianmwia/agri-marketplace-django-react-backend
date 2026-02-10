# Agriculture Marketplace

This project is a comprehensive B2C digital ecosystem built with django , designed to bridge a gap between farmers, buyers and agricultural experts. It streamlines the farm to table supply chain while proving a dedicated communication channel for technical farm support.

## Tech Stack

![Django](https://img.shields.io/badge/Django-%23092E20.svg?logo=django&logoColor=white)

- **Backend** python3, Django
- **Frontend** Django Html
- **Database** Sqlite3
- **Authentication** Django Auth
- **Libraries and dependencies** Available in the requirements.txt file
- **APIs** - Django Rest Framework
- **API Documentation** - Integrated Swagger

## Features

- Account creation - Secure account creation and authentication with django
- User Authentication and validation
- Multi-Role User management
* Farmers - the backbone of the platform, they produce, manage icoming orders and seek expert advice
* Buyers - consumers or businesses looking to purchase fresh produce directly from the source
* Extension Officers - proffessionals who provide technical support and respond to farm issue reports

- Marketplace and order Workflow
* Produce Listings - farmers can create, edit and manage digital catalog of harvests
* Order management - Buyers can place orders directly

## Api Documentation

This Project includes a fully documented REST API for front end integration with third party services

* Interactive UI : Access to the api playground at

```api
/swagger/
```

* Endpoints : Include full CRUD for Account Creation, Produce, and Order life cycle management

## Live demo

_Coming Soon_

## Installation and Setup

1. Clone the repository

```bash
git clone https://github.com/Ianmwia/agri-marketplace-django-react-backend.git
```

2. Open the folder in a terminal

```git
cd photo_project

```
3. Create the virtual environment

```git
source venv/scripts/activate
```

4. Install the dependencies

```git
pip install -r requirements.txt
```

5.Open in vs code and run the server

```python
python manage.py runserver
```

## Contributing

- Contributions are welcome
- Feel Free to Fork the Repository and  Submit a pull request

- If there are any issues or comments please raise a new Issue