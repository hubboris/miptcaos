#include <stdio.h>

int main(void) {
    unsigned long long price;
    
    if (scanf("%llu", &price) != 1) {
        return 1;
    }

    unsigned long long vat = (price * 20 + 50) / 100;
    unsigned long long total = price + vat;

    printf("VAT: %llu\n", vat);
    printf("Total: %llu\n", total);

    return 0;
}
