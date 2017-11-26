CC=gcc
FLAGS=-g -O -Wall

all: server.exe client.exe test-program.exe

server.exe: server.c
	$(CC) $(FLAGS) -o $@ $^
client.exe: client.c
	$(CC) $(FLAGS) -o $@ $^
test-program.exe: test-program.c
	$(CC) $(FLAGS) -o $@ $^