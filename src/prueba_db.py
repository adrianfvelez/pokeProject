from create_db import *

conn = create_connection(db_nombre)

if conn is not None:
    #REEGISTRO DE POKEMONES ATRAPADOS

    sql_crear_atrapado(conn,(0,2)) #<<<<<<<<< para guardar que el usuario 0 atrapó el pokemon 2
    print( get_usuario_by_id(conn,1) ) #regresa usuario 1
    print( get_all_pokemones_from_usuario(conn,0) ) #regresa todos los pokemones del usuario 0

else:
    print("No se pudo conectar la base")
