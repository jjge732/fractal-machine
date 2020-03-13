# Fractal Machine

## File Structure
```
fractal-machine
├── project                          --> directory for package
│    ├── app                         --> directory for main functionality of GUI
│    │   └── __main__.py             --> first file to be run (used for testing as of now)
│    │   └── image_editor.py         --> mainly used for creating images in images directory
│    ├── connection                  --> directory for connection to the postgres database
│    │   └── __init__.py             --> empty init file
│    │   └── config.py               --> file for configuring connection to the database
│    │   └── connection.py           --> used for testing the connection
│    │   └── database.ini            --> holds configurations for the database
│    │   └── setup.py                --> allows easier install?
│    ├── controller                  --> directory for making sql commands in python
│    │   └── __init__.py             --> empty init file
│    │   └── image.py                --> makes changes to images table in postgres
│    │   └── user.py                 --> makes changes to users table in postgres
│    ├── images                      --> directory for holding images made by users
│    │   └── __init__.py             --> empty init file
│    ├── models                      --> directory for housing models for the postgres tables
│    │   └── __main__.py             --> creates tables in postgres
│    ├── sql                         --> directory for holding one time use sql queries
│    │   └── seed.sql                --> file seeding database with data for testing purposes
│    ├── tests                       --> directory for holding tests
│    └── __init__.py                 --> empty init file             
├── .gitignore                       --> basic gitignore
├── create_tables.py                 --> file for creating tables in the database
├── main.py                          --> main file for running the app
├── README.md                        --> this file
├── requirements.txt                 --> states requirements of this project
└── setup.py                         --> file for setting up the module
```

## Setup
TODO: add to this once everything is working

This app requires postgresql to run. To install with homebrew run:
```bash
brew install postgresql
```
To start postgres, run:
```bash
brew services start postgresql
```
And to stop it, run:
```bash
brew services stop postgresql
```
You will also need data in postgres. Run the following to enter postgres:
```bash
psql postgres
```
And the run:
```sql
CREATE DATABASE fractal_machine;
CREATE ROLE postgres;
ALTER ROLE postgres WITH LOGIN;
```
Finally, the project needs to know its location in your file structure in order to run properly.
To provide this information, add to your bash profile by running this command:
```bash
echo "export FRACTAL_MACHINE_ROOT=$(pwd)" >> ~/.bash_profile
source ~/.bash_profile
```

## TODO: (not necessarily all of the following)
- GUI (pygame)
    - functionality
    - aesthetics
- finalize file conversion and get working with input data
- export files to Downloads
- make more image file conversions
- finalize sql tables
- encryption for user passwords

## FAQ
### How do I install homebrew?
Run this command:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```