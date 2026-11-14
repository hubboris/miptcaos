cmake_minimum_required(VERSION 3.15)
project(CalcProject)

include(FetchContent)
FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG        v1.14.0
)
set(INSTALL_GTEST OFF CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

add_library(math_lib STATIC calc.cpp)
add_executable(calc_tests tests.cpp)
target_link_libraries(calc_tests PRIVATE math_lib GTest::gtest_main)
include(CTest)
enable_testing()
gtest_discover_tests(calc_tests)
