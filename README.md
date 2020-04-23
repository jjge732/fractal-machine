# Fractal Machine

## File Structure
```
fractal-machine
├── project                          --> directory for package
│    ├── app                         --> directory for main functionality of app 
│    │	 ├── routes 				         --> directory for aws functions
│    │   |	└── __init__.py          --> empty init file 
│    │   |	└── __main__.py          --> used for testing aws functions 
│    │	 |  └── aws.py               --> holds aws functions for storage capabilties
│    │   └── __init__.py             --> empty init file
│    │   └── __main__.py             --> used for testing as of now
│    │   └── boardpiece.py           --> class that creates boardpieces 
│    │   └── game.py                 --> old version of GUI with just b/w tiles 
│    │   └── gamebutton.py           --> class that creates the buttons of the game 
│    │   └── image_editor.py         --> mainly used for creating images in images directory
│    │   └── Inlanders Demo.otf      --> one of the fonts used in the game
│    │   └── Jelly Crazies.ttf       --> font used for game.py, the inital version of the GUI
│    │   └── game_color.py           --> / main file to run, is the main script for the GUI /
│    │   └── webscrap_forcolors.py   --> web scrapping script to get color rgb and hex values
│    │   └── RGB_HEX.xlsx            --> storage of rgb and hex values 
│    │   └── colortile.py            --> class that create the color tiles 
│    │   └── colortile.py            --> class that create the color tiles   
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
├── main.py                          --> used for testing 
├── README.md                        --> this file
├── requirements.txt                 --> states requirements of this project
└── setup.py                         --> file for setting up the module
```

## Setup

Before running, complete this step in order to generate the SVG file:
The project needs to know its location in your file structure in order to run properly.
To provide this information, add to your bash profile by running this command:
```bash
echo "export FRACTAL_MACHINE_ROOT=$(pwd)" >> ~/.bash_profile
source ~/.bash_profile
```
