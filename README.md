# Bike Rental Project 🚲

This is a Django-based web application for a bike rental service. This project allows users to browse available bikes, rent them, and leave reviews. It also includes user authentication and a profile page for users to manage their rentals. This project was developed by a Code Institute student as a learning exercise.

## Project Features

* **User Authentication**: Users can sign up, log in, and log out. The application uses `django-allauth` for handling authentication.

* **Bike Listings**: A list of available bikes is displayed on the homepage. Users can sort the bikes by name, type, size, price, and rating.

* **Bike Details**: Each bike has a detail page with more information, including a description, its availability status, and user reviews.

* **User Profiles**: Each user has a profile page that displays their active rentals and rental history.

* **Rental System**: Authenticated users can rent available bikes. The system tracks active and past rentals.

* **Review and Rating System**: Users can leave reviews and ratings for bikes they have rented. The average rating for each bike is displayed on the bike listing and detail pages.

## Application Screenshots

Below are some screenshots of the application in action.

**Homepage**
![Bike Rental Project Homepage](/static/media/homepage.png)

**Bike Detail Page**
![Bike Detail Page](/static/media/bike-detail.png)

**User Sign Up Page**
![User Sign Up](/static/media/user-signup.png)

**User Profile**
![User Profile](/static/media/user-profile.png)

**Admin Interface**
![Admin Interface](/static/media/admin-interface.png)

## ERD Diagram

Here is the Entity-Relationship Diagram for the project, showing the relationships between the different models:

```erDiagram
    USER {
        int id PK
        string username
        string password
        string first_name
        string last_name
        string email
    }
    PROFILE {
        int id PK
        int user_id FK
        date date_of_birth
    }
    BIKE {
        int id PK
        string name
        string type
        string description
        string size
        bool is_available
        decimal price_per_hour
        string featured_image
    }
    RENTAL {
        int id PK
        int user_id FK
        int bike_id FK
        datetime start_time
        datetime end_time
        decimal total_cost
    }
    REVIEW {
        int id PK
        int bike_id FK
        int user_id FK
        int rating
        text comment
        datetime created_at
    }

    USER ||--o{ PROFILE : "has"
    USER ||--o{ RENTAL : "makes"
    USER ||--o{ REVIEW : "writes"
    BIKE ||--o{ RENTAL : "is rented in"
    BIKE ||--o{ REVIEW : "is reviewed in"
```
![ERD diagram graphical representation](/static/media/erd-diagram.png)
In the diagram, user information is split between the `USER` model (which contains `first_name` and `last_name`) and the associated `PROFILE` model (which contains `date_of_birth`). All of these fields are implemented during registration.

## Testing

### Manual Testing

The following table outlines the manual tests conducted for this project.

| **Feature** | **Test Case** | **Expected Outcome** | **Actual Outcome** | 
|---|---|---|---|
| User Authentication | Register a new user with valid information. | User is successfully registered and logged in. | ✅ | 
| User Authentication | Register a new user with an existing username. | An error message is displayed, and registration fails. | ✅ | 
| User Authentication | Register a new user younger than 14 years old. | An error message is displayed, and registration fails. | ✅ | 
| User Authentication | Register a new user older than 90 years old. | An error message is displayed, and registration fails. | ✅ | 
| User Authentication | Login with a valid username and password. | User is successfully logged in. | ✅ | 
| User Authentication | Login with an invalid username or password. | An error message is displayed, and login fails. | ✅ | 
| User Authentication | Logout from an authenticated session. | User is successfully logged out. | ✅ | 
| Bike Rentals | Rent an available bike. | The bike is marked as unavailable, and the rental is added to the user's profile. | ✅ | 
| Bike Rentals | Verify that unavailable/rented bikes do not appear on the main list. | Only bikes with `is_available=True` are displayed to the user. | ✅ | 
| Bike Rentals | Attempt to rent a bike while having an active rental. | The user is notified that they already have an active rental. | ✅ | 
| Bike Rentals | Return a rented bike. | The bike is marked as available, and the rental is moved to the user's rental history with a calculated cost. | ✅ | 
| Reviews | Leave a review for a bike. | The review is added to the bike's detail page. | ✅ | 
| Reviews | Edit an existing review. | The review is updated on the bike's detail page. | ✅ | 
| Reviews | Delete an existing review. | The review is removed from the bike's detail page. | ✅ | 

