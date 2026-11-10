#include <stdio.h>
#include "int_vec.h"

int main(void) {
    IntVec v;
    int x;

    vec_init(&v);
    if (v.data == NULL) {
        fprintf(stderr, "Error: out of memory\n");
        return 1;
    }

    /* Читаем числа до первого отрицательного (или до конца ввода). */
    while (scanf("%d", &x) == 1 && x >= 0) {
        if (x % 2 == 0 && vec_push(&v, x) != 0) {
            fprintf(stderr, "Error: out of memory\n");
            vec_free(&v);
            return 1;
        }
    }

    for (size_t i = 0; i < v.size; i++) {
        printf(i ? " %d" : "%d", v.data[i]);
    }
    printf("\n");
    printf("Count: %zu\n", v.size);
    printf("Capacity: %zu\n", v.capacity);

    vec_free(&v);
    return 0;
}
