# cd boss_code
# cd .\boss_code
#!/usr/bin/python
import mysql.connector
import streamlit as st
from datetime import datetime
from dbcreate import *
from movie import *
from rating import *
from actor import *
from genre import *
from feature import *
from studio import *
from price import *
from media import *
import pandas as pd

# Connect to database
# Create variables
user_input = ''

mydb = mysql.connector.connect(
    host='localhost',
    user='student',
    password='student'
)

uname = st.text_input('Enter Username: ')
pwd = st.text_input('Enter Password: ', type='password')

if uname == 'student' and pwd == 'student':
    st.success('Logged in as student')
    st.write('\n')
    print('Connected to Film database')

    db_cursor = mydb.cursor()

    # ask user via streamlit if they want to create/reset database
    st.title('Welcome to the film Database')
    st.write('Would you like to create/reset the database?')
    placeholder = st.empty()
    user_input = placeholder.text_input('Enter yes or no', key=1)
    enter_button = st.button('Enter', key=8)
    click_clear = st.button('Clear', key=3)
    if user_input == 'yes' and enter_button:
        create_db = create(db_cursor, mydb)
        create_db.create_db()
    if click_clear:
        user_input = placeholder.text_input("", key=2)
    if user_input == 'no' and enter_button:
        st.write('Database not created/reset')
        st.write('Please continue to use the database')

    film = mysql.connector.connect(
        host='localhost',
        user='student',
        password='student',
        database='film'
    )

    mycursor = film.cursor()

    print('Connected to MySQL film database')

    st.write('Please select an option from the menus below')

    if st.checkbox("Show PDF of the Film Database"):
        test = mycursor.execute('''SELECT * FROM movie''')
        newtest = mycursor.fetchall()

        if not newtest:
            st.write("There's no information in the database. Cannot generate PDF.")
        else:
            mycursor.execute('''
                            SELECT movie_title
                            ,      GROUP_CONCAT(DISTINCT studio_name) AS Studio
                            ,      GROUP_CONCAT(DISTINCT media_type) AS 'Media Type'
                            ,      movie_year
                            ,      GROUP_CONCAT(DISTINCT genre_name) AS Genre
                            ,      GROUP_CONCAT( DISTINCT CONCAT_WS(' ',actor_fname, actor_lname)) AS Actor
                            ,      GROUP_CONCAT( DISTINCT feature_name) AS Feature
                            ,      rating_level
                            ,      GROUP_CONCAT(DISTINCT CONCAT('$',price_value)) AS Price
                            FROM movie m
                                LEFT JOIN movie_studio ms ON m.movie_id = ms.movie_id
                                LEFT JOIN studio s ON ms.studio_id = s.studio_id
                                LEFT JOIN movie_media mm ON m.movie_id = mm.movie_id
                                    LEFT JOIN media as me ON mm.media_id = me.media_id
                                    LEFT JOIN price as p ON mm.price_id = p.price_id
                                LEFT JOIN movie_genre as mg ON m.movie_id = mg.movie_id
                                    LEFT JOIN genre as g ON mg.genre_id = g.genre_id
                                LEFT JOIN cast as c ON m.movie_id = c.movie_id
                                    LEFT JOIN actor as a ON c.actor_id = a.actor_id
                                LEFT JOIN movie_feature as mf ON m.movie_id = mf.movie_id
                                    LEFT JOIN feature as f ON mf.feature_id = f.feature_id
                                LEFT JOIN rating as r ON m.rating_id = r.rating_id
                            GROUP BY movie_title, movie_year, rating_level, m.movie_id
                            ORDER BY m.movie_id;
                            ''')
            df = pd.DataFrame(mycursor.fetchall())
            df.columns = ['Movie Title', 'Studio', 'Media Type', 'Movie Year', 'Genre', 'Actor', 'Feature', 'Rating', 'Price']
            st.write(df)


    user_input = st.selectbox("Rating Menu", [
                              "Choose an Option",
                              "View Ratings",
                              "Add Rating"])
    
    if user_input == "View Ratings":
        test = mycursor.execute('''
                                  SELECT rating_id
                                  FROM   rating
                                  WHERE  rating_id IS NOT NULL
                                ''')
        newtest = mycursor.fetchall()

        if not newtest:
            st.write("There are no ratings in the database.")

        else:
            mycursor.execute('''SELECT * FROM rating''')
            # Print all rows formatted using panda dataframe
            df = pd.DataFrame(mycursor.fetchall())
            df.columns = ['Rating Id', 'Rating Level']
            st.write(df)
            st.write('\n')
    
    if user_input == "Add Rating":

        rating_level = st.selectbox("Add a Rating:", [
                              "Choose an Option",
                              "G",
                              "PG",
                              "PG-13"])

        usr_button = st.button("Add Rating")

        if usr_button:
            add_rating = rating(mycursor, film)
            add_rating.add_rating(rating_level)

        st.write(mycursor.rowcount, 'record created.')
        st.write('\n')
