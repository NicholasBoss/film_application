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

    def add_movie_studio(self, studio_name, movie_id):
        self.add_studio(studio_name)
        self.db_cursor.execute('SELECT studio_id FROM studio WHERE studio_name = %s', (studio_name, ))
        studio_id = self.db_cursor.fetchone()[0]
        self.db_cursor.execute('INSERT INTO movie_studio (movie_id, studio_id) VALUES (%s, %s)',
                                (movie_id, studio_id))
        self.mydb.commit()
        print(self.db_cursor.rowcount, 'record inserted.')
        print('\n')

    def delete_studio(self, studio_id):
        self.db_cursor.execute('DELETE FROM studio WHERE studio_id = %s', (studio_id, ))
        self.mydb.commit()
        print(self.db_cursor.rowcount, 'record deleted.')
        print('\n')

    