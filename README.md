# Overview

This project shows a possible frontend for a database in the Intro to Databases (ITM 111) course at BYU-Idaho.

# System Requirements

VS Code

Python (Make sure you add it to the path/environment variables when installing)

MySQL Workbench 

MySQL Server

(Use the 8.0.34 versions on Windows, MAC users: Workbench does not work normally but you can try using the 8.0.36 versions)

A student user with access to a 'film' database. This is created in the Local Instance tab (Root User):

```
CREATE USER 'student'@'localhost';
GRANT ALL ON film.* TO 'student'@'localhost';
```

# How to Access the Application

The streamlit library is used and must be installed using:

```
pip install streamlit
```

You must also use the mysql.connector library. You can install it using:

```
pip install mysql-connector-python
```

To run the application, type in the terminal:

```
streamlit run film_stream.py
```

If everything has been successfully installed, the application will run.

The username and password for the application is 'student'.

Enjoy playing around with the application!
