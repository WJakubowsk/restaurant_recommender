# Intelligent Restaurant Recommender System
This project was implemented for the course Intelligent System Project in winter semester of 2024/25.

## Summary
The project delivers a comprehensive, web-based Intelligent Restaurant Recommender System. This AI-powered system enables users to filter preferences and discover personalized restaurant recommendations tailored to their needs. Featuring an intuitive interface and user-friendly filters, including sustainability-focused options, it simplifies the search for the perfect dining experience.

## How to set up the system
Prerequisites: 
* Python 3.12 with PIP manager
* Node.JS with NPM manager
* Anaconda (optionally for creating Python virtual environment)

1. Set up back-end (Python)
* In root directory, after optionally creating anaconda environment,
install all Python dependencies:
`pip install -r requirements.txt`
* Navigate to `/src` folder and execute:
```
python manage.py migrate # for setting up infrastructure
python manage.py runserver # for exposing back-end
```
* Optionally, you can also load the data about restaurants, using the custom commands based on scripts in `/src/management/commands`. These scripts will populate the database with Restaurant, Reviews and User data from CSV files. To do this:
    - Download the CSV files from [here](TODO) and put them in `/data` folder
    - Execute the following commands:
    ```
    python manage.py load_users --csv-file ../data/yelp_academic_dataset_user_sample.csv
    
    python manage.py load_restaurants --csv-file ../data/yelp_academic_dataset_business_preprocessed.csv

    python manage.py load_reviews --csv-file ../data/yelp_academic_dataset_review_1MLN_filtered.csv
    ```
    The data will be loaded in the database after 6-8 hours.

2. Set up front-end (JavaScript)
After having installed Node.JS and NPM, the only action left to do is install the packages required by the React.JS in the app. To do this, navigate to `/src/react-app/src` folder and execute following commands:
```
npm install # for installing dependencies
npm start # for exposing frontend
```

After both front-end and back-end are set up, navigate to https://127.0.0.1:3000 or https://localhost:3000 to use the system.

## Project structure
The system was built using modular components and with adherence to REST framework. The main logic is implemented in Python/Django, while the frontend part is implemented in JavaScript/React.JS. The core structure contains:
- `/data` - folder to put the data into
- `/src` - folder with the majority of functionalities
- `README.md` - manual for the project (this file)

To dive deeper into the technical intricacies, we shall move to `/src` folder, in which we find:
- `/app` - folder with back-end logic of the app.
- `/authentication` - component for user authentication and log-in functionalities
- `/config` - set of config files for the system
- `/filter` - Review filtering module. The script `review_filter.py` performs offline filtering of the reviews from CSV file.
- `/react-app` - contains the whole front-end infrastructure
- `/templates` - html views of the websites
- `manage.py` - heart of the Django system, executes the logic contained in other directories and sets up the back-end.

## Contributors
- Zuzanna Kotlińska
- Wiktor Jakubowski
- Jakub Żytliński

