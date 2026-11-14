#include <stdlib.h>
#include "int_vec.h"

void vec_init(IntVec *v) {
    v->capacity = 4;
    v->count = 0;
    v->data = malloc(v->capacity * sizeof(int));
    
    if (v->data == NULL) {
        v->capacity = 0;
    }
}

int vec_push(IntVec *v, int x) {
    if (v->count == v->capacity) {
        int new_capacity = (v->capacity == 0) ? 4 : (v->capacity * 2);
        
        int *new_data = realloc(v->data, new_capacity * sizeof(int));
        
        if (new_data == NULL) {
            return -1;
        }
        
        v->data = new_data;
        v->capacity = new_capacity;
    }

    v->data[v->count] = x;
    v->count++;
    
    return 0;
}

void vec_free(IntVec *v) {
    if (v->data != NULL) {
        free(v->data);
    }
    v->data = NULL;
    v->count = 0;
    v->capacity = 0;
}
