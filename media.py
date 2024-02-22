class media:

    def __init__(self, db_cursor, mydb):
        self.db_cursor = db_cursor
        self.mydb = mydb

    def add_media(self, media_title):
        self.db_cursor.execute('INSERT INTO media (media_type) VALUES (%s)',
                                (media_title,))
        self.mydb.commit()
        print(self.db_cursor.rowcount, 'record inserted.')
        print('\n')

    def update_media(self, media_id, media_title):
        self.db_cursor.execute('UPDATE media SET media_title = %s WHERE media_id = %s',
                                (media_title, media_id))
        self.mydb.commit()
        print(self.db_cursor.rowcount, 'record updated.')
        print('\n')

    def delete_media(self, media_id):
        self.db_cursor.execute('DELETE FROM media WHERE media_id = %s', (media_id, ))
        self.mydb.commit()
        print(self.db_cursor.rowcount, 'record deleted.')
        print('\n')

    def add_movie_media(self, media_id, movie_id, price_id):
        if price_id == None:
            self.db_cursor.execute('INSERT INTO movie_media (movie_id, media_id) VALUES (%s, %s)',
                                (movie_id, media_id))
        else:
            self.db_cursor.execute('INSERT INTO movie_media (movie_id, media_id, price_id) VALUES (%s, %s, %s)',
                                (movie_id, media_id, price_id))
        self.mydb.commit()
        print(self.db_cursor.rowcount, 'record inserted.')
        print('\n')

    def update_movie_media(self, media_id, movie_id, price_id, new_movie_id):
        self.db_cursor.execute('SELECT movie_media_id FROM movie_media WHERE media_id = %s AND movie_id = %s',(media_id, movie_id))
        result = self.db_cursor.fetchone()
        if price_id == None:
            self.db_cursor.execute('UPDATE movie_media SET movie_id = %s, media_id = %s WHERE movie_media_id = %s', (movie_id, media_id, result[0]))
        else:
            self.db_cursor.execute('UPDATE movie_media SET movie_id = %s, media_id = %s, price_id = %s WHERE movie_media_id = %s', (new_movie_id, media_id, price_id, result[0]))
        self.mydb.commit()
        print(self.db_cursor.rowcount, 'record updated.')
        print('\n')

    def delete_movie_media(self, movie_media_id):
        self.db_cursor.execute('DELETE FROM movie_media WHERE movie_media_id = %s', (movie_media_id,))
        self.mydb.commit()
        print(self.db_cursor.rowcount, 'record deleted.')
        print('\n')