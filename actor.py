class actor:

    def __init__(self, db_cursor, mydb):
        self.db_cursor = db_cursor
        self.mydb = mydb

    def add_actor(self, actor_fname, actor_lname):
        self.db_cursor.execute('INSERT INTO actor (actor_fname, actor_lname) VALUES (%s, %s)',
                                (actor_fname, actor_lname))
        self.mydb.commit()
        print(self.db_cursor.rowcount, 'record inserted.')
        print('\n')

    def update_actor(self, actor_id, actor_fname, actor_lname):
        self.db_cursor.execute('UPDATE actor SET actor_fname = %s, actor_lname = %s WHERE actor_id = %s',
                                (actor_fname, actor_lname, actor_id))
        
        self.mydb.commit()
        print(self.db_cursor.rowcount, 'record updated.')
        print('\n')

    def delete_actor(self, actor_id):
        self.db_cursor.execute('DELETE FROM actor WHERE actor_id = %s', (actor_id, ))
        self.mydb.commit()
        print(self.db_cursor.rowcount, 'record deleted.')
        print('\n')

    def add_movie_actor(self, actor_id, movie_id):
        self.db_cursor.execute('INSERT INTO cast (movie_id, actor_id) VALUES (%s, %s)',
                                (movie_id, actor_id))
        self.mydb.commit()
        print(self.db_cursor.rowcount, 'record inserted.')
        print('\n')

    def update_movie_actor(self, actor_id, movie_id, new_movie_id):
        self.db_cursor.execute('SELECT cast_id FROM cast WHERE actor_id = %s AND movie_id = %s',(actor_id, movie_id))
        result = self.db_cursor.fetchone()
        self.db_cursor.execute('UPDATE cast SET movie_id = %s, actor_id = %s WHERE cast_id = %s', (new_movie_id, actor_id, result[0]))
        self.mydb.commit()
        print(self.db_cursor.rowcount, 'record updated.')
        print('\n')

    def delete_movie_actor(self, cast_id):
        self.db_cursor.execute('DELETE FROM cast WHERE cast_id = %s', (cast_id,))
        self.mydb.commit()
        print(self.db_cursor.rowcount, 'record deleted.')
        print('\n')