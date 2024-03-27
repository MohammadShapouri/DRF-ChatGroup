
# Django Rest Framework Chat Group

A chat group like telegram's groups in django rest framework.


## Features
* Creating, retrieving, updating, and deleting user accounts.
* Changing password and resetting password.
* validating user info with OTP code.
* Using celery for running tasks asynchronously.
* Caching data in Redis.
* Different access levels and responses based on the user account type that sends requests. (Sperusers and staffs have the same access level as superusers in
  Django admin panel.)
* Creating, retrieving, updating, and deleting groups
* Different access levels for managing groups based on user type (owner, admin, or normal user).
* Each group can have one owner and more than one admin
* Creating public and private groups



## Installation
__If you use windows, instead of using '_python3 -m_' and '_python3_', use '_python -m_' and _python_' in commands.__
* Run the following command in your terminal to clone this project or download it directly.
    ```
    $ git clone git@github.com:MohammadShapouri/DRF-UserAccount.git
    ```
* Install Redis and PostgreSQL.

* Navigate to the project folder (DRF-UserAccount folder).

* Create a .env file and fill it. (.env.sample is a sample file that shows which fields the .env file has.)

* Run the following command to create virtualenv. (If you haven't installed virtualenv package, you need to install virtualenv package first).
    ```
    $ python3 -m virtualenv venv
    ```

* Activate virtualenv.
    > Run the following command in Linux
    ```
    $ source venv/bin/activate
    ```
    > Run the following command in windows
    ```
    $ venv/Scripts/activate
    ```


* Run the following command to install the required frameworks and packages.
    ```
    $ pip install -r requirements.txt
    ```

* Navigate to the config folder.

* Run the following commands one by one to run the project.
    ```
    $ python3 manage.py makemigrations
    $ python3 manage.py migrate
    $ python3 manage.py runserver
    ```

* Run the following command in the folder that contains manage.py to run celery.
  ```
    python -m celery -A config worker -l info

  ```


## Document
### Database Tables Schema Picture:
![database tables schema picture](https://github.com/MohammadShapouri/DRF-ChatGroup/blob/main/docs/database-tables-schema.png?raw=true)

### Swagger
* Swagger is available in _127.0.0.1:8000_ when you run project.
![swagger preview](https://github.com/MohammadShapouri/DRF-ChatGroup/blob/main/docs/ChatGroup-swagger-preview.png?raw=true)

### Postman
* Postman data is available in _docs_ folder. You can import and use it.




## Things to do in the future
* Dockerizing project.
* Creating CRUD methods and classes using Django-channels for managing messages in each group.
* Customizing Django admin panel.

