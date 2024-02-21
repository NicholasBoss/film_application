class movie:

    def __init__(self, db_cursor, mydb):
        self.db_cursor = db_cursor
        self.mydb = mydb

    def add_movie(self, movie_title, movie_year, rating_id):
        self.db_cursor.execute('INSERT INTO movie (movie_title, movie_year, rating_id) VALUES (%s, %s, %s)',
                                (movie_title, movie_year, rating_id))
        self.mydb.commit()
        print(self.db_cursor.rowcount, 'record inserted.')
        print('\n')


    def update_movie(self, movie_id, movie_year, rating_id):
        self.db_cursor.execute('UPDATE movie SET movie_year = %s, rating_id = %s WHERE movie_id = %s',
                                (movie_year, rating_id, movie_id))
        
        self.mydb.commit()
        print(self.db_cursor.rowcount, 'record updated.')
        print('\n')

    def delete_movie(self, movie_id):
        self.db_cursor.execute('DELETE FROM movie WHERE movie_id = %s', (movie_id, ))
        self.mydb.commit()
        print(self.db_cursor.rowcount, 'record deleted.')
        print('\n')
