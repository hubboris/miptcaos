CXX = g++
CXXFLAGS = -Wall -Wextra -std=c++17

TARGET = calculator
SRCS = main.cpp calc.cpp
OBJS = $(SRCS:%.cpp=obj/%.o)

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $^

obj/%.o: %.cpp | obj
	$(CXX) $(CXXFLAGS) -c $< -o $@

obj:
	mkdir -p obj

clean:
	rm -rf obj $(TARGET)
