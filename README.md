# Flask App - Store

A Web Application made using python-flask that does CRUD operations, stores the data in sqlite database.

## More about CRUD
The acronym CRUD stands for create, read, update and delete. These are the four basic functions of persistent storage.
* CREATE procedures: Performs the INSERT statement to create a new record.
* READ procedures: Reads the table records based on the primary keynoted within the input parameter.
* UPDATE procedures: Executes an UPDATE statement on the table based on the specified primary key for a record within the WHERE clause of the statement.
* DELETE procedures: Deletes a specified row in the WHERE clause.

## Requirements
============

The python dependencies are managed using pip and listed in
`requirements.txt`

## Setting up Local Development
============================

First, clone this repository:

    git clone https://github.com/kush225/store_flask_app.git

You can use pip, virtualenv and virtualenvwrapper to install the requirements:

    pip install -r requirements.txt
    
Start the server by running `python app.py`:

	python app.py

Browse to [localhost](http://127.0.0.1:5000) for the index page


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## HEROKU LINK
[HEROKU](https://store-flask-app.herokuapp.com/)
