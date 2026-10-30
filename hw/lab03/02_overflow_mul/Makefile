CC = gcc
CFLAGS = -Wall -Wextra
TARGET = solution

.PHONY: all clean

all: $(TARGET)

$(TARGET): solution.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(TARGET)
