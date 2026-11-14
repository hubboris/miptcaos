#include "swap_pairs.h"

void swap_pairs(int *arr, int n) {
    for (int i = 0; i < n - 1; i += 2) {
        int *first = arr + i;
        int *second = arr + i + 1;
        int temp = *first;
        *first = *second;
        *second = temp;
    }
}
