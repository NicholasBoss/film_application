class price:

    def __init__(self, db_cursor, mydb):
        self.db_cursor = db_cursor
        self.mydb = mydb

    def add_price(self, price_value):
        sql = "INSERT INTO price (price_value) VALUES (%s)"
        val = (price_value, )
        self.db_cursor.execute(sql, val)
        self.mydb.commit()

        print(self.db_cursor.rowcount, "record inserted.")

    def update_price(self, price_id, price_value):
        sql = "UPDATE price SET price_value = %s WHERE price_id = %s"
        val = (price_value, price_id)
        self.db_cursor.execute(sql, val)
        self.mydb.commit()

        print(self.db_cursor.rowcount, "record updated.")

    def delete_price(self, price_id):
        sql = "DELETE FROM price WHERE price_id = %s"
        val = (price_id, )
        self.db_cursor.execute(sql, val)
        self.mydb.commit()

        print(self.db_cursor.rowcount, "record deleted.")

        