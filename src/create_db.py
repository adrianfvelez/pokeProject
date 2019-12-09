import sqlite3
from sqlite3 import Error

#Regresa la conexión a la base de datos
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def sql_crear_usuario(conn, usr):
    sql = ''' INSERT INTO usuario(id,name)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, usr)
    conn.commit()
    return cur.lastrowid


def sql_crear_pokemon(conn, pokemon):
    sql = ''' INSERT INTO pokemon(id,name)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, pokemon)
    conn.commit()
    return cur.lastrowid


def sql_crear_atrapado(conn, atrapado):
    try:
        sql = ''' INSERT INTO atrapado(id_usuario,id_pokemon) VALUES(?,?) '''
        cur = conn.cursor()
        cur.execute(sql, atrapado)
        conn.commit()
        return cur.lastrowid
    except:#ya lo atrpo
        print("ya lo atrapó")
        return None

def get_usuario_by_id(conn,id):
    cursorObj = conn.cursor()
    cursorObj.execute("SELECT * FROM usuario WHERE id='"+str(id)+"'")
    rows = cursorObj.fetchone()
    return rows

def get_all_pokemones_from_usuario(conn,id):
    cursorObj = conn.cursor()
    cursorObj.execute("SELECT id,name FROM atrapado INNER JOIN pokemon ON atrapado.id_pokemon=pokemon.id WHERE atrapado.id_usuario='"+str(id)+"'")
    rows = cursorObj.fetchall()
    return rows




db_nombre = r"pokemon.db"

tabla_usuario = """ CREATE TABLE IF NOT EXISTS usuario (
                        id integer PRIMARY KEY,
                        name text NOT NULL
                    ); """

tabla_pokemon = """CREATE TABLE IF NOT EXISTS pokemon (
                    id integer PRIMARY KEY,
                    name text NOT NULL
                );"""

tabla_atrapados = """CREATE TABLE IF NOT EXISTS atrapado(
                        id_usuario integer NOT NULL,
                        id_pokemon integer NOT NULL,
                        FOREIGN KEY (id_usuario) REFERENCES usuario(id),
                        FOREIGN KEY (id_pokemon) REFERENCES pokemon(id),
                        UNIQUE (id_usuario, id_pokemon)
                    );"""

def main():

    # conexión db
    conn = create_connection(db_nombre)

    # creacion de tablas
    if conn is not None:
        # creación de tablas
        create_table(conn, tabla_usuario)
        create_table(conn, tabla_pokemon)
        create_table(conn, tabla_atrapados)

        #REGISTRO DE USUARIOS
        nombres = ['Lisandro','Velez','America']
        for i in range(len(nombres)):
            usr = (i, nombres[i])
            sql_crear_usuario(conn, usr)

        #REISTRO DE POKEMONES
        nombres_pokemon = ['pikachu','raichu','squirtle','warturtle','pidgey','pidgeotto','charmander','charmeleon','bulbasaur','ivysaur']
        for i in range(len(nombres_pokemon)):
            pokemon = (i, nombres_pokemon[i])
            sql_crear_pokemon(conn, pokemon)

        #REEGISTRO DE POKEMONES ATRAPADOS
        sql_crear_atrapado(conn,(1,8))


        print("BASE TERMINADA")

    else:
        print("No se pudo conectar la base de datos.")


if __name__ == '__main__':
    main()
