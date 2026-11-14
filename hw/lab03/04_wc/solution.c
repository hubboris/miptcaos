#include <stdio.h>

int main(void) {
    int c;
    unsigned long long chars = 0;
    unsigned long long words = 0;
    unsigned long long lines = 0;
    int in_word = 0;

    while ((c = getchar()) != EOF) {
        chars++;

        if (c == '\n') {
            lines++;
        }

        if (c == ' ' || c == '\t' || c == '\n') {
            in_word = 0;
        } else {
            if (!in_word) {
                words++;
                in_word = 1;
            }
        }
    }

    printf("Chars: %llu\n", chars);
    printf("Words: %llu\n", words);
    printf("Lines: %llu\n", lines);

    return 0;
}
