#include <stdio.h>
#include <stdlib.h>

struct Matrix {
    int width;
    int height;
    int *data;
};

void printMatrix(struct Matrix *img) {
    int r, c;
    for (r = 0; r < img->height; r++) {
        for (c = 0; c < img->width; c++) {
            printf("%d ", img->data[r * img->width + c]);
        }
        printf("\n");
    }
}

struct Matrix *applyThreshold(struct Matrix *img) {
    struct Matrix *result = (struct Matrix *)malloc(sizeof(struct Matrix));
    result->width  = img->width;
    result->height = img->height;
    result->data   = (int *)malloc(img->height * img->width * sizeof(int));

    int cutoff = 3;
    int total  = img->height * img->width;
    int k;
    for (k = 0; k < total; k++) {
        result->data[k] = (img->data[k] >= cutoff) ? 1 : 0;
    }
    return result;
}

struct LineQueue {
    int *buffer;
    int head;
    int tail;
    int capacity;
};

struct LineQueue *initQueue(int capacity) {
    struct LineQueue *q = (struct LineQueue *)malloc(sizeof(struct LineQueue));
    q->buffer   = (int *)malloc(capacity * sizeof(int));
    q->tail     = -1;
    q->head     = 0;
    q->capacity = capacity;
    return q;
}

int queueEmpty(struct LineQueue *q) {
    return (q->tail < q->head) ? 1 : 0;
}

struct LineQueue *pushQueue(struct LineQueue *q, int val) {
    if (q->tail == q->capacity - 1) {
        printf("queue overflow");
    } else {
        q->tail++;
        q->buffer[q->tail] = val;
    }
    return q;
}

struct LineQueue *popQueue(struct LineQueue *q) {
    if (queueEmpty(q)) {
        printf("queue underflow");
    } else {
        q->head++;
    }
    return q;
}

int frontValue(struct LineQueue *q) {
    return q->buffer[q->head];
}

int *runBFS(struct Matrix *mask, int origin) {
    int total = mask->height * mask->width;
    struct LineQueue *q = initQueue(total);
    int *seen = (int *)calloc(total, sizeof(int));

    seen[origin] = 1;
    pushQueue(q, origin);

    while (!queueEmpty(q)) {
        int cur = frontValue(q);
        q = popQueue(q);

        int r = cur / mask->width;
        int c = cur % mask->width;

        if (r > 0) {
            int above = cur - mask->width;
            if (mask->data[above] == 1 && seen[above] == 0) {
                seen[above] = 1;
                pushQueue(q, above);
            }
        }
        if (r < mask->height - 1) {
            int below = cur + mask->width;
            if (mask->data[below] == 1 && seen[below] == 0) {
                seen[below] = 1;
                pushQueue(q, below);
            }
        }
        if (c < mask->width - 1) {
            int nxt = cur + 1;
            if (mask->data[nxt] == 1 && seen[nxt] == 0) {
                seen[nxt] = 1;
                pushQueue(q, nxt);
            }
        }
        if (c > 0) {
            int prv = cur - 1;
            if (mask->data[prv] == 1 && seen[prv] == 0) {
                seen[prv] = 1;
                pushQueue(q, prv);
            }
        }
    }
    return seen;
}

void detectAndDraw(struct Matrix *mask, int *seen) {
    int rMin = mask->height, rMax = 0;
    int cMin = mask->width,  cMax = 0;
    int total = mask->height * mask->width;
    int i;

    for (i = 0; i < total; i++) {
        if (seen[i] == 1) {
            int r = i / mask->width;
            int c = i % mask->width;
            if (r < rMin) rMin = r;
            if (r > rMax) rMax = r;
            if (c < cMin) cMin = c;
            if (c > cMax) cMax = c;
        }
    }

    for (i = 0; i < total; i++) {
        int r = i / mask->width;
        int c = i % mask->width;
        if (r >= rMin && r <= rMax && c >= cMin && c <= cMax) {
            if (r == rMin || r == rMax || c == cMin || c == cMax) {
                mask->data[i] = 9;
            }
        }
    }

    int boxW = cMax - cMin + 1;
    int boxH = rMax - rMin + 1;
    int filledCount = 0;

    for (i = 0; i < total; i++) {
        if (seen[i] == 1) filledCount++;
    }

    if (filledCount == boxW * boxH) {
        printf("Rectangle detected\n");
    } else if (boxW == boxH) {
        printf("Circle detected\n");
    } else {
        printf("Unknown shape\n");
    }

    printMatrix(mask);
}

int main() {
    struct Matrix *image = (struct Matrix *)malloc(sizeof(struct Matrix));
    image->height = 5;
    image->width  = 5;
    image->data   = (int *)malloc(image->height * image->width * sizeof(int));

    int n;
    for (n = 0; n < 25; n++) {
        if (n == 2  || n == 6  || n == 7  || n == 8  ||
            n == 10 || n == 11 || n == 12 || n == 13 ||
            n == 14 || n == 16 || n == 17 || n == 18 || n == 22) {
            image->data[n] = 5;
        } else {
            image->data[n] = 0;
        }
    }

    printMatrix(image);
    struct Matrix *mask = applyThreshold(image);
    printf("\n");
    printMatrix(mask);

    int startIdx = -1;
    int total = mask->height * mask->width;
    int i;
    for (i = 0; i < total; i++) {
        if (mask->data[i] == 1) {
            startIdx = i;
            break;
        }
    }

    int *seen = runBFS(mask, startIdx);
    printf("\n");
    detectAndDraw(mask, seen);

    return 0;
}
