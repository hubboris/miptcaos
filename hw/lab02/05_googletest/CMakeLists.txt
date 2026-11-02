cmake_minimum_required(VERSION 3.15)
project(CalcGTestProject)

set(CMAKE_CXX_STANDARD 17)

include(FetchContent)
FetchContent_Declare(
    googletest
    URL https://github.com/google/googletest/archive/refs/tags/v1.14.0.zip
)
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

add_library(math_lib STATIC calc.cpp calc.h)

add_executable(calc_tests tests.cpp)

target_link_libraries(calc_tests PRIVATE math_lib gtest_main)

include(CTest)
enable_testing()
gtest_discover_tests(calc_tests)
