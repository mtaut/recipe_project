# Recipe-App

This project is part of **CareerFoundry's Recipe App**, built using Django. It is a web-based application that allows users to create and save recipes in a clean and simple user interface.

## Features

### **User Authentication**

- User authentication with **login** and **logout** functionality
- Application utilizes Django's built-in security, **CSRF protection**
- Protected views ensure only authenticated users can access certain pages within the app

### Recipe Creation

- Users are able to create a recipe within the app
- Recipes are stored in an **SQLite** database
- Saved recipes from user can be viewed within app

### Search Functionality

- Users can search for recipes by ingredient
- Individual recipe details are displayed for each recipe

### Data Analytics and Other

- **Matplotlib** is used to generate statistics and visualizations based on recipe data
- Recipes are automatically rated by difficulty level based on **number of ingredients** and **cooking time**
- **Django Admin Dashboard** is available for managing database entries

## Technologies Used

- **Python** `v3.13.1` (Compatible with `v3.6+`)
- **Django** `v5.1.5`
- **SQLite3** default database
- **HTML, CSS, JavaScript**

## Installation

1. **Clone the repository**

```sh
git clone https://github.com/yourusername/recipe-app.git
cd recipe-app
```

2. **Create and activate a virtual environment**

```sh
python -m venv venv
source venv/bin/activate
# On Windows
venv\Scripts\activate
```

3. **Install Dependencies**

```sh
pip install -r requirements.txt
```

4. **Apply migrations and run the server**

```sh
python manage.py migrate
python manage.py runserver
```