# Movies
    user_input = st.selectbox("Movie Menu", [
                            "Choose an Option", 
                            "View Movies",
                            "Add Movie", 
                            "Update Movie",
                            "Remove Movie"])

    # Add movie
    if user_input == 'Add Movie':
        # st.write('Add Employee')
        test = mycursor.execute('''
                                  SELECT rating_id
                                  FROM   rating
                                  WHERE  rating_id IS NOT NULL
                                ''')
        newtest = mycursor.fetchall()

        if not newtest:
            st.write('No Ratings in Database. Cannot enter a movie.')
        
        else:
            
            movie_title = st.text_input('Enter Movie Title: ')
            movie_year = st.number_input('Enter Release Year: ')
            rating = mycursor.execute('''
                                        SELECT rating_id, rating_level
                                        FROM   rating;
                                    ''')
            df = pd.DataFrame(mycursor.fetchall())
            df.columns = ['Rating ID','Rating Level']
            st.write(df)
            rating_id = st.text_input('Enter Rating ID: ')
            st.write('\n')

            usr_button = st.button('Add Movie')
            # use dbcreate.py add_employee function
            if usr_button:                
                add_mov = movie(mycursor, film)
                add_mov.add_movie(movie_title, movie_year, rating_id)

            st.write(mycursor.rowcount, 'record created.')
            st.write('\n')

    # Remove movie
    elif user_input == 'Remove Movie':
        # st.write('Remove Employee')
        test = mycursor.execute('''
                                SELECT movie_id
                                FROM movie 
                                WHERE movie_id IS NOT NULL
                                ''')
        newtest = mycursor.fetchall()
        # print(newtest)
        # if newtest is empty list, print message
        if not newtest:
            st.write('No Movies in Database')
        else:
            mycursor.execute('SELECT * FROM movie')

            # Print all rows formatted using panda dataframe
            df = pd.DataFrame(mycursor.fetchall())
            df.columns = ['Movie Id', 'Movie Title', 'Movie Year', 'Rating Id']
            st.write(df)
            st.write('\n')

            movie_id = st.text_input('Enter movie id: ')
            st.write('\n')
            
            usr_button = st.button('Remove Movie')
            # use movie.py delete_movie function
            if usr_button:
                remove_mov = movie(mycursor, film)
                remove_mov.delete_movie(movie_id)
            st.write(mycursor.rowcount, 'record deleted.')
            st.write('\n')

    # Update movie details
    elif user_input == 'Update Movie':

        # st.write('Update Employee')
        test = mycursor.execute('''
                                SELECT movie_id
                                FROM movie
                                WHERE movie_id IS NOT NULL
                                ''')
        newtest = mycursor.fetchall()
        # print(newtest)
        # if newtest is empty list, print message
        if not newtest:
            st.write('No movies in Database.')
        else:
            mycursor.execute('''
                            SELECT * FROM movie
                            ''')

            # Print all rows formatted using panda dataframe
            df = pd.DataFrame(mycursor.fetchall())
            df.columns = ['Movie Id', 'Movie Title', 'Movie Year', 'Rating Id']
            st.write(df)
            st.write('\n')
            movie_id = st.text_input('Enter Movie Id: ')
            movie_year = st.text_input('Enter New Release Year (YYYY): ')
            rating = mycursor.execute('''
                                        SELECT rating_id, rating_level
                                        FROM   rating;
                                    ''')
            df = pd.DataFrame(mycursor.fetchall())
            df.columns = ['Rating ID','Rating Level']
            st.write(df)
            rating_id = st.text_input('Enter rating Id : ')
            
            st.write('\n')
            usr_button = st.button('Update Movie')
            # use dbcreate.py update_employee function
            if usr_button:
                update_mov = movie(mycursor, film)
                update_mov.update_movie(movie_id, movie_year, rating_id)

            st.write(mycursor.rowcount, 'record updated.')
            st.write('\n')

    # View employees
    elif user_input == 'View Movies':
        # st.write('View Employees')
        st.write('\n')
        test = mycursor.execute('''
                                SELECT movie_id
                                FROM movie
                                WHERE movie_id IS NOT NULL
                                ''')
        newtest = mycursor.fetchall()
        # print(newtest)
        # if newtest is empty list, print message
        if not newtest:
            st.write('No Movies in Database.')
        else:
            mycursor.execute('''SELECT * FROM movie''')
            # Print all rows formatted using panda dataframe
            df = pd.DataFrame(mycursor.fetchall())
            df.columns = ['Movie Id', 'Movie Title', 'Movie Year', 'Rating Id']
            st.write(df)
            st.write('\n')

# Actors
    actor_input = st.selectbox("Actor Menu", [
                               "Choose an Option", 
                               "View Actors", 
                               "Add Actor", 
                               "Link Actor to Movie", 
                               "Update Actor Link to Movie",
                               "Update Actor", 
                               "Delete Actor"])

    # View actor
    if actor_input == "View Actors":
        # st.write('View Gear')
        st.write('\n')
        test = mycursor.execute('''
                                SELECT actor_id 
                                FROM actor
                                WHERE actor_id IS NOT NULL
                                ''')
        newtest = mycursor.fetchall()
        # print(newtest)
        # if newtest is empty list, print message
        if not newtest:
            st.write('No Actors in Database.')
        else:
            # add functionality to filter by movie
            if st.checkbox('Filter by Movie'):
                mycursor.execute('''
                                SELECT movie_id
                                ,      movie_title 
                                FROM movie
                                ''')
                m_df = pd.DataFrame(mycursor.fetchall())
                m_df.columns = ['Movie Id', 'Movie Title']
                st.write(m_df)
                movie_id = st.text_input('Enter Movie Id: ')
                st.write('\n')
                movie_filter_button = st.button('Filter')

                if movie_filter_button:
                    mycursor.execute('''
                                    SELECT movie_title
                                    ,      GROUP_CONCAT( DISTINCT CONCAT_WS(' ',actor_fname, actor_lname)) AS Actor
                                    FROM movie m 
                                    LEFT JOIN cast c ON m.movie_id = c.movie_id 
                                    LEFT JOIN actor a ON c.actor_id = a.actor_id 
                                    WHERE m.movie_id = %s
                                    ''', (movie_id,))
                    a_df = pd.DataFrame(mycursor.fetchall())
                    a_df.columns = ['Movie Title', 'Actors']
                    st.write(a_df)
                    st.write('\n')
            else:
                mycursor.execute('''
                                SELECT actor_fname
                                ,      actor_lname
                                FROM   actor
                                ''')

                ac_df = pd.DataFrame(mycursor.fetchall())
                ac_df.columns = ['Actor First Name', 'Actor Last Name']
                st.write(ac_df)
                st.write('\n')

    elif actor_input == "Add Actor":
        # st.write('Add Gear')
        st.write('\n')
        a_fname = st.text_input('Enter Actor First Name: ')
        a_lname = st.text_input('Enter Actor Last Name: ')

        if a_lname == '':
            a_lname = ' '
        
        actor_button = st.button('Add Actor')
        # use gear.py add_gear function
        if actor_button:
            add_actor = actor(mycursor, film)
            add_actor.add_actor(a_fname, a_lname)
        st.write(mycursor.rowcount, 'record updated.')
        st.write('\n')

    # Link actor to movie
    elif actor_input == "Link Actor to Movie":
        
            test = mycursor.execute('''
                                SELECT movie_id
                                FROM movie
                                WHERE movie_id IS NOT NULL
                                ''')
            newtest = mycursor.fetchall()

            test2 = mycursor.execute('''
                                    SELECT actor_id
                                    FROM actor
                                    WHERE actor_id IS NOT NULL
                                    ''')
            newtest2 = mycursor.fetchall()

            # print(newtest)
            # if newtest is empty list, print message
            if not newtest and not newtest2:
                st.write('No Movies or Actors in the Database.')
            elif not newtest:
                st.write('No Movies in Database.')
            elif not newtest2:
                st.write('No Actors in Database.')
            else:
                mycursor.execute('''
                                SELECT movie_id
                                ,      movie_title 
                                FROM   movie
                                ''')
                a_df = pd.DataFrame(mycursor.fetchall())
                a_df.columns = ['Movie Id', 'Movie Title']
                st.write(a_df)
                movie_id = st.text_input('Enter Movie Id: ')
                st.write('\n')
                mycursor.execute('''
                                SELECT actor_id
                                ,      actor_fname
                                ,      actor_lname
                                FROM   actor
                                ''')
                a_df = pd.DataFrame(mycursor.fetchall())
                a_df.columns = ['Actor Id', 'Actor First Name', 'Actor Last Name']
                st.write(a_df)
                actor_id = st.text_input('Enter Actor Id: ')
                st.write('\n')
                movie_actor_add = st.button('Add Actor to Movie')

                if movie_actor_add:
                    add_movie_actor = actor(mycursor, film)
                    add_movie_actor.add_movie_actor(actor_id, movie_id)

    # Update actor link to movie
    elif actor_input == "Update Actor Link to Movie":
        test = mycursor.execute('''
                                SELECT movie_id
                                FROM movie
                                WHERE movie_id IS NOT NULL
                                ''')
        newtest = mycursor.fetchall()

        test2 = mycursor.execute('''
                                SELECT actor_id
                                FROM actor
                                WHERE actor_id IS NOT NULL
                                ''')
        newtest2 = mycursor.fetchall()

        if not newtest and not newtest2:
            st.write('No Movies or Actors in the Database.')
        elif not newtest:
            st.write('No Movies in Database.')
        elif not newtest2:
            st.write('No Actors in Database.')
        else:
            mycursor.execute('''
                            SELECT m.movie_id
                            ,      movie_title
                            ,      a.actor_id
                            ,      actor_fname
                            ,      actor_lname
                            FROM movie m 
                            LEFT JOIN cast c ON m.movie_id = c.movie_id 
                            LEFT JOIN actor a ON c.actor_id = a.actor_id
                            ORDER BY m.movie_id
                            ''')
            m_df = pd.DataFrame(mycursor.fetchall())
            m_df.columns = ['Movie Id', 'Movie Title', 'Actor Id', 'Actor First Name', 'Actor Last Name']
            st.write(m_df)
            movie_id = st.text_input('Enter Movie Id: ')
            st.write('\n')
            actor_id = st.text_input('Enter Actor Id: ')
            st.write('\n')
            movie_actor_button = st.button('Update Actor Link to Movie')

            if movie_actor_button:
                update_movie_actor = actor(mycursor, film)
                update_movie_actor.update_movie_actor(actor_id, movie_id)

    #update actor
    elif actor_input == "Update Actor":
        st.write('\n')
        test = mycursor.execute('''
                                SELECT actor_id
                                FROM   actor
                                WHERE  actor_id IS NOT NULL
                                ''')
        newtest = mycursor.fetchall()
        # print(newtest)
        # if newtest is empty list, print message
        if not newtest:
            st.write('No Actors in Database.')
        else:
            mycursor.execute('''
                            SELECT    actor_id
                            ,         actor_fname
                            ,         actor_lname
                            FROM      actor
                            ''')
            ua_df = pd.DataFrame(mycursor.fetchall())
            ua_df.columns = ['Actor ID','Actor First Name','Actor Last Name']
            st.write(ua_df)

            actor_id = st.text_input('Enter Actor id: ')
            st.write('\n')
            a_fname = st.text_input('Enter Actor First Name: ')
            st.write('\n')
            a_lname = st.text_input('Enter Actor Last Name:')

            up_actor_button = st.button('Update Actor')

            if up_actor_button:
                update_actor = actor(mycursor, film)
                update_actor.update_actor(actor_id, a_fname, a_lname)
            st.write(mycursor.rowcount, 'record updated')
            st.write('\n')
    
    # Delete actor
    elif actor_input == 'Delete Actor':
        test = mycursor.execute('''
                                SELECT actor_id
                                FROM   actor 
                                WHERE  actor_id IS NOT NULL
                                ''')
        newtest = mycursor.fetchall()
        # print(newtest)
        # if newtest is empty list, print message
        if not newtest:
            st.write('No Actors in Database.')
        else:
            mycursor.execute(f'''
                            SELECT actor_id
                            ,      actor_fname
                            ,      actor_lname
                            FROM   actor
                            ''')
            gr_df = pd.DataFrame(mycursor.fetchall())
            gr_df.columns = ['Actor Id','Actor First Name', 'Actor Last Name']
            st.write(gr_df)

            actor_id = st.text_input('Enter Actor id: ')
            st.write('\n')

            del_actor_button = st.button('Delete Actor')

            if del_actor_button:
                delete_actor = actor(mycursor, film)
                delete_actor.delete_actor(actor_id)
            st.write(mycursor.rowcount, 'record deleted.')
            st.write('\n')


