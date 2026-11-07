#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "my_strcmp.h"

#define MAX_LEN 1024

/* Читает строку без символа перевода строки. Возвращает 0 при EOF. */
static int read_line(char *buf, size_t size) {
    if (fgets(buf, (int)size, stdin) == NULL) {
        return 0;
    }
    size_t len = strlen(buf);
    if (len > 0 && buf[len - 1] == '\n') {
        buf[len - 1] = '\0';
    }
    return 1;
}

int main() {
    char a[MAX_LEN], b[MAX_LEN], line[MAX_LEN];

    if (!read_line(line, sizeof line)) {
        return 1;
    }
    int n = atoi(line);

    for (int i = 0; i < n; i++) {
        if (!read_line(a, sizeof a) || !read_line(b, sizeof b)) {
            return 1;
        }
        int r = my_strcmp(a, b);
        puts(r < 0 ? "less" : r > 0 ? "greater" : "equal");
    }
    return 0;
}
