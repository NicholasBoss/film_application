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

    def delete_genre(self, genre_id):
        self.db_cursor.execute('DELETE FROM genre WHERE genre_id = %s', (genre_id, ))
        self.mydb.commit()
        print(self.db_cursor.rowcount, 'record deleted.')
        print('\n')