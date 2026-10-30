CXX = g++
CXXFLAGS = -Wall -Wextra -std=c++17 -MMD -MP
MODE ?= release
ifeq ($(MODE), debug)
    OPT_FLAGS = -g -O0
else
    OPT_FLAGS = -O3
endif


OBJ_DIR = obj/$(MODE)
TARGET = calculator
SRCS = $(wildcard *.cpp)
OBJS = $(patsubst %.cpp,$(OBJ_DIR)/%.o,$(SRCS))
DEPS = $(OBJS:.o=.d)

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) $(OPT_FLAGS) -o $@ $^

$(OBJ_DIR)/%.o: %.cpp | $(OBJ_DIR)
	$(CXX) $(CXXFLAGS) $(OPT_FLAGS) -c $< -o $@

$(OBJ_DIR):
	mkdir -p $(OBJ_DIR)

-include $(DEPS)

clean:
	rm -rf obj $(TARGET)
