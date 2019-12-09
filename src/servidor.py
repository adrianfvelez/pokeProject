#Código para el servidor

import socket
from codigos_mensajes import *
from struct import pack
from socket import timeout
from random import randint
import _thread

def enviaMensaje(conn,msg):
	conn.sendall(msg)

def conexionConCliente(conn):
	try:
		sesion_iniciada = False #bandera para saber si ya inició sesión
		id_solicitado = conn.recv(2) # primer mensaje que recibe el servidor, con id de usuario
		id_usuario = id_solicitado[1]
		while sesion_iniciada == False:
			#checar que el mensaje sea correcto y exista el usuario
			if id_solicitado[0] == ENVIO_IP and id_usuario == 1:
				sesion_iniciada = True
				enviaMensaje(conn,pack('B',ID_ENCONTRADO))
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
		while msg_recibido[0] != SALIR:
			#si se solicita una consulta de pokemon
			if msg_recibido[0] == CONSULTA_POKEMON:
				enviaMensaje(conn,pack('B',LISTA_POKEMON))
				msg_recibido = conn.recv(2)
			elif msg_recibido[0] == SOLICITA_CAPTURA:
				#generar un pokemon aleatorio
				#checar si ya tiene todos
				todos= False
				if todos:
					enviaMensaje(conn,pack('B',NO_MAS_CAPTURAS))
					msg_recibido = conn.recv(2)
					continue
				inicio_captura = True
				#checar si el usuario lo tiene
				if repetido:
					enviaMensaje(conn,pack('B',POKEMON_REPETIDO))
					msg_recibido = conn.recv(1)
					continue
				#si no tiene todos ni esta repetido
				enviaMensaje(conn,pack('B',CAPTURAR_POKEMON))
				msg_recibido = conn.recv(1)
				continue
			elif msg_recibido[0] == SI:
				#la primera ve que dice que sí se inicializan sus intentos
				if inicio_captura:
					intentos_restantes = 5
					inicio_captura = False
					pkg1 = pack('B',INTENTAR_CAPTURA)
					pkg2 = pack('B',1)
					pkg3 = pack('B',1)
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
					enviaMensaje(conn,pack('B',ENVIO_POKEMON))
					msg_recibido = conn.recv(2)
				#si no hay exito en la captura
				else:
					print("FALLÓ :(\n")
					intentos_restantes = intentos_restantes-1
					pkg1 = pack('B',INTENTAR_CAPTURA)
					pkg2 = pack('B',1)
					pkg3 = pack('B',1)
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