# Genre
    genre_input = st.selectbox("Genre Menu", [
                                    "Choose an Option", 
                                    "View Genres",
                                    "Add Genre",
                                    "Link Genre to Movie",
                                    "Update Genre Link to Movie",
                                    "Update Genre",
                                    "Delete Genre"])
    # View genres
    if genre_input == "View Genres":
        st.write('\n')
        # If no repairs or if valueerror, print message
        test = mycursor.execute('''
                                SELECT genre_id
                                FROM genre 
                                WHERE genre_id IS NOT NULL
                                ''')
        newtest = mycursor.fetchall()
        # print(newtest)
        # if newtest is empty list, print message
        if not newtest:
            st.write('No Genres in Database.')

        else:
            # checkbox to filter by movie
            if st.checkbox('Filter by Movie'):
                mycursor.execute('''
                                SELECT movie_id
                                ,      movie_title 
                                FROM movie
                                ''')
                m_df = pd.DataFrame(mycursor.fetchall())
                m_df.columns = ['Movie Id', 'Movie Title']
                st.write(m_df)
                movie_id = st.text_input('Enter Movie Id: ')
                st.write('\n')
                movie_filter_button = st.button('Filter')

                if movie_filter_button:
                    mycursor.execute('''
                                    SELECT movie_title
                                    ,      GROUP_CONCAT(DISTINCT genre_name) AS genre_name
                                    FROM movie m 
                                    LEFT JOIN movie_genre mg ON m.movie_id = mg.movie_id 
                                    LEFT JOIN genre g ON mg.genre_id = g.genre_id 
                                    WHERE m.movie_id = %s
                                    ''', (movie_id,))
                    g_df = pd.DataFrame(mycursor.fetchall())
                    g_df.columns = ['Movie Title', 'Genre Name']
                    st.write(g_df)
                    st.write('\n')
            else:
                mycursor.execute('''
                                SELECT genre_id
                                ,      genre_name
                                FROM genre
                                ''')
                g_df = pd.DataFrame(mycursor.fetchall())
                g_df.columns = ['Genre Id', 'Genre Name']
                st.write(g_df)
                st.write('\n')

    # Add Genre
    elif genre_input == "Add Genre":
        
        st.write('\n')
        genre_name = st.text_input('Enter Genre Name: ')
            
        
        genre_button = st.button('Add Genre')
        # use genre.py add_genre function
        if genre_button:
            add_genre = genre(mycursor, film)
            add_genre.add_genre(genre_name)
        st.write(mycursor.rowcount, 'record created.')
        st.write('\n')

    # Link Genre to Movie
    elif genre_input == "Link Genre to Movie":
        test = mycursor.execute('''
                                SELECT movie_id
                                FROM movie 
                                WHERE movie_id IS NOT NULL
                                ''')
        newtest = mycursor.fetchall()

        test2 = mycursor.execute('''
                                SELECT genre_id
                                FROM genre
                                WHERE genre_id IS NOT NULL
                                ''')
        newtest2 = mycursor.fetchall()

        if not newtest and not newtest2:
            st.write('No Movies or Genres in the Database.')
        elif not newtest:
            st.write('No Movies in Database.')
        elif not newtest2:
            st.write('No Genres in Database.')
        else:
            mycursor.execute('''
                            SELECT movie_id
                            ,      movie_title 
                            FROM movie
                            ''')
            m_df = pd.DataFrame(mycursor.fetchall())
            m_df.columns = ['Movie Id', 'Movie Title']
            st.write(m_df)
            movie_id = st.text_input('Enter Movie Id: ')
            st.write('\n')
            mycursor.execute('''
                            SELECT genre_id
                            ,      genre_name
                            FROM genre
                            ''')
            s_df = pd.DataFrame(mycursor.fetchall())
            s_df.columns = ['Genre Id', 'Genre Name']
            st.write(s_df)
            genre_id = st.text_input('Enter Genre Id: ')
            st.write('\n')
            genre_movie_button = st.button('Add Genre to Movie')

            if genre_movie_button:
                add_genre_movie = genre(mycursor, film)
                add_genre_movie.add_movie_genre(genre_id, movie_id)

    # Update Genre Link to Movie
    elif genre_input == "Update Genre Link to Movie":
        test = mycursor.execute('''
                                SELECT movie_id
                                FROM movie 
                                WHERE movie_id IS NOT NULL
                                ''')
        newtest = mycursor.fetchall()

        test2 = mycursor.execute('''
                                SELECT genre_id
                                FROM genre
                                WHERE genre_id IS NOT NULL
                                ''')
        newtest2 = mycursor.fetchall()

        if not newtest and not newtest2:
            st.write('No Movies or Genres in the Database.')
        elif not newtest:
            st.write('No Movies in Database.')
        elif not newtest2:
            st.write('No Genres in Database.')
        else:
            mycursor.execute('''
                            SELECT m.movie_id
                            ,      movie_title 
                            ,      g.genre_id
                            ,      genre_name
                            FROM movie m
                            LEFT JOIN movie_genre mg ON m.movie_id = mg.movie_id
                            LEFT JOIN genre g ON mg.genre_id = g.genre_id
                            ORDER BY m.movie_id
                            ''')
            m_df = pd.DataFrame(mycursor.fetchall())
            m_df.columns = ['Movie Id', 'Movie Title', 'Genre Id', 'Genre Name']
            st.write(m_df)
            movie_id = st.text_input('Enter Movie Id: ')
            st.write('\n')
            genre_id = st.text_input('Enter Genre Id: ')
            st.write('\n')
            genre_movie_button = st.button('Update Genre Link to Movie')

            if genre_movie_button:
                update_genre_movie = genre(mycursor, film)
                update_genre_movie.update_movie_genre(genre_id, movie_id)

    # Update Genre
    elif genre_input == "Update Genre":
        st.write('\n')
        test = mycursor.execute('''
                                SELECT genre_id 
                                FROM genre 
                                WHERE genre_id IS NOT NULL
                                ''')
        newtest = mycursor.fetchall()
        # print(newtest)
        # if newtest is empty list, print message
        if not newtest:
            st.write('No Genres in Database.')
        else:
            # list employee first name and gear name and employee_log_id
            mycursor.execute('''
                            SELECT genre_id
                            ,      genre_name
                            FROM   genre
                            ''')
            e_df = pd.DataFrame(mycursor.fetchall())
            e_df.columns = ['Genre Id','Genre Name']
            st.write(e_df)
            st.write('\n')
            genre_id = st.text_input('Enter genre id: ')
            genre_name = st.text_input('Enter new genre name: ')

            genre_button = st.button('Update Genre')
            # use genre.py update_genre function
            if genre_button:
                update_genre = genre(mycursor, film)
                update_genre.update_genre(genre_id, genre_name)
            st.write(mycursor.rowcount, 'record updated.')
            st.write('\n')

    # Delete Genre
    elif genre_input == "Delete Genre":
        st.write('\n')
        test = mycursor.execute('''
                                SELECT genre_id
                                FROM genre 
                                WHERE genre_id IS NOT NULL
                                ''')
        newtest = mycursor.fetchall()
        # print(newtest)
        # if newtest is empty list, print message
        if not newtest:
            st.write('No Genres in Database.')
        else:
            # list genre id and genre name
            mycursor.execute('''
                            SELECT genre_id
                            ,      genre_name
                            FROM   genre
                            ''')
            e_df = pd.DataFrame(mycursor.fetchall())
            e_df.columns = ['Genre Id', 'Genre Name']
            st.write(e_df)
            st.write('\n')
            genre_id = st.text_input('Enter Genre id: ')
           
            delete_genre_button = st.button('Delete Genre')
            # use genre.py delete_genre function
            if delete_genre_button:
                delete_genre = genre(mycursor, film)
                delete_genre.delete_genre(genre_id)
            st.write(mycursor.rowcount, 'record updated.')
            st.write('\n')

    
    #Feature
    feature_input = st.selectbox("Feature Menu", [
                                    "Choose an Option", 
                                    "View Features",
                                    "Add Feature",
                                    "Link Feature to Movie",
                                    "Update Feature Link to Movie"
                                    "Update Feature",
                                    "Delete Feature"])
    
    # View feature
    if feature_input == "View Features":
        st.write('\n')
        # If no repairs or if valueerror, print message
        test = mycursor.execute('''
                                SELECT feature_id
                                FROM feature 
                                WHERE feature_id IS NOT NULL
                                ''')
        newtest = mycursor.fetchall()
        # print(newtest)
        # if newtest is empty list, print message
        if not newtest:
            st.write('No Features in Database.')

        else:
            # checkbox to filter by movie
            if st.checkbox('Filter by Movie'):
                mycursor.execute('''
                                SELECT movie_id
                                ,      movie_title 
                                FROM movie
                                ''')
                m_df = pd.DataFrame(mycursor.fetchall())
                m_df.columns = ['Movie Id', 'Movie Title']
                st.write(m_df)
                movie_id = st.text_input('Enter Movie Id: ')
                st.write('\n')
                movie_filter_button = st.button('Filter')

                if movie_filter_button:
                    mycursor.execute('''
                                    SELECT movie_title
                                    ,      GROUP_CONCAT(DISTINCT feature_name) AS feature_name
                                    FROM movie m 
                                    LEFT JOIN movie_feature mf ON m.movie_id = mf.movie_id 
                                    LEFT JOIN feature f ON mf.feature_id = f.feature_id 
                                    WHERE m.movie_id = %s
                                    ''', (movie_id,))
                    g_df = pd.DataFrame(mycursor.fetchall())
                    g_df.columns = ['Movie Title', 'Feature Name']
                    st.write(g_df)
                    st.write('\n')
            else:
                mycursor.execute('''
                                SELECT feature_id
                                ,      feature_name
                                FROM feature
                                ''')
                g_df = pd.DataFrame(mycursor.fetchall())
                g_df.columns = ['Feature Id', 'Feature Name']
                st.write(g_df)
                st.write('\n')

    # Create feature
    elif feature_input == "Add Feature":
        
        st.write('\n')
        feature_name = st.text_input('Enter Feature Name: ')
            
        
        feature_button = st.button('Add Feature')
        # use feature.py add_feature function
        if feature_button:
            add_feature = feature(mycursor, film)
            add_feature.add_feature(feature_name)
        st.write(mycursor.rowcount, 'record created.')
        st.write('\n')

    # Link feature to movie
    elif feature_input == "Link Feature to Movie":
        test = mycursor.execute('''
                                SELECT movie_id
                                FROM movie 
                                WHERE movie_id IS NOT NULL
                                ''')
        newtest = mycursor.fetchall()

        test2 = mycursor.execute('''
                                SELECT feature_id
                                FROM feature
                                WHERE feature_id IS NOT NULL
                                ''')
        newtest2 = mycursor.fetchall()

        if not newtest and not newtest2:
            st.write('No Movies or Features in the Database.')
        elif not newtest:
            st.write('No Movies in Database.')
        elif not newtest2:
            st.write('No Features in Database.')
        else:
            mycursor.execute('''
                            SELECT movie_id
                            ,      movie_title 
                            FROM movie
                            ''')
            m_df = pd.DataFrame(mycursor.fetchall())
            m_df.columns = ['Movie Id', 'Movie Title']
            st.write(m_df)
            movie_id = st.text_input('Enter Movie Id: ')
            st.write('\n')
            mycursor.execute('''
                            SELECT feature_id
                            ,      feature_name
                            FROM feature
                            ''')
            s_df = pd.DataFrame(mycursor.fetchall())
            s_df.columns = ['Feature Id', 'Feature Name']
            st.write(s_df)
            feature_id = st.text_input('Enter Feature Id: ')
            st.write('\n')
            feature_movie_button = st.button('Add Feature to Movie')

            if feature_movie_button:
                add_feature_movie = feature(mycursor, film)
                add_feature_movie.add_movie_feature(feature_id, movie_id)

    # Update feature link to movie
    elif feature_input == "Update Feature Link to Movie":
        test = mycursor.execute('''
                                SELECT movie_id
                                FROM movie 
                                WHERE movie_id IS NOT NULL
                                ''')
        newtest = mycursor.fetchall()

        test2 = mycursor.execute('''
                                SELECT feature_id
                                FROM feature
                                WHERE feature_id IS NOT NULL
                                ''')
        newtest2 = mycursor.fetchall()

        if not newtest and not newtest2:
            st.write('No Movies or Features in the Database.')
        elif not newtest:
            st.write('No Movies in Database.')
        elif not newtest2:
            st.write('No Features in Database.')
        else:
            mycursor.execute('''
                            SELECT m.movie_id
                            ,      movie_title
                            ,      f.feature_id
                            ,      feature_name 
                            FROM movie m
                            LEFT JOIN movie_feature mf ON m.movie_id = mf.movie_id
                            LEFT JOIN feature f ON mf.feature_id = f.feature_id
                            ORDER BY m.movie_id
                            ''')
            m_df = pd.DataFrame(mycursor.fetchall())
            m_df.columns = ['Movie Id', 'Movie Title', 'Feature Id', 'Feature Name']
            st.write(m_df)
            movie_id = st.text_input('Enter Movie Id: ')
            st.write('\n')
            feature_id = st.text_input('Enter Feature Id: ')
            st.write('\n')
            feature_movie_button = st.button('Update Feature Link to Movie')

            if feature_movie_button:
                update_feature_movie = feature(mycursor, film)
                update_feature_movie.update_movie_feature(feature_id, movie_id)

    # Update feature
    elif feature_input == "Update Feature":
        st.write('\n')
        test = mycursor.execute('''
                                SELECT feature_id 
                                FROM feature 
                                WHERE feature_id IS NOT NULL
                                ''')
        newtest = mycursor.fetchall()
        # print(newtest)
        # if newtest is empty list, print message
        if not newtest:
            st.write('No Features in Database.')
        else:
            # list feature id and feature name
            mycursor.execute('''
                            SELECT feature_id
                            ,      feature_name
                            FROM   feature
                            ''')
            e_df = pd.DataFrame(mycursor.fetchall())
            e_df.columns = ['Feature Id','Feature Name']
            st.write(e_df)
            st.write('\n')
            feature_id = st.text_input('Enter feature id: ')
            feature_name = st.text_input('Enter new feature name: ')

            feature_button = st.button('Update Feature')
            # use feature.py update_feature function
            if feature_button:
                update_feature = feature(mycursor, film)
                update_feature.update_feature(feature_id, feature_name)
            st.write(mycursor.rowcount, 'record updated.')
            st.write('\n')

    # Delete feature
    elif feature_input == "Delete Feature":
        st.write('\n')
        test = mycursor.execute('''
                                SELECT feature_id
                                FROM feature 
                                WHERE feature_id IS NOT NULL
                                ''')
        newtest = mycursor.fetchall()
        # print(newtest)
        # if newtest is empty list, print message
        if not newtest:
            st.write('No Features in Database.')
        else:
            # list feature id and feature name
            mycursor.execute('''
                            SELECT feature_id
                            ,      feature_name
                            FROM   feature
                            ''')
            e_df = pd.DataFrame(mycursor.fetchall())
            e_df.columns = ['Feature Id', 'Feature Name']
            st.write(e_df)
            st.write('\n')
            feature_id = st.text_input('Enter feature id: ')
           
            delete_feature_button = st.button('Delete Feature')
            # use feature.py delete_feature function
            if delete_feature_button:
                delete_feature = feature(mycursor, film)
                delete_feature.delete_feature(feature_id)
            st.write(mycursor.rowcount, 'record updated.')
            st.write('\n')

    #Studio
            
    studio_input = st.selectbox("Studio Menu", [
                                    "Choose an Option", 
                                    "View Studios",
                                    "Add Studio",
                                    "Link Studio to Movie",
                                    "Update Studio Link to Movie",
                                    "Update Studio",
                                    "Delete Studio"])
    # View studio
    if studio_input == "View Studios":
        st.write('\n')
        # If no repairs or if valueerror, print message
        test = mycursor.execute('''
                                SELECT studio_id
                                FROM studio 
                                WHERE studio_id IS NOT NULL
                                ''')
        newtest = mycursor.fetchall()
        # print(newtest)
        # if newtest is empty list, print message
        if not newtest:
            st.write('No Studios in Database.')

        else:
            # checkbox to filter by movie
            if st.checkbox('Filter by Movie'):
                mycursor.execute('''
                                SELECT movie_id
                                ,      movie_title 
                                FROM movie
                                ''')
                m_df = pd.DataFrame(mycursor.fetchall())
                m_df.columns = ['Movie Id', 'Movie Title']
                st.write(m_df)
                movie_id = st.text_input('Enter Movie Id: ')
                st.write('\n')
                movie_filter_button = st.button('Filter')

                if movie_filter_button:
                    mycursor.execute('''
                                    SELECT movie_title
                                    ,      GROUP_CONCAT(studio_name) AS studio_name
                                    FROM movie m 
                                    LEFT JOIN movie_studio ms ON m.movie_id = ms.movie_id
                                    LEFT JOIN studio s ON ms.studio_id = s.studio_id 
                                    WHERE m.movie_id = %s
                                    ''', (movie_id,))
                    g_df = pd.DataFrame(mycursor.fetchall())
                    g_df.columns = ['Movie Title', 'Studio Name']
                    st.write(g_df)
                    st.write('\n')
            else:
                mycursor.execute('''
                                SELECT studio_id
                                ,      studio_name
                                FROM studio
                                ''')
                g_df = pd.DataFrame(mycursor.fetchall())
                g_df.columns = ['Studio Id', 'Studio Name']
                st.write(g_df)
                st.write('\n')

    # Create studio
    elif studio_input == "Add Studio":
        
        st.write('\n')
        studio_name = st.text_input('Enter Studio Name: ')
            
        
        studio_button = st.button('Add Studio')
        # use studio.py add_studio function
        if studio_button:
            add_studio = studio(mycursor, film)
            add_studio.add_studio(studio_name)
        st.write(mycursor.rowcount, 'record created.')
        st.write('\n')

    #Link Studio to Movie
    elif studio_input == "Link Studio to Movie":
        st.write('\n')
        test = mycursor.execute('''
                                SELECT movie_id
                                FROM movie 
                                WHERE movie_id IS NOT NULL
                                ''')
        newtest = mycursor.fetchall()

        test2 = mycursor.execute('''
                                SELECT studio_id
                                FROM studio
                                WHERE studio_id IS NOT NULL
                                ''')
        newtest2 = mycursor.fetchall()

        # print(newtest)
        # if newtest is empty list, print message
        if not newtest and not newtest2:
            st.write('No Movies or Studios in the Database.')
        elif not newtest:
            st.write('No Movies in Database.')
        elif not newtest2:
            st.write('No Studios in Database.') 
        else:
            mycursor.execute('''
                            SELECT movie_id
                            ,      movie_title 
                            FROM movie
                            ''')
            m_df = pd.DataFrame(mycursor.fetchall())
            m_df.columns = ['Movie Id', 'Movie Title']
            st.write(m_df)
            movie_id = st.text_input('Enter Movie Id: ')
            st.write('\n')
            mycursor.execute('''
                            SELECT studio_id
                            ,      studio_name 
                            FROM studio
                            ''')
            s_df = pd.DataFrame(mycursor.fetchall())
            s_df.columns = ['Studio Id', 'Studio Name']
            st.write(s_df)
            studio_id = st.text_input('Enter Studio Id: ')
            st.write('\n')
            studio_movie_button = st.button('Add Studio to Movie')

            if studio_movie_button:
                add_studio_movie = studio(mycursor, film)
                add_studio_movie.add_movie_studio(studio_id, movie_id)

    # Update studio link to movie
    elif studio_input == "Update Studio Link to Movie":
        test = mycursor.execute('''
                                SELECT movie_id
                                FROM movie 
                                WHERE movie_id IS NOT NULL
                                ''')
        newtest = mycursor.fetchall()

        test2 = mycursor.execute('''
                                SELECT studio_id
                                FROM studio
                                WHERE studio_id IS NOT NULL
                                ''')
        newtest2 = mycursor.fetchall()

        if not newtest and not newtest2:
            st.write('No Movies or Studios in the Database.')
        elif not newtest:
            st.write('No Movies in Database.')
        elif not newtest2:
            st.write('No Studios in Database.')
        else:
            mycursor.execute('''
                            SELECT m.movie_id
                            ,      movie_title
                            ,      s.studio_id
                            ,      studio_name 
                            FROM movie m
                            LEFT JOIN movie_studio ms ON m.movie_id = ms.movie_id
                            LEFT JOIN studio s ON ms.studio_id = s.studio_id
                            ORDER BY m.movie_id
                            ''')
            m_df = pd.DataFrame(mycursor.fetchall())
            m_df.columns = ['Movie Id', 'Movie Title', 'Studio Id', 'Studio Name']
            st.write(m_df)
            movie_id = st.text_input('Enter Movie Id: ')
            st.write('\n')
            studio_id = st.text_input('Enter Studio Id: ')
            st.write('\n')
            studio_movie_button = st.button('Update Studio Link to Movie')

            if studio_movie_button:
                update_studio_movie = studio(mycursor, film)
                update_studio_movie.update_movie_studio(studio_id, movie_id)

    # Update studio
    elif studio_input == "Update Studio":
        st.write('\n')
        test = mycursor.execute('''
                                SELECT studio_id 
                                FROM studio 
                                WHERE studio_id IS NOT NULL
                                ''')
        newtest = mycursor.fetchall()
        # print(newtest)
        # if newtest is empty list, print message
        if not newtest:
            st.write('No Studios in Database.')
        else:
            # list studio id and studio name
            mycursor.execute('''
                            SELECT studio_id
                            ,      studio_name
                            FROM   studio
                            ''')
            e_df = pd.DataFrame(mycursor.fetchall())
            e_df.columns = ['Studio Id','Studio Name']
            st.write(e_df)
            st.write('\n')
            studio_id = st.text_input('Enter studio id: ')
            studio_name = st.text_input('Enter new studio name: ')

            studio_button = st.button('Update Studio')
            # use studio.py update_studio function
            if studio_button:
                update_studio = studio(mycursor, film)
                update_studio.update_studio(studio_id, studio_name)
            st.write(mycursor.rowcount, 'record updated.')
            st.write('\n')

    # Delete studio
    elif studio_input == "Delete Studio":
        st.write('\n')
        test = mycursor.execute('''
                                SELECT studio_id
                                FROM studio 
                                WHERE studio_id IS NOT NULL
                                ''')
        newtest = mycursor.fetchall()
        # print(newtest)
        # if newtest is empty list, print message
        if not newtest:
            st.write('No Studios in Database.')
        else:
            # list studio id and studio name
            mycursor.execute('''
                            SELECT studio_id
                            ,      studio_name
                            FROM   studio
                            ''')
            e_df = pd.DataFrame(mycursor.fetchall())
            e_df.columns = ['Studio Id', 'Studio Name']
            st.write(e_df)
            st.write('\n')
            studio_id = st.text_input('Enter studio id: ')
           
            delete_studio_button = st.button('Delete Studio')
            # use studio.py delete_studio function
            if delete_studio_button:
                delete_studio = studio(mycursor, film)
                delete_studio.delete_studio(studio_id)
            st.write(mycursor.rowcount, 'record updated.')
            st.write('\n')

