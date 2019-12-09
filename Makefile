run_servidor:
	@cd src && python3 servidor.py

run_cliente:
	@cd src && python3 cliente.py

documentacion:
	sudo cp mandocs/servidor.1 /usr/local/share/man/man1/servidor.1
	sudo cp mandocs/cliente.1 /usr/local/share/man/man1/cliente.1
	sudo mandb

docs_servidor:
	@man ./mandocs/servidor.1

docs_cliente:
	@man ./mandocs/cliente.1

install:
	@cd src && python3 create_db.py

uninstall:
	@rm src/pokemon.db
