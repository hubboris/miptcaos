#include <stdio.h>

int main(void) {
    unsigned long long addr, align;
    
    if (scanf("%llu %llu", &addr, &align) != 2) {
        return 1;
    }

    if (addr % align == 0) {
        printf("Aligned: yes\n");
        printf("Down: %llu\n", addr);
        printf("Up: %llu\n", addr);
    } else {
        printf("Aligned: no\n");
        unsigned long long down = addr - (addr % align);
        unsigned long long up = down + align;
        printf("Down: %llu\n", down);
        printf("Up: %llu\n", up);
    }

    return 0;
}
