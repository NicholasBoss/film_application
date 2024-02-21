class rating:

    def __init__(self, db_cursor, mydb):
        self.db_cursor = db_cursor
        self.mydb = mydb

    def add_rating(self, rating_level):
        sql = "INSERT INTO rating (rating_level) VALUES (%s)"
        val = (rating_level, )
        self.db_cursor.execute(sql, val)
        self.mydb.commit()

        print(self.db_cursor.rowcount, "record inserted.")