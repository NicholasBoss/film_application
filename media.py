class media:

    def __init__(self, db_cursor, mydb):
        self.db_cursor = db_cursor
        self.mydb = mydb

    def add_media(self, media_id, media_title):
        self.db_cursor.execute('INSERT INTO media (media_id, media_title) VALUES (%s, %s)',
                                (media_id, media_title))
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

    def add_movie_media(self, media_title, movie_id):
        self.add_media(media_title, movie_id)
        self.db_cursor.execute('SELECT media_id FROM media WHERE media_title = %s', (media_title, ))
        media_id = self.db_cursor.fetchone()[0]
        self.db_cursor.execute('INSERT INTO movie_media (movie_id, media_id) VALUES (%s, %s)',
                                (movie_id, media_id))
        self.mydb.commit()
        print(self.db_cursor.rowcount, 'record inserted.')
        print('\n')