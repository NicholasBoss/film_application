class studio:

    def __init__(self, db_cursor, mydb):
        self.db_cursor = db_cursor
        self.mydb = mydb

    def add_studio(self, studio_name):
        self.db_cursor.execute('INSERT INTO studio (studio_name) VALUES (%s)',
                                (studio_name, ))
        self.mydb.commit()
        print(self.db_cursor.rowcount, 'record inserted.')
        print('\n')

    def update_studio(self, studio_id, studio_name):
        self.db_cursor.execute('UPDATE studio SET studio_name = %s WHERE studio_id = %s',
                                (studio_name, studio_id))
        self.mydb.commit()
        print(self.db_cursor.rowcount, 'record updated.')
        print('\n')

    def add_movie_studio(self, studio_id, movie_id):
        self.db_cursor.execute('INSERT INTO movie_studio (movie_id, studio_id) VALUES (%s, %s)',
                                (movie_id, studio_id))
        self.mydb.commit()
        print(self.db_cursor.rowcount, 'record inserted.')
        print('\n')

    def update_movie_studio(self, studio_id, movie_id, new_movie_id, new_studio_id):
        self.db_cursor.execute('SELECT movie_studio_id FROM movie_studio WHERE studio_id = %s AND movie_id = %s',(studio_id, movie_id))
        result = self.db_cursor.fetchone()
        self.db_cursor.execute('UPDATE movie_studio SET movie_id = %s, studio_id = %s WHERE movie_studio_id = %s', (new_movie_id, new_studio_id, result[0]))
        self.mydb.commit()
        print(self.db_cursor.rowcount, 'record updated.')
        print('\n')

    def delete_movie_studio(self, movie_studio_id):
        self.db_cursor.execute('DELETE FROM movie_studio WHERE movie_studio_id = %s', (movie_studio_id,))
        self.mydb.commit()
        print(self.db_cursor.rowcount, 'record deleted.')
        print('\n')

    def delete_studio(self, studio_id):
        self.db_cursor.execute('DELETE FROM studio WHERE studio_id = %s', (studio_id, ))
        self.mydb.commit()
        print(self.db_cursor.rowcount, 'record deleted.')
        print('\n')

    