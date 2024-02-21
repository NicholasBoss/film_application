class genre:

    def __init__(self, db_cursor, mydb):
        self.db_cursor = db_cursor
        self.mydb = mydb

    def add_genre(self, genre_name):
        self.db_cursor.execute('INSERT INTO genre (genre_name) VALUES (%s)',
                                (genre_name, ))
        self.mydb.commit()
        print(self.db_cursor.rowcount, 'record inserted.')
        print('\n')

    def update_genre(self, genre_id, genre_name):
        self.db_cursor.execute('UPDATE genre SET genre_name = %s WHERE genre_id = %s',
                                (genre_name, genre_id))
        self.mydb.commit()
        print(self.db_cursor.rowcount, 'record updated.')
        print('\n')

    def add_movie_genre(self, genre_id, movie_id):
        self.db_cursor.execute('INSERT INTO movie_genre (movie_id, genre_id) VALUES (%s, %s)',
                                (movie_id, genre_id))
        self.mydb.commit()
        print(self.db_cursor.rowcount, 'record inserted.')
        print('\n')

    def update_movie_genre(self, genre_id, movie_id):
        self.db_cursor.execute('SELECT movie_genre_id FROM movie_genre WHERE genre_id = %s AND movie_id = %s',(genre_id, movie_id))
        result = self.db_cursor.fetchone()
        self.db_cursor.execute('UPDATE movie_genre SET movie_id = %s, genre_id = %s WHERE movie_genre_id = %s', (movie_id, genre_id, result[0]))
        self.mydb.commit()
        print(self.db_cursor.rowcount, 'record updated.')
        print('\n')

    def delete_genre(self, genre_id):
        self.db_cursor.execute('DELETE FROM genre WHERE genre_id = %s', (genre_id, ))
        self.mydb.commit()
        print(self.db_cursor.rowcount, 'record deleted.')
        print('\n')