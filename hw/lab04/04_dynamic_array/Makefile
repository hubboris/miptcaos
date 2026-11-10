CC = gcc
CFLAGS = -Wall -Wextra
TARGET = solution
SRCS = main.c int_vec.c

.PHONY: all asan clean

all: $(TARGET)

$(TARGET): $(SRCS) int_vec.h
	$(CC) $(CFLAGS) -o $@ $(SRCS)

# Сборка с санитайзерами (проверка утечек памяти и выходов за границы)
asan: $(SRCS) int_vec.h
	$(CC) $(CFLAGS) -g -fsanitize=address,undefined -o solution_asan $(SRCS)

clean:
	rm -f $(TARGET) solution_asan
