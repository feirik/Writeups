CC=gcc
CFLAGS=
LFLAGS= -lm

all: thesis

%.o : %.c
	@echo " Started to compile $@"
	@$(CC) $(CFLAGS) -c -o $@ $<

thesis.o: thesis.c

thesis: thesis.o
	@echo -e " Linking $@"
	@$(CC) $(CFLAGS) $^ $(LFLAGS) -o $@

clean: 
	rm thesis.o thesis
