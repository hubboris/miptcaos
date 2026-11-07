CC = gcc
CFLAGS = -Wall -Wextra
TARGET = solution
SRCS = main.c my_strcmp.c

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(SRCS) my_strcmp.h
	$(CC) $(CFLAGS) -o $@ $(SRCS)

clean:
	rm -f $(TARGET)