### Automated Testing

Automated tests are implemented using Django's built-in testing framework and Jest for frontend JavaScript.

* **Backend Tests**:
  * `reviews/tests.py`: Contains tests for the `Review` model and the `DeleteReview` view. These tests ensure that reviews are created correctly, that ratings are validated, and that users can delete their own reviews.
  * `rentals/tests.py`: Includes tests for the `create_rental` view. These tests verify that authenticated users can rent available bikes and that users with active rentals cannot rent another bike.

* **Frontend Tests**:
  * `static/js/star-rating.test.js`: Contains Jest tests for the star rating component on the review form. These tests ensure that the star rating functionality works as expected, including initialization, user interaction (clicking and hovering), and updating the hidden input value.

### Code Validation

#### Python Linter (Flake8)
All Python code was checked for errors and adherence to the PEP 8 style guide using the **Flake8** linter in Visual Studio Code. No errors were reported.

#### W3C Validators
The HTML and CSS files were validated to ensure they meet the latest web standards.
* **HTML:** All HTML pages were validated using the [W3C Markup Validation Service](https://validator.w3.org/).
* **CSS:** The `style.css` file was validated using the [W3C CSS Validation Service](https://jigsaw.w3.org/css-validator/).

## Application Loading Speed

To ensure a good user experience, the application's loading speed was tested using the Chrome Lighthouse report.
![Bike Rental Project Lighthouse Report](/static/media/lighthouse-report.png)

## Deployment

### Local Setup

1. **Fork and Clone the Repository:**
   First, fork the [original repository](https://github.com/ihorsniezhko/bike-rental-project.git) to your own GitHub account. Then, clone your forked repository to your local machine:
   ```bash
   git clone [https://github.com/your-username/bike-rental-project.git](https://github.com/your-username/bike-rental-project.git)
   cd bike-rental-project
   ```

2. **Create the Database:**
   Navigate to the [Code Institute database page](https://dbs.ci-dbs.net/) to create your PostgreSQL database. You will receive the `DATABASE_URL` via email.

3. **Set Up Environment Variables:**
   * Create a file named `env.py` in the root directory of the project.
   * Add `env.py` to your `.gitignore` file to ensure it's not committed to version control.
   * In `env.py`, add your secret variables:
     ```python
     import os
     
     os.environ.setdefault("DATABASE_URL", "your-database-url-from-email")
     os.environ.setdefault("SECRET_KEY", "your-own-strong-secret-key")
     os.environ.setdefault("CLOUDINARY_URL", "your-cloudinary-url")
     ```

4. **Install Dependencies:**
   Install all required packages from the `requirements.txt` file.
   ```bash
   pip install -r requirements.txt
   ```

5. **Run Migrations and Create Superuser:**
   Apply the database migrations to create the necessary tables and create an admin user.
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run the Application Locally:**
   ```bash
   python manage.py runserver
   ```

### Heroku Deployment

1.  **Install WhiteNoise:**
    WhiteNoise allows your application to serve its own static files in production.
    ```bash
    pip install whitenoise
    pip freeze > requirements.txt
    ```

2.  **Update `settings.py` for Static Files:**
    In your `bike_rental/settings.py` file, make the following changes:
    * Add `whitenoise.middleware.WhiteNoiseMiddleware` to your `MIDDLEWARE` list, right after the `SecurityMiddleware`.
    * Define `STATIC_ROOT`.

    ```python
    # settings.py

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this line
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        # ... other middleware
    ]

    # ... at the bottom of the file, with other static file settings
    STATIC_URL = '/static/'
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    ```

3. **Prepare for Deployment:**
   * In your `settings.py` file, ensure the `DEBUG` value is set to `False`.
   * Commit and push your changes (including the updated `requirements.txt` and `settings.py`) to your GitHub repository:
     ```bash
     git add .
     git commit -m "Configure WhiteNoise and prepare for deployment"
     git push
     ```

4. **Create a Heroku App:**
   Make sure you have the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed and are logged in.
   ```bash
   heroku create your-app-name
   ```

5. **Connect Heroku to GitHub:**
   * In your Heroku app dashboard, navigate to the `Deploy` tab.
   * Under `Deployment method`, click `GitHub` and connect your repository.

6. **Set Up Heroku Config Vars:**
   * In your Heroku app dashboard, go to `Settings` > `Reveal Config Vars`.
   * Add the following variables:
     * `DATABASE_URL`: The URL for your **Code Institute database**.
     * `CLOUDINARY_URL`: Your Cloudinary URL.
     * `SECRET_KEY`: Your Django secret key.
     * `HEROKU_HOSTNAME`: The hostname of your deployed Heroku app (e.g., `your-app-name.herokuapp.com`).

7. **Deploy and Run Migrations:**
   * On the `Deploy` tab, trigger a `Manual deploy` of the `main` branch.
   * Once the deploy is complete, run migrations:
   ```bash
   heroku run python manage.py migrate --app your-app-name
   ```
Your app should now be live.

## Future Features and Improvements

* **Payment Integration:** Integrate a payment gateway like Stripe or PayPal to handle rental payments directly through the website.
* **Advanced Search and Filtering:** Implement a search bar to find bikes by name and add more advanced filtering options, such as filtering by availability on a specific date.
* **User-to-User Messaging:** Create a simple messaging system to allow users to ask questions about a bike before renting.
* **Admin Dashboard Enhancements:** Improve the admin panel with more detailed analytics, such as rental statistics, popular bikes, and user activity reports.
* **Booking Calendar:** Instead of immediate rentals, allow users to book bikes for specific dates and times in the future using a calendar interface.

## Credits and Resources

This project was developed by a Code Institute student. The following resources were instrumental in the development process:

* **Django Documentation**: The official Django documentation was an essential resource for understanding the framework's features and best practices.
  * [Django Documentation](https://docs.djangoproject.com/en/4.2/)

* **Code Institute database**: The project uses a PostgreSQL database provided by Code Institute.
  * [Code Institute](https://codeinstitute.net)

* **django-allauth**: This package was used for user authentication.
  * [django-allauth Documentation](https://django-allauth.readthedocs.io/en/latest/)

* **django-crispy-forms**: This package was used to make the forms look better.
  * [django-crispy-forms Documentation](https://django-crispy-forms.readthedocs.io/en/latest/)

* **django-summernote**: This package was used for the rich text editor in the review and bike description fields.
  * [django-summernote GitHub Repository](https://github.com/summernote/django-summernote)

* **Cloudinary**: This service was used for storing and serving the bike images.
  * [Cloudinary Documentation](https://cloudinary.com/documentation)

* **Heroku**: The project is deployed on Heroku.
  * [Heroku Documentation](https://devcenter.heroku.com/)

* **Bootstrap**: The frontend is built with Bootstrap 5.
  * [Bootstrap Documentation](https://getbootstrap.com/docs/5.3/)

* **Jest**: Used for testing the frontend JavaScript code.
  * [Jest Documentation](https://jestjs.io/docs/en/getting-started)

* **Mermaid**: Used for creating the ERD diagram.
  * [Mermaid Documentation](https://mermaid.js.org/)

### Acknowledgements

* A big thank you to the **Code Institute** mentors for their guidance and support throughout this project.
* Countless tips and solutions were found on **Stack Overflow**, and I'm grateful to the community for sharing their knowledge.
