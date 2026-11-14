#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <limits.h>
int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <integer> [integer ...]\n", argv[0]);
        return 0;
    }

    long max_val = 0;
    long min_val = 0;
    int found_valid = 0;
    for (int i = 1; i < argc; i++) {
        char *endptr;
        errno = 0;
        long val = strtol(argv[i], &endptr, 10);
        if (endptr == argv[i] || *endptr != '\0' || errno == ERANGE) {
            fprintf(stderr, "Warning: skipping invalid argument \"%s\"\n", argv[i]);
            continue;
        }

        if (!found_valid) {
            max_val = val;
            min_val = val;
            found_valid = 1;
        } else {
            if (val > max_val) max_val = val;
            if (val < min_val) min_val = val;
        }
    }

    if (!found_valid) {
        fprintf(stderr, "Usage: %s <integer> [integer ...]\n", argv[0]);
    } else {
        printf("Max: %ld\n", max_val);
        printf("Min: %ld\n", min_val);
    }

    return 0;
}
