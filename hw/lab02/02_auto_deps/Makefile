CXX = g++
CXXFLAGS = -Wall -Wextra -std=c++17 -MMD -MP
TARGET = calculator
SRCS = $(wildcard *.cpp)
OBJS = $(patsubst %.cpp,obj/%.o,$(SRCS))
DEPS = $(OBJS:.o=.d)

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $^

obj/%.o: %.cpp | obj
	$(CXX) $(CXXFLAGS) -c $< -o $@

obj:
	mkdir -p obj

-include $(DEPS)

clean:
	rm -rf obj $(TARGET)
