#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int width;
    int height;
    int *data;
} Matrix;

typedef struct Cell {
    int val;
    int r;
    int c;
    struct Cell *link;
} Cell;

Cell *makeCell(int r, int c, int v) {
    Cell *p = (Cell *)malloc(sizeof(Cell));
    p->val  = v;
    p->r    = r;
    p->c    = c;
    p->link = NULL;
    return p;
}

Cell *toSparse(Matrix *m) {
    Cell *front = NULL;
    Cell *rear  = NULL;
    int total   = m->height * m->width;

    for (int k = 0; k < total; k++) {
        if (m->data[k] == 0) continue;

        int ri = k / m->width;
        int ci = k % m->width;

        Cell *p = makeCell(ri, ci, m->data[k]);
        if (front == NULL) {
            front = rear = p;
        } else {
            rear->link = p;
            rear       = p;
        }
    }
    return front;
}

void printCells(Cell *front) {
    for (Cell *p = front; p != NULL; p = p->link)
        printf("(row=%d, col=%d, value=%d)\n", p->r, p->c, p->val);
}

void printMatrix(Matrix *m) {
    for (int i = 0; i < m->height; i++) {
        for (int j = 0; j < m->width; j++)
            printf("%d ", m->data[i * m->width + j]);
        printf("\n");
    }
}

Matrix *applyThreshold(Matrix *m) {
    Matrix *out   = (Matrix *)malloc(sizeof(Matrix));
    out->width    = m->width;
    out->height   = m->height;
    out->data     = (int *)malloc(m->height * m->width * sizeof(int));

    int cutoff = 3;
    int sz     = m->height * m->width;

    for (int i = 0; i < sz; i++)
        out->data[i] = (m->data[i] >= cutoff) ? 1 : 0;

    return out;
}

void detectEdges(Cell *front, Matrix *m) {
    for (Cell *p = front; p != NULL; p = p->link) {
        int onEdge = 0;
        int idx;

        idx = (p->r - 1) * m->width + p->c;
        if (p->r > 0 && m->data[idx] == 0)
            onEdge = 1;

        idx = (p->r + 1) * m->width + p->c;
        if (!onEdge && p->r < m->height - 1 && m->data[idx] == 0)
            onEdge = 1;

        idx = p->r * m->width + (p->c - 1);
        if (!onEdge && p->c > 0 && m->data[idx] == 0)
            onEdge = 1;

        idx = p->r * m->width + (p->c + 1);
        if (!onEdge && p->c < m->width - 1 && m->data[idx] == 0)
            onEdge = 1;

        if (onEdge)
            printf("(row=%d, col=%d, value=%d)\n", p->r, p->c, p->val);
    }
}

Matrix *invertBinary(Matrix *m) {
    int sz = m->height * m->width;
    for (int i = 0; i < sz; i++)
        m->data[i] = (m->data[i] == 0) ? 1 : 0;

    printMatrix(m);
    Cell *sp = toSparse(m);
    printCells(sp);
    return m;
}

Matrix *rebuildMatrix(Cell *sp, Matrix *ref) {
    Matrix *res  = (Matrix *)malloc(sizeof(Matrix));
    res->height  = ref->height;
    res->width   = ref->width;
    res->data    = (int *)calloc(ref->height * ref->width, sizeof(int));

    for (Cell *p = sp; p != NULL; p = p->link)
        res->data[p->r * res->width + p->c] = p->val;

    printMatrix(res);
    return res;
}

int main() {
    Matrix *img  = (Matrix *)malloc(sizeof(Matrix));
    img->height  = 5;
    img->width   = 5;
    img->data    = (int *)malloc(img->height * img->width * sizeof(int));

    int hotSpots[] = {2, 6, 7, 8, 10, 11, 12, 13, 14, 16, 17, 18, 22};
    int numSpots   = sizeof(hotSpots) / sizeof(hotSpots[0]);

    for (int i = 0; i < 25; i++) {
        img->data[i] = 0;
        for (int j = 0; j < numSpots; j++) {
            if (i == hotSpots[j]) {
                img->data[i] = 5;
                break;
            }
        }
    }

    printMatrix(img);

    Matrix *mask = applyThreshold(img);
    printf("\n");
    printMatrix(mask);

    Cell *sp = toSparse(mask);
    printCells(sp);
    detectEdges(sp, mask);

    Matrix *inv    = invertBinary(mask);
    Cell   *invSp  = toSparse(inv);
    rebuildMatrix(invSp, inv);

    return 0;
}
