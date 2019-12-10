# -*- coding: utf-8 -*-
"""
En este modulo se encuentra la implementación de la aplicación para el servidor del juego de Pokemón.
"""
import socket
from codigos_mensajes import *
from struct import pack
from socket import timeout
from random import randint
import _thread
from create_db import *

def enviaMensaje(conn,msg):
	"""
	Envía un mensaje msg a través de la conexión conn

	:param conn: conexión
	:param msg:  mensaje
	:return:      - - -
	"""
	conn.sendall(msg)

def conexionConCliente(conn):
	"""
	Función que se usa en un thread para atender las conexiones de los clientes. En esta se implementa todo el flujo para el servidor.

	:param conn: conexión
	:return:      - - -
	"""
	try:
		pokemones = [0,1,2,3,4,5,6,7,8,9]
		nombres_pokemon = ['pikachu','raichu','squirtle','warturtle','pidgey','pidgeotto','charmander','charmeleon','bulbasaur','ivysaur']
		pokemones_pre = [0,2,4,6,8]
		nombres_pokemon_pre = ['pikachu','squirtle','pidgey','charmander','bulbasaur']
		pokemones_ev = [1,3,5,7,9]
		nombres_pokemon_ev = ['raichu','warturtle','pidgeotto','charmeleon','ivysaur']
		connDB = create_connection(db_nombre)
		if(connDB is None):
			print("FATAL ERROR. NO BASE DE DATOS")
			return
		sesion_iniciada = False #bandera para saber si ya inició sesión
		id_solicitado = conn.recv(2) # primer mensaje que recibe el servidor, con id de usuario
		id_usuario = id_solicitado[1]
		while sesion_iniciada == False:
			#checar que el mensaje sea correcto y exista el usuario
			if id_solicitado[0] == ENVIO_IP and (id_usuario in [0,1,2]):
				sesion_iniciada = True
				pkg1 = pack('B',ID_ENCONTRADO)
				pkg2 = pack('B',id_usuario)
				enviaMensaje(conn,pkg1+pkg2)
				break
			#si no existía el ID, se envía mensaje de que no estaba
			elif id_usuario != 1:
				enviaMensaje(conn,pack('B',ID_NO_ENCONTRADO))
			#espera un nuevo mensaje del cliente, sobre si quiere reintentar o salir
			id_solicitado = conn.recv(2)
			#si el cliente no quiere continuar, se le manda mensaje de cerrar sesion
			if id_solicitado[0] == NO:
				enviaMensaje(conn,pack('B',TERMINANDO_SESION))
				conn.close()
				return
			else:
				id_usuario = id_solicitado[1]
		#Aquí ya se ha iniciado sesión
		print("Se ha iniciado la sesión de:"+str(id_usuario))
		msg_recibido = conn.recv(2)
		repetido = False #bandera para saber si el usuario ya tiene el pokémon
		inicio_captura = False #bandera para saber si se comenzará a capturar un pokémon
		intentos_restantes = 0 #numero de intentos que quedan
		id_pokemon = 10
		while msg_recibido[0] != SALIR:
			#si se solicita una consulta de pokemon
			if msg_recibido[0] == CONSULTA_POKEMON:
				pkg1 = pack('B',LISTA_POKEMON)
				pkg2 = pack('B',id_usuario)
				all_poke_usuario = get_all_pokemones_from_usuario(connDB,id_usuario)
				pkg_send = pkg1 + pkg2
				for i in all_poke_usuario:
					pkg_send = pkg_send + pack('B',i[0])
				enviaMensaje(conn,pkg_send)
				msg_recibido = conn.recv(2)
			elif msg_recibido[0] == SOLICITA_CAPTURA:
				#generar un pokemon aleatorio de acuerdo a los que no ha atrapado de preevoluciones
				all_poke_usuario = get_all_pokemones_from_usuario(connDB,id_usuario)
				already_have_this = []
				for i in all_poke_usuario:
					already_have_this.append(i[0])
				disponibles = list(set(pokemones).symmetric_difference(set(already_have_this)))
				#checar si ya tiene todos
				todos = len(already_have_this) == 10
				if todos:
					enviaMensaje(conn,pack('B',NO_MAS_CAPTURAS))
					msg_recibido = conn.recv(2)
					continue
				ran_poke = randint(0,9)
				while ran_poke % 2 == 1 or ((ran_poke+1) in already_have_this):
					ran_poke = randint(0,9)
				print(ran_poke)
				id_pokemon = ran_poke
				inicio_captura = True
				repetido = ran_poke in already_have_this
				if repetido:
					id_pokemon = id_pokemon+1
					pkg1 = pack('B',POKEMON_REPETIDO)
					pkg2 = pack('B',id_usuario)
					pkg3 = pack('B',id_pokemon)
					enviaMensaje(conn,pkg1+pkg2+pkg3)
					msg_recibido = conn.recv(1)
					continue
				#si no tiene todos ni esta repetido
				pkg1 = pack('B',CAPTURAR_POKEMON)
				pkg2 = pack('B',id_usuario)
				pkg3 = pack('B',id_pokemon)
				enviaMensaje(conn,pkg1+pkg2+pkg3)
				msg_recibido = conn.recv(1)
				continue
			elif msg_recibido[0] == SI:
				#la primera ve que dice que sí se inicializan sus intentos
				if inicio_captura:
					intentos_restantes = 5
					inicio_captura = False
					pkg1 = pack('B',INTENTAR_CAPTURA)
					pkg2 = pack('B',id_usuario)
					pkg3 = pack('B',id_pokemon)
					pkg4 = pack('B',intentos_restantes)
					enviaMensaje(conn,pkg1+pkg2+pkg3+pkg4)
					msg_recibido = conn.recv(1)
					continue
				#si se acaban los intentos
				if intentos_restantes == 0:
					print("SE ACABARON LOS INTENTOS\n")
					enviaMensaje(conn,pack('B',NO_MAS_INTENTOS))
					msg_recibido = conn.recv(2)
					continue
				#generar aletorio
				exito_captura = randint(0,10) < 3
				#si hubo exito en la captura
				if exito_captura:
					print("POKEMON CAPTURADO\n")
					sql_crear_atrapado(connDB,(id_usuario,id_pokemon))
					pkg1 = pack('B',ENVIO_POKEMON)
					pkg2 = pack('B',id_usuario)
					pkg3 = pack('B',id_pokemon)
					enviaMensaje(conn,pkg1+pkg2+pkg3)
					msg_recibido = conn.recv(2)
				#si no hay exito en la captura
				else:
					print("FALLÓ :(\n")
					intentos_restantes = intentos_restantes-1
					pkg1 = pack('B',INTENTAR_CAPTURA)
					pkg2 = pack('B',id_usuario)
					pkg3 = pack('B',id_pokemon)
					pkg4 = pack('B',intentos_restantes)
					enviaMensaje(conn,pkg1+pkg2+pkg3+pkg4)
					msg_recibido = conn.recv(1)
			#si se recibe un mensaje de NO
			else:
				enviaMensaje(conn,pack('B',RECIBIDO))
				print("RECIBIDO")
				msg_recibido = conn.recv(2)

		enviaMensaje(conn,pack('B',TERMINANDO_SESION))
		conn.close()
	except timeout:
		conn.close()
		print("El tiempo de espera se terminó. Se cerró la conexión")

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = socket.gethostname()
puerto = 9999
s.bind((host,puerto))
print("Inicializando servidor Pokémon")
s.listen(5)
print("Escuchando")

while True:
	conn, address = s.accept()
	conn.settimeout(60)
	print("Conectado con:",address)
	#se inicia un nuevo hilo con una nueva conexión con cliente
	_thread.start_new_thread(conexionConCliente,(conn,))
	#aquiiniciaria el nuevo hilo. Llamar funcion del nuevo hilo
