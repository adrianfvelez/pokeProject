#Código del cliente

import socket
from codigos_mensajes import *
from struct import pack

def enviaMensaje(conn,msg):
	conn.sendall(msg)

#función que mantiene la conexión cuando se esta intentando capturar un pokémon
def capturar_pokemon(s,mensaje):
	recibido = s.recv(4)
	#mientras se siga intentando capturar
	while recibido[0] == INTENTAR_CAPTURA:
		print(recibido[3])
		intentos = recibido[3]
		intenta = input("Quedan "+str(intentos)+" intentos. ¿Quieres lanzar una pokébola?\n1)Si\n2)No\n")
		if intenta == "1":
			enviaMensaje(s,pack('B',SI))
			recibido = s.recv(4096)
		else:
			enviaMensaje(s,pack('B',NO))
			s.recv(1)
			break
	#ya no se sigue intentando la captura
	if recibido[0] == ENVIO_POKEMON:
		#mostrar la imagen aqui
		print("AQUI ESTA TU PIKACHU")
	elif recibido[0] == NO_MAS_INTENTOS:
		print("El pokémon se ha escapado :(\n")

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = socket.gethostname()
port = 9999

s.connect((host,port))
print("Conectado a POKEMON GO")

#aquí comienza la conexión

print("BIENVENIDO")
msg_code_recibido = 0
#manda su ID hasta que este en la base
while msg_code_recibido != ID_ENCONTRADO:
	id_usuario = int(input("Ingrese el ID de usuario con el que quiere jugar:"))
	pkg1 = pack('B',ENVIO_IP)
	pkg2 = pack('B',id_usuario)
	enviaMensaje(s,pkg1+pkg2)
	msg_recibido = s.recv(2)
	msg_code_recibido = msg_recibido[0]

#en este punto ya se inicio sesión

respuesta = 0 #para saber qué eligió el usuario
tipo_mensaje = 0 #el tipo de mensaje que se esta recibiendo
while tipo_mensaje != TERMINANDO_SESION:
	while not (respuesta == "1" or respuesta == "2" or respuesta == "3"):
		respuesta = input(
			"¿qué desea realizar?"+
			"\n1)Capturar pokémon"+
			"\n2)Consultar mis pokémon"+
			"\n3)Salir")
	#si se quiere capturar un pokemon
	if respuesta == "1":
		enviaMensaje(s,pack('B',SOLICITA_CAPTURA))
		respuesta = 0
		msg_recibido = s.recv(4)
		captura = 0
		#si ya se capturó a todos
		if msg_recibido[0] == NO_MAS_CAPTURAS:
			print("FELICIDADES. HAS ATRAPADO A TODOS\n")
			pass
		elif msg_recibido[0] == CAPTURAR_POKEMON:
			#decodificar qué pokemon apareció
			captura = input("Un pikachu salvaje ha aparecido, ¿deseas capturarlo?"+
				"\n1)Sí"+
				"\n2)No\n")
		else:
			captura = input("Un pikachu salvaje ha aparecido pero parece que ya lo has capturado antes, "+
				"¿deseas capturar a su evolución o escapar?"+
				"\n1)Capturar evolución"+
				"\n2)Escapar\n")
		if captura == "1":
			enviaMensaje(s,pack('B',SI))
			capturar_pokemon(s,msg_recibido)
		else:
			enviaMensaje(s,pack('B',NO))
			msg_recibido = s.recv(1)
			tipo_mensaje = msg_recibido[0]
	#si se quiere consultar lista de pokemon
	elif respuesta == "2":
		enviaMensaje(s,pack('B',CONSULTA_POKEMON))
		respuesta = 0
		msg_recibido = s.recv(4096)
		if msg_recibido[0] == LISTA_POKEMON:
			#imprimir la lista de pokemon
			print("AQUI VA LA LISTA DE POKEMON\n")
	#si se quiere salir
	else:
		enviaMensaje(s,pack('B',SALIR))
		respuesta = 0
		msg_recibido = s.recv(1)
		tipo_mensaje = msg_recibido[0]

#se cierra la conexión
print("GRACIAS POR JUGAR. SE CIERRA LA CONEXIÓN")
s.close()
