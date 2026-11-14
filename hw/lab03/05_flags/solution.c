#include <stdio.h>

int main(void) {
    unsigned char reg = 0;
    int cmd;

    while (scanf("%d", &cmd) == 1 && cmd != 0) {
        int n;
        switch (cmd) {
            case 1:
                if (scanf("%d", &n) == 1)
                    reg |= (1 << n);
                break;
            case 2:
                if (scanf("%d", &n) == 1)
                    reg &= ~(1 << n);
                break;
            case 3:
                if (scanf("%d", &n) == 1)
                    reg ^= (1 << n);
                break;
            case 4:
                for (int i = 7; i >= 0; i--) {
                    putchar(((reg >> i) & 1) ? '1' : '0');
                }
                putchar('\n');
                break;
        }
    }

    return 0;
}
