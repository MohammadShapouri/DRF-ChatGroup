
# Django Rest Framework Chat Group

A chat group like telegram's groups in django rest framework.


## Features
* Creating, retriving, updating and deleting user account.
* Changing password and reseting password.
* validating user info with OTP code.
* Using celery for running tasks asynchronously.
* Different access level and responses based on the user account type which sends request. (Sperusers and staffs have the same access level as superusers in
  django admin panel.)
* Creating, retriving, updating and deleting groups
* Different access levels for managing group base on user type (owner, admis or normal user).
* Each group can have one owner and more than one admin
* Creating public and private groups



## Installation
__If you use windows, instead of using '_python3 -m_' and '_python3_', use '_python -m_' and _python_' in commands.__
* Run the following command in your teminal to clone this project or download it directly.
    ```
    $ git clone git@github.com:MohammadShapouri/DRF-UserAccount.git
    ```
* Install redis and postgresql.

* Navigate to the project folder (DRF-UserAccount folder).

* Create a .env file and fill it. (.env.sample is a sample file which shows which fields should .env file have.)

* Run the following command to create virtualenv. (If you haven't install virtualenv package, you need to install virtualenv package first).
    ```
    $ python3 -m virtualenv venv
    ```

* Activate virtualenv.
    > Run the following command in linux
    ```
    $ source venv/bin/activate
    ```
    > Run the following command in windows
    ```
    $ venv/Scripts/activate
    ```


* Run the following command to install required frameworks and packages.
    ```
    $ pip install -r requirements.txt
    ```

* Navigate to config folder.

* Run the following commands one by one to run the project.
    ```
    $ python3 manage.py makemigrations
    $ python3 manage.py migrate
    $ python3 manage.py runserver
    ```

* Run the following command in the folder which contains manage.py to run celery.
  ```
    python -m celery -A config worker -l info

  ```


# Things to do in future
* Dockerizing project. (Though it must be Dockerized after creating project.)
* Creating CRUD methods and classes using django-channels for managing messages in each group.
* Writing test cases.
* Customizing django admin panel.

