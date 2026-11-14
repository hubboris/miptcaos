#include <stdio.h>
#include <limits.h>

int main(void) {
    int a, b;
    
    if (scanf("%d %d", &a, &b) != 2) {
        return 1;
    }

    long long res = (long long)a * b;

    if (res > INT_MAX || res < INT_MIN) {
        printf("Overflow\n");
    } else {
        printf("Product: %lld\n", res);
    }

    return 0;
}
