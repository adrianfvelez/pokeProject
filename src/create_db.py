# -*- coding: utf-8 -*-
"""
En este módulo se maneja la creación de la base de datos y se implementan funciones para su fácil manejo.
"""

import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """
    Crea una conexión con la base de datos de SQLite

    :param db_file: nombre del archivo de la base de datos.
    :return:        conexión con la base.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """
    Función para crear tablas en la base de datos.

    :param conn: conexión
    :param create_table_sql: sentencia de sql para crear una tabla
    :return:      - - -
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def sql_crear_usuario(conn, usr):
    """
    Función para insertar en la tabla usuario

    :param conn: conexión
    :param create_table_sql: tupla de datos a insertar
    :return:      - - -
    """
    sql = ''' INSERT INTO usuario(id,name)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, usr)
    conn.commit()
    return cur.lastrowid


def sql_crear_pokemon(conn, pokemon):
    """
    Función para insertar en la tabla pokemon

    :param conn: conexión
    :param create_table_sql: tupla de datos a insertar
    :return:      - - -
    """
    sql = ''' INSERT INTO pokemon(id,name)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, pokemon)
    conn.commit()
    return cur.lastrowid


def sql_crear_atrapado(conn, atrapado):
    """
    Función para insertar en la tabla atrapado

    :param conn: conexión
    :param create_table_sql: tupla de datos a insertar
    :return:      - - -
    """
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
    """
    Función para buscar usuario por id en la base de datos.

    :param conn: conexión
    :param id: id del usuario a buscar
    :return: tupla con datos del usuario
    """
    cursorObj = conn.cursor()
    cursorObj.execute("SELECT * FROM usuario WHERE id='"+str(id)+"'")
    rows = cursorObj.fetchone()
    return rows


def get_all_pokemones_from_usuario(conn,id):
    """
    Función para buscar todos los pokemon de un usuario

    :param conn: conexión
    :param id: id del usuario a buscar
    :return: lista con tuplas de datos de los pokemones
    """
    cursorObj = conn.cursor()
    cursorObj.execute("SELECT id FROM atrapado INNER JOIN pokemon ON atrapado.id_pokemon=pokemon.id WHERE atrapado.id_usuario='"+str(id)+"'")
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
    """
    Función pricipal del módulo que crea y pobla la base con pokemones y usuarios predeterminados.

    :param conn: conexión
    :param id: id del usuario a buscar
    :return: tupla con datos del usuario
    """

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

        print("BASE TERMINADA")

    else:
        print("No se pudo conectar la base de datos.")


if __name__ == '__main__':
    main()
