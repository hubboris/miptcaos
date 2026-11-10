#include <stdio.h>
#include "swap_pairs.h"

#define MAX_N 1000
#define GUARD 0x7EADBEEF

int main(void) {
    int n;

    if (scanf("%d", &n) != 1 || n < 0 || n > MAX_N) {
        return 1;
    }

    /* Массив на стеке; по краям — «сторожевые» значения для проверки выхода за границы. */
    int buf[MAX_N + 2];
    int *arr = buf + 1;

    buf[0] = GUARD;
    buf[n + 1] = GUARD;
    for (int i = 0; i < n; i++) {
        if (scanf("%d", &arr[i]) != 1) {
            return 1;
        }
    }

    swap_pairs(arr, n);

    if (buf[0] != GUARD || buf[n + 1] != GUARD) {
        fprintf(stderr, "Error: out-of-bounds write detected\n");
        return 2;
    }

    for (int i = 0; i < n; i++) {
        printf(i ? " %d" : "%d", arr[i]);
    }
    printf("\n");
    return 0;
}
