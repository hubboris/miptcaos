#ifndef INT_VEC_H
#define INT_VEC_H

#include <stddef.h>

/* Динамически расширяемый массив целых чисел. */
typedef struct {
    int *data;        /* указатель на выделенный блок памяти */
    size_t size;      /* сколько элементов сейчас хранится */
    size_t capacity;  /* сколько элементов помещается в выделенный блок */
} IntVec;

/* Создаёт пустой массив: выделяет память на 4 элемента (size = 0, capacity = 4). */
void vec_init(IntVec *v);

/* Добавляет x в конец. Если массив заполнен (size == capacity), увеличивает
   ёмкость вдвое через realloc. Возвращает 0 при успехе и -1, если память
   выделить не удалось (тогда уже сохранённые данные остаются целыми). */
int vec_push(IntVec *v, int x);

/* Освобождает память и обнуляет поля (data = NULL, size = 0, capacity = 0). */
void vec_free(IntVec *v);

#endif