#Price Menu
    price_input = st.selectbox("Price Menu", [
                                    "Choose an Option", 
                                    "View Prices",
                                    "Add Price",
                                    "Update Price",
                                    "Delete Price"])
    # View price
    if price_input == "View Prices":
        st.write('\n')
        # If no prices or if valueerror, print message
        test = mycursor.execute('''
                                SELECT price_id
                                FROM price 
                                WHERE price_id IS NOT NULL
                                ''')
        newtest = mycursor.fetchall()
        # print(newtest)
        # if newtest is empty list, print message
        if not newtest:
            st.write('No Prices in Database.')

        else:
            mycursor.execute('''
                            SELECT price_id
                            ,      price_value
                            FROM   price
                            ''')
            g_df = pd.DataFrame(mycursor.fetchall())
            g_df.columns = ['Price Id', 'Price Value']
            st.write(g_df)
            st.write('\n')

    # Create price
    elif price_input == "Add Price":
        st.write('\n')
        price_value = st.text_input('Enter Price Value: ')
            
        price_button = st.button('Add Price')
        # use price.py add_price function
        if price_button:
            add_price = price(mycursor, film)
            add_price.add_price(price_value)
        st.write(mycursor.rowcount, 'record created.')
        st.write('\n')

    # Update price
    elif price_input == "Update Price":
        st.write('\n')
        test = mycursor.execute('''
                                SELECT price_id 
                                FROM price 
                                WHERE price_id IS NOT NULL
                                ''')
        newtest = mycursor.fetchall()
        # print(newtest)
        # if newtest is empty list, print message
        if not newtest:
            st.write('No Prices in Database.')
        else:
            # list price id and price value
            mycursor.execute('''
                            SELECT price_id
                            ,      price_value
                            FROM   price
                            ''')
            e_df = pd.DataFrame(mycursor.fetchall())
            e_df.columns = ['Price Id','Price Value']
            st.write(e_df)
            st.write('\n')
            price_id = st.text_input('Enter price id: ')
            price_value = st.text_input('Enter new price value: ')

            price_button = st.button('Update Price')
            # use price.py update_price function
            if price_button:
                update_price = price(mycursor, film)
                update_price.update_price(price_id, price_value)
            st.write(mycursor.rowcount, 'record updated.')
            st.write('\n')

    # Delete price
    elif price_input == "Delete Price":
        st.write('\n')
        test = mycursor.execute('''
                                SELECT price_id
                                FROM price 
                                WHERE price_id IS NOT NULL
                                ''')
        newtest = mycursor.fetchall()
        # print(newtest)
        # if newtest is empty list, print message
        if not newtest:
            st.write('No Prices in Database.')
        else:
            # list price id and price value
            mycursor.execute('''
                            SELECT price_id
                            ,      price_value
                            FROM   price
                            ''')
            e_df = pd.DataFrame(mycursor.fetchall())
            e_df.columns = ['Price Id', 'Price Value']
            st.write(e_df)
            st.write('\n')
            price_id = st.text_input('Enter price id: ')
           
            delete_price_button = st.button('Delete Price')
            # use price.py delete_price function
            if delete_price_button:
                delete_price = price(mycursor, film)
                delete_price.delete_price(price_id)
            st.write(mycursor.rowcount, 'record updated.')
            st.write('\n')

