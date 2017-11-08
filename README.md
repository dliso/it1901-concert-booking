# IT1901 Project 1
## Festival Management System

This is a web app for managing festivals.

### Requirements
- Python 3.6
- npm
- git

### Setup
Execute the following commands:

Mac/Linux:
- `git clone https://github.com/dliso/it1901-concert-booking.git`
- `cd it1901-concert-booking`
- `npm install -g bower`
- Optional:
  - `python3 -m virtualenv venv`
  - `source venv/bin/activate`
- `pip3 install -r requirements.txt`
- `./manage.py bower install`
- `./manage.py collectstatic`
- `./manage.py makefakedata` to fill the database with randomish data
- `./manage.py runserver`

The application should now be up and running at [localhost:8000](http://localhost:8000).
A bunch of users have been created so you can test the system, e.g. `admin`, `booking_manager_1`, `chief_booking_manager_1` and `pr_manager_1`, all with the password `qweqweqwe`.
