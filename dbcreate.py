class create:
    def __init__(self, db_cursor, mydb):
        self.db_cursor = db_cursor
        self.mydb = mydb

    def create_db(self):
        #drop database
        self.db_cursor.execute('DROP DATABASE IF EXISTS film')
        print('Database dropped')
        print('\n')
        #create database
        self.db_cursor.execute('CREATE DATABASE IF NOT EXISTS film')

        # create tables
        self.db_cursor.execute('USE film')
        
        self.db_cursor.execute('DROP TABLE IF EXISTS rating')
        self.db_cursor.execute('CREATE TABLE IF NOT EXISTS film.rating '
                                '(rating_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY'
                                ', rating_level VARCHAR(5) NOT NULL)'
                                'ENGINE = InnoDB;')
        
        self.db_cursor.execute('DROP TABLE IF EXISTS movie')
        self.db_cursor.execute('CREATE TABLE IF NOT EXISTS film.movie '
                               '(movie_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY'
                               ', movie_title VARCHAR(45) NOT NULL'
                               ', movie_year INT UNSIGNED NOT NULL'
                               ', rating_id INT UNSIGNED NOT NULL'
                               ', INDEX movie_fk1_idx (rating_id ASC) VISIBLE'
                               ', CONSTRAINT movie_fk1'
                               '    FOREIGN KEY (rating_id)'
                               '    REFERENCES  film.rating (rating_id)'
                               '    ON DELETE CASCADE'
                               '    ON UPDATE CASCADE)'
                               ' ENGINE = InnoDB;')
        
        self.db_cursor.execute('DROP TABLE IF EXISTS actor')
        self.db_cursor.execute('CREATE TABLE IF NOT EXISTS film.actor '
                               '(actor_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY'
                               ', actor_fname VARCHAR(45) NOT NULL'
                               ', actor_lname VARCHAR(45) NOT NULL)'
                               'ENGINE = InnoDB;')
        
        self.db_cursor.execute('DROP TABLE IF EXISTS genre')
        self.db_cursor.execute('CREATE TABLE IF NOT EXISTS film.genre '
                               ' (genre_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY'
                               ', genre_name VARCHAR(45) NOT NULL)'
                               'ENGINE = InnoDB;')
        
        self.db_cursor.execute('DROP TABLE IF EXISTS studio')
        self.db_cursor.execute('CREATE TABLE IF NOT EXISTS film.studio '
                               '(studio_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY'
                               ', studio_name VARCHAR(45) NOT NULL)'
                               'ENGINE = InnoDB;')
        
        self.db_cursor.execute('DROP TABLE IF EXISTS feature')
        self.db_cursor.execute('CREATE TABLE IF NOT EXISTS film.feature '
                               '(feature_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY'
                               ', feature_name VARCHAR(45) NOT NULL)'
                               'ENGINE = InnoDB;')
        
        self.db_cursor.execute('DROP TABLE IF EXISTS media')
        self.db_cursor.execute('CREATE TABLE IF NOT EXISTS film.media '
                               '(media_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY'
                               ', media_name VARCHAR(45) NOT NULL)'
                               'ENGINE = InnoDB;')
        
        self.db_cursor.execute('DROP TABLE IF EXISTS price')
        self.db_cursor.execute('CREATE TABLE IF NOT EXISTS film.price '
                               '(price_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY'
                               ', price_value FLOAT UNSIGNED NOT NULL)'
                               'ENGINE = InnoDB;')
        
        self.db_cursor.execute('DROP TABLE IF EXISTS movie_genre')
        self.db_cursor.execute('CREATE TABLE IF NOT EXISTS film.movie_genre '
                               '(movie_genre_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY'
                               ', movie_id INT UNSIGNED NOT NULL'
                               ', genre_id INT UNSIGNED NOT NULL'
                               ', INDEX movie_genre_fk1_idx (movie_id ASC) VISIBLE'
                               ', INDEX movie_genre_fk2_idx (genre_id ASC) VISIBLE'
                               ', CONSTRAINT movie_genre_fk1'
                               '    FOREIGN KEY (movie_id)'
                               '    REFERENCES film.movie (movie_id)'
                               '    ON DELETE CASCADE'
                               '    ON UPDATE CASCADE,'
                               '  CONSTRAINT movie_genre_fk2'
                               '    FOREIGN KEY (genre_id)'
                               '    REFERENCES film.genre (genre_id)'
                               '    ON DELETE CASCADE'
                               '    ON UPDATE CASCADE)'
                               'ENGINE = InnoDB;')
        
        self.db_cursor.execute('DROP TABLE IF EXISTS cast')
        self.db_cursor.execute('CREATE TABLE IF NOT EXISTS film.cast '
                               '(cast_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY'
                               ', movie_id INT UNSIGNED NOT NULL'
                               ', actor_id INT UNSIGNED NOT NULL'
                               ', INDEX cast_fk1_idx (movie_id ASC) VISIBLE'
                               ', INDEX cast_fk2_idx (actor_id ASC) VISIBLE'
                               ', CONSTRAINT cast_fk1'
                               '    FOREIGN KEY (movie_id)'
                               '    REFERENCES film.movie (movie_id)'
                               '    ON DELETE CASCADE'
                               '    ON UPDATE CASCADE,'
                               '  CONSTRAINT cast_fk2'
                               '    FOREIGN KEY (actor_id)'
                               '    REFERENCES film.actor (actor_id)'
                               '    ON DELETE CASCADE'
                               '    ON UPDATE CASCADE)'
                               'ENGINE = InnoDB;')
        
        self.db_cursor.execute('DROP TABLE IF EXISTS movie_feature')
        self.db_cursor.execute('CREATE TABLE IF NOT EXISTS film.movie_feature '
                               '(movie_feature_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY'
                               ', movie_id INT UNSIGNED NOT NULL'
                               ', feature_id INT UNSIGNED NOT NULL'
                               ', INDEX movie_feature_fk1_idx (movie_id ASC) VISIBLE'
                               ', INDEX movie_feature_fk2_idx (feature_id ASC) VISIBLE'
                               ', CONSTRAINT movie_feature_fk1'
                               '    FOREIGN KEY (movie_id)'
                               '    REFERENCES film.movie (movie_id)'
                               '    ON DELETE CASCADE'
                               '    ON UPDATE CASCADE,'
                               '  CONSTRAINT movie_feature_fk2'
                               '    FOREIGN KEY (feature_id)'
                               '    REFERENCES film.feature (feature_id)'
                               '    ON DELETE CASCADE'
                               '    ON UPDATE CASCADE)'
                               'ENGINE = InnoDB;')
        
        self.db_cursor.execute('DROP TABLE IF EXISTS movie_media')
        self.db_cursor.execute('CREATE TABLE IF NOT EXISTS film.movie_media '
                               '( movie_media_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY'
                               ', movie_id INT UNSIGNED NOT NULL'
                               ', media_id INT UNSIGNED NOT NULL'
                               ', price_id INT UNSIGNED NULL'
                               ', INDEX movie_media_fk1_idx (media_id ASC) VISIBLE'
                               ', INDEX movie_media_fk2_idx (movie_id ASC) VISIBLE'
                               ', INDEX movie_media_fk3_idx (price_id ASC) VISIBLE'
                               ', CONSTRAINT movie_media_fk1'
                               '    FOREIGN KEY (movie_id)'
                               '    REFERENCES film.movie (movie_id)'
                               '    ON DELETE CASCADE'
                               '    ON UPDATE CASCADE,'
                               '  CONSTRAINT movie_media_fk2'
                               '    FOREIGN KEY (media_id)'
                               '    REFERENCES film.media (media_id)'
                               '    ON DELETE CASCADE'
                               '    ON UPDATE CASCADE,'
                               '  CONSTRAINT movie_media_fk3'
                               '    FOREIGN KEY (price_id)'
                               '    REFERENCES film.price (price_id)'
                               '    ON DELETE CASCADE'
                               '    ON UPDATE CASCADE)'
                               'ENGINE = InnoDB;')
        
        self.db_cursor.execute('DROP TABLE IF EXISTS movie_studio')
        self.db_cursor.execute('CREATE TABLE IF NOT EXISTS film.movie_studio '
                               '( movie_studio_id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY'
                               ', movie_id INT UNSIGNED NOT NULL'
                               ', studio_id INT UNSIGNED NOT NULL'
                               ', INDEX movie_studio_fk1_idx (movie_id ASC) VISIBLE'
                               ', INDEX movie_studio_fk2_idx (studio_id ASC) VISIBLE'
                               ', CONSTRAINT movie_studio_fk1'
                               '    FOREIGN KEY (movie_id)'
                               '    REFERENCES film.movie (movie_id)'
                               '    ON DELETE CASCADE'
                               '    ON UPDATE CASCADE,'
                               '  CONSTRAINT movie_studio_fk2'
                               '    FOREIGN KEY (studio_id)'
                               '    REFERENCES film.studio (studio_id)'
                               '    ON DELETE CASCADE'
                               '    ON UPDATE CASCADE)'
                               'ENGINE = InnoDB;')
        

        self.mydb.commit()
        print('Database created/reset')
        print('\n')


    # def add_movie(self, movie_first_name, movie_last_initial, movie_hire_status, movie_hire_date):
    #     self.db_cursor.execute('USE film')
    #     self.db_cursor.execute('INSERT INTO movie (movie_first_name, movie_last_initial, movie_hire_status, movie_hire_date) VALUES (%s, %s, %s, %s)',
    #                     (movie_first_name, movie_last_initial, movie_hire_status, movie_hire_date))
    #     self.mydb.commit()
    #     print('movie added')
    #     print('\n')