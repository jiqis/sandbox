CC=gcc
FLAGS=-Wall

test: test.c queue.o
	$(CC) $(FLAGS) -o $@ $^

queue.o: queue.c queue.h
	$(CC) $(FLAGS) -c $<
