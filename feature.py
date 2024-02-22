class feature:

    def __init__(self, db_cursor, mydb):
        self.db_cursor = db_cursor
        self.mydb = mydb

    def add_feature(self, feature_name):
        self.db_cursor.execute('INSERT INTO feature (feature_name) VALUES (%s)',
                                (feature_name, ))
        self.mydb.commit()
        print(self.db_cursor.rowcount, 'record inserted.')
        print('\n')

    def update_feature(self, feature_id, feature_name):
        self.db_cursor.execute('UPDATE feature SET feature_name = %s WHERE feature_id = %s',
                                (feature_name, feature_id))
        self.mydb.commit()
        print(self.db_cursor.rowcount, 'record updated.')
        print('\n')

    def add_movie_feature(self, feature_id, movie_id):
        self.db_cursor.execute('INSERT INTO movie_feature (movie_id, feature_id) VALUES (%s, %s)',
                                (movie_id, feature_id))
        self.mydb.commit()
        print(self.db_cursor.rowcount, 'record inserted.')
        print('\n')

    def update_movie_feature(self, feature_id, movie_id, new_movie_id):
        self.db_cursor.execute('SELECT movie_feature_id FROM movie_feature WHERE feature_id = %s AND movie_id = %s',(feature_id, movie_id))
        result = self.db_cursor.fetchone()
        self.db_cursor.execute('UPDATE movie_feature SET movie_id = %s, feature_id = %s WHERE movie_feature_id = %s', (new_movie_id, feature_id, result[0]))
        self.mydb.commit()
        print(self.db_cursor.rowcount, 'record updated.')
        print('\n')

    def delete_movie_feature(self, movie_feature_id):
        self.db_cursor.execute('DELETE FROM movie_feature WHERE movie_feature_id = %s', (movie_feature_id,))
        self.mydb.commit()
        print(self.db_cursor.rowcount, 'record deleted.')
        print('\n')

    def delete_feature(self, feature_id):
        self.db_cursor.execute('DELETE FROM feature WHERE feature_id = %s', (feature_id, ))
        self.mydb.commit()
        print(self.db_cursor.rowcount, 'record deleted.')
        print('\n')