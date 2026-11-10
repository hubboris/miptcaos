CC = gcc
CFLAGS = -Wall -Wextra
TARGET = solution
SRCS = main.c swap_pairs.c

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(SRCS) swap_pairs.h
	$(CC) $(CFLAGS) -o $@ $(SRCS)

clean:
	rm -f $(TARGET)
