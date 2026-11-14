#include "my_strcmp.h"

int my_strcmp(const char *a, const char *b) {

    while (*a != '\0' && *a == *b) {
        a++;
        b++;
    }


    unsigned char char_a = (unsigned char)*a;
    unsigned char char_b = (unsigned char)*b;
    return char_a - char_b;
}
