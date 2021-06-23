create extension dblink;


DROP FUNCTION f_create_db(text);
CREATE OR REPLACE FUNCTION f_create_db(dbname text)
  RETURNS void AS
$func$
BEGIN

IF EXISTS (SELECT 1 FROM pg_database WHERE datname = dbname) THEN
   RAISE NOTICE 'Database already exists';
ELSE
   PERFORM dblink_exec('dbname=' || current_database()   -- current db
                     , 'CREATE DATABASE ' || quote_ident(dbname));
END IF;

END
$func$ LANGUAGE plpgsql;



DECLARE
   line library%rowtype;
   usage_line integer;
   usage_book_id integer;
   user_usage double precision := 0;
   total_usage double precision := 0;
BEGIN
   
   FOR usage_line IN
      SELECT book_id FROM usage
      LOOP
         total_usage = total_usage + 1;
      END LOOP;
   
    FOR line IN
        SELECT * FROM library
        LOOP
         user_usage = 0;
         FOR usage_book_id IN
            SELECT book_id FROM usage WHERE book_id = line.book_id
            LOOP
            
            user_usage = user_usage + 1;
            
            END LOOP;
      
         UPDATE library
         SET popularity = user_usage / total_usage WHERE library.id = line.id;
        END LOOP;
    RETURN NEW;
END;



CREATE FUNCTION insert_into_book(id integer, name varchar(256), page_count integer)
  RETURNS void AS
  $BODY$
      BEGIN
        INSERT INTO book
        VALUES(id, name, page_count);
      END;
$BODY$
LANGUAGE plpgsql;



CREATE FUNCTION insert_into_lib_user(id integer, first_name varchar(256), last_name varchar(256), birth_date date, book_count integer)
  RETURNS void AS
  $BODY$
      BEGIN
        INSERT INTO lib_user
        VALUES(id , first_name, last_name, birth_date, book_count);
      END;
$BODY$
LANGUAGE plpgsql;



CREATE FUNCTION insert_into_usage(id integer, user_id integer, book_id integer)
  RETURNS void AS
  $BODY$
      BEGIN
        INSERT INTO usage
        VALUES(id, user_id, book_id);
      END;
$BODY$
LANGUAGE plpgsql;




CREATE FUNCTION insert_into_library(id integer, book_id integer, book_count integer, popularity integer)
  RETURNS void AS
  $BODY$
      BEGIN
        INSERT INTO library
        VALUES(id, book_id, book_count);
      END;
$BODY$
LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION delete_value_by_ID(table varchar(256), id_ integer)
  RETURNS void AS
$func$ 
BEGIN

   DELETE FROM table WHERE id = id_;

END
$func$ 
LANGUAGE plpgsql;


-----------------------


CREATE FUNCTION create_table_book()
  RETURNS void AS
  $BODY$
      BEGIN
         CREATE TABLE book (
            id serial not null,
            name varchar(256),
            page_count integer not null,
            primary key(id)
         );
      END
$BODY$
LANGUAGE plpgsql;



CREATE FUNCTION create_table_lib_user()
  RETURNS void AS
  $BODY$
      BEGIN
        CREATE TABLE lib_user (
         id serial not null, 
         first_name varchar(256), 
         last_name varchar(256), 
         birth_date date, 
         book_count integer,
         primary key(id)
         );
      END
$BODY$
LANGUAGE plpgsql;



CREATE FUNCTION create_table_usage()
  RETURNS void AS
  $BODY$
      BEGIN
        CREATE TABLE usage (
         id serial not null, 
         user_id integer REFERENCES lib_user (id), 
         book_id integer REFERENCES book (id),
         primary key(id)
         );
      END
$BODY$
LANGUAGE plpgsql;



CREATE FUNCTION create_table_library()
  RETURNS void AS
  $BODY$
      BEGIN
        CREATE TABLE library (
         id serial not null,
         book_id integer REFERENCES book (id), 
         book_count integer default 0, 
         popularity integer default 0,
         primary key(id)
         );
      END
$BODY$
LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION delete_value_by_ID(table varchar(256), id_ integer)
  RETURNS void AS
$func$ 
BEGIN

   DELETE FROM table WHERE id = id_;

END
$func$ 
LANGUAGE plpgsql;
