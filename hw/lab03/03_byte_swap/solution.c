#include <stdio.h>
#include <stdint.h>

int main(void) {
    uint32_t num;
    
    if (scanf("%u", &num) != 1) {
        return 1;
    }

    uint32_t res = ((num & 0xFF000000) >> 24) |
                   ((num & 0x00FF0000) >> 8)  |
                   ((num & 0x0000FF00) << 8)  |
                   ((num & 0x000000FF) << 24);

    printf("Decimal: %u\n", res);
    printf("Hex: 0x%08X\n", res);

    return 0;
}