# Media Menu
    media_input = st.selectbox("Media Menu", [
                                    "Choose an Option", 
                                    "View Media",
                                    "Add Media",
                                    "Link Media, Movie, and Price",
                                    "Update Media and Price Links to Movie",
                                    "Update Media",
                                    "Delete Media"])
    # View media
    if media_input == "View Media":
        st.write('\n')
        # If no repairs or if valueerror, print message
        test = mycursor.execute('''
                                SELECT media_id
                                FROM media 
                                WHERE media_id IS NOT NULL
                                ''')
        newtest = mycursor.fetchall()
        # print(newtest)
        # if newtest is empty list, print message
        if not newtest:
            st.write('No Media in Database.')

        else:
            # checkbox to filter by movie
            if st.checkbox('Filter by Movie'):
                st.write('\n')
                test = mycursor.execute('''
                                        SELECT movie_id
                                        FROM movie 
                                        WHERE movie_id IS NOT NULL
                                        ''')
                newtest = mycursor.fetchall()
                # print(newtest)
                # if newtest is empty list, print message
                if not newtest:
                    st.write('No Movies in Database.')
                else:
                    mycursor.execute('''
                                    SELECT movie_id
                                    ,      movie_title 
                                    FROM movie
                                    ''')
                    m_df = pd.DataFrame(mycursor.fetchall())
                    m_df.columns = ['Movie Id', 'Movie Title']
                    st.write(m_df)
                    movie_id = st.text_input('Enter Movie Id: ')
                    st.write('\n')
                    movie_filter_button = st.button('Filter')

                    if movie_filter_button:
                        mycursor.execute('''
                                        SELECT movie_title
                                        ,      GROUP_CONCAT(DISTINCT media_type) AS media_type
                                        FROM movie m 
                                        LEFT JOIN movie_media mm ON m.movie_id = mm.movie_id
                                        LEFT JOIN media md ON mm.media_id = md.media_id
                                        WHERE m.movie_id = %s
                                        ''', (movie_id,))
                        g_df = pd.DataFrame(mycursor.fetchall())
                        g_df.columns = ['Movie Title', 'Media Type']
                        st.write(g_df)
                        st.write('\n')
            # Show prices, media, and movies
            elif st.checkbox('Show Movies by Media and Price'):
                test = mycursor.execute('''
                                        SELECT movie_id
                                        FROM movie
                                        WHERE movie_id IS NOT NULL
                                        ''')
                newtest = mycursor.fetchall()

                test2 = mycursor.execute('''
                                         SELECT price_id
                                         FROM price
                                         WHERE price_id IS NOT NULL
                                        ''')
                newtest2 = mycursor.fetchall()

                # print(newtest)
                # if newtest is empty list, print message
                if not newtest:
                    st.write('No Movies in Database.')
                elif not newtest2:
                    st.write('No Prices in Database.')
                
                else:
                    mycursor.execute('''
                                    SELECT movie_title
                                    ,      GROUP_CONCAT(media_type) AS media_type
                                    ,      GROUP_CONCAT(CONCAT('$',price_value)) AS price_value
                                    FROM movie m
                                    LEFT JOIN movie_media mm ON m.movie_id = mm.movie_id
                                    LEFT JOIN media md ON mm.media_id = md.media_id
                                    LEFT JOIN price p ON mm.price_id = p.price_id
                                    GROUP BY movie_title, m.movie_id
                                    ORDER BY m.movie_id
                                    ''')
                    g_df = pd.DataFrame(mycursor.fetchall())
                    g_df.columns = ['Movie Title', 'Media Type', 'Price Value']
                    st.write(g_df)
                    st.write('\n')
            else:
                mycursor.execute('''
                                SELECT media_id
                                ,      media_type
                                FROM media
                                ''')
                g_df = pd.DataFrame(mycursor.fetchall())
                g_df.columns = ['Media Id', 'Media Type']
                st.write(g_df)
                st.write('\n')

    # Create media
    elif media_input == "Add Media":
        
        st.write('\n')
        media_type = st.text_input('Enter Media Type: ')
            
        
        media_button = st.button('Add Media')
        # use media.py add_media function
        if media_button:
            add_media = media(mycursor, film)
            add_media.add_media(media_type)
        st.write(mycursor.rowcount, 'record created.')
        st.write('\n')

    # Link media and price to movie
    elif media_input == "Link Media, Movie, and Price":
        # checkbox to add media to movie
        st.write('\n')
        test = mycursor.execute('''
                                SELECT movie_id
                                FROM movie
                                ''')
        newtest = mycursor.fetchall()

        test2 = mycursor.execute('''
                                SELECT price_id
                                FROM price
                                ''')
        newtest2 = mycursor.fetchall()
        # print(newtest)
        # if newtest is empty list, print message
        if not newtest and not newtest2:
            st.write('No Movies or Prices in Database.')
        elif not newtest:
            st.write('No Movies in Database.')
        elif not newtest2:
            st.write('No Prices in Database.')
        else:
            mycursor.execute('''
                            SELECT media_id
                            ,      media_type
                            FROM media
                            ''')
            me_df = pd.DataFrame(mycursor.fetchall())
            me_df.columns = ['Media Id', 'Media Type']
            st.write(me_df)
            media_id = st.text_input('Enter Media Id: ')
            st.write('\n')
            mycursor.execute('''
                            SELECT movie_id
                            ,      movie_title 
                            FROM movie
                            ''')
            m_df = pd.DataFrame(mycursor.fetchall())
            m_df.columns = ['Movie Id', 'Movie Title']
            st.write(m_df)
            me_movie_id = st.text_input('Enter Movie Id to Join with Media: ')
            st.write('\n')
            mycursor.execute('''
                            SELECT price_id
                            ,      price_value
                            FROM   price
                            ''')
            p_df = pd.DataFrame(mycursor.fetchall())
            p_df.columns = ['Price Id', 'Price Value']
            st.write(p_df)
            price_id = st.text_input('Enter Price Id: ')
            if price_id == '':
                price_id = None
            media_movie_button = st.button('Add Media to Movie')

            if media_movie_button:
                add_media_movie = media(mycursor, film)
                add_media_movie.add_movie_media(media_id, me_movie_id, price_id)

    # Update media and price link to movie
    elif media_input == "Update Media and Price Links to Movie":
        # checkbox to add media to movie
        st.write('\n')
        test = mycursor.execute('''
                                SELECT movie_id
                                FROM movie
                                ''')
        newtest = mycursor.fetchall()

        test2 = mycursor.execute('''
                                SELECT price_id
                                FROM price
                                ''')
        newtest2 = mycursor.fetchall()
        # print(newtest)
        # if newtest is empty list, print message
        if not newtest and not newtest2:
            st.write('No Movies or Prices in Database.')
        elif not newtest:
            st.write('No Movies in Database.')
        elif not newtest2:
            st.write('No Prices in Database.')
        else:
            mycursor.execute('''
                            SELECT m.movie_id
                            ,      movie_title
                            ,      md.media_id
                            ,      media_type
                            ,      p.price_id
                            ,      price_value
                            FROM movie m
                            LEFT JOIN movie_media mm ON m.movie_id = mm.movie_id
                            LEFT JOIN media md ON mm.media_id = md.media_id
                            LEFT JOIN price p ON mm.price_id = p.price_id
                            ORDER BY m.movie_id
                            ''')
            me_df = pd.DataFrame(mycursor.fetchall())
            me_df.columns = ['Movie Id', 'Movie Title', 'Media Id', 'Media Type', 'Price Id', 'Price Value']
            st.write(me_df)
            media_id = st.text_input('Enter Media Id: ')
            st.write('\n')
            me_movie_id = st.text_input('Enter Movie Id to Join with Media: ')
            st.write('\n')
            price_id = st.text_input('Enter Price Id: ')
            if price_id == '':
                price_id = None
            media_movie_button = st.button('Update Media and Price Links to Movie')

            if media_movie_button:
                update_media_movie = media(mycursor, film)
                update_media_movie.update_movie_media(media_id, me_movie_id, price_id)

    # Update media
    elif media_input == "Update Media":
        st.write('\n')
        test = mycursor.execute('''
                                SELECT media_id 
                                FROM media 
                                WHERE media_id IS NOT NULL
                                ''')
        newtest = mycursor.fetchall()
        # print(newtest)
        # if newtest is empty list, print message
        if not newtest:
            st.write('No Media in Database.')
        else:
            # list media id and media type
            mycursor.execute('''
                            SELECT media_id
                            ,      media_type
                            FROM   media
                            ''')
            e_df = pd.DataFrame(mycursor.fetchall())
            e_df.columns = ['Media Id','Media Type']
            st.write(e_df)
            st.write('\n')
            media_id = st.text_input('Enter media id: ')
            media_type = st.text_input('Enter new media type: ')

            media_button = st.button('Update Media')
            # use media.py update_media function
            if media_button:
                update_media = media(mycursor, film)
                update_media.update_media(media_id, media_type)
            st.write(mycursor.rowcount, 'record updated.')
            st.write('\n')

    # Delete media
    elif media_input == "Delete Media":
        st.write('\n')
        test = mycursor.execute('''
                                SELECT media_id
                                FROM media 
                                WHERE media_id IS NOT NULL
                                ''')
        newtest = mycursor.fetchall()
        # print(newtest)
        # if newtest is empty list, print message
        if not newtest:
            st.write('No Media in Database.')
        else:
            # list media id and media type
            mycursor.execute('''
                            SELECT media_id
                            ,      media_type
                            FROM   media
                            ''')
            e_df = pd.DataFrame(mycursor.fetchall())
            e_df.columns = ['Media Id', 'Media Type']
            st.write(e_df)
            st.write('\n')
            media_id = st.text_input('Enter media id: ')
           
            delete_media_button = st.button('Delete Media')
            # use media.py delete_media function
            if delete_media_button:
                delete_media = media(mycursor, film)
                delete_media.delete_media(media_id)
            st.write(mycursor.rowcount, 'record updated.')
            st.write('\n')