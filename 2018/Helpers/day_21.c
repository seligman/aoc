#include <stdio.h>
#include <stdlib.h>
#ifdef _MSC_VER
typedef __int64 int64_t;
#else
#include <stdint.h>
#endif

#if !defined(max)
#define max(a, b) ((a) > (b) ? (a) : (b)) 
#endif
 
typedef struct avl_node {
    int data;
    struct avl_node * left;
    struct avl_node * right;
    int height;
} avl_node;

avl_node* find(int e, avl_node* t) {
    if (t == NULL) {
        return NULL;
    } else if (e < t->data) {
        return find( e, t->left );
    } else if(e > t->data) {
        return find(e, t->right);
    } else {
        return t;
    }
}
 
static int height(avl_node* n) {
    if (n == NULL) {
        return -1;
    } else {
        return n->height;
    }
}

static avl_node* single_rotate_with_left(avl_node* k2) {
    avl_node* k1 = NULL;
 
    k1 = k2->left;
    k2->left = k1->right;
    k1->right = k2;
 
    k2->height = max(height(k2->left), height(k2->right)) + 1;
    k1->height = max(height(k1->left), k2->height) + 1;
    return k1;
}
 
static avl_node* single_rotate_with_right(avl_node* k1) {
    avl_node* k2;
 
    k2 = k1->right;
    k1->right = k2->left;
    k2->left = k1;
 
    k1->height = max(height(k1->left), height(k1->right)) + 1;
    k2->height = max(height(k2->right), k1->height) + 1;
 
    return k2;
}
 
static avl_node* double_rotate_with_left(avl_node* k3) {
    k3->left = single_rotate_with_right(k3->left);
    return single_rotate_with_left(k3);
}
 
static avl_node* double_rotate_with_right(avl_node* k1) {
    k1->right = single_rotate_with_left( k1->right );
    return single_rotate_with_right( k1 );
}
 
avl_node* insert(int e, avl_node* t) {
    if (t == NULL) {
        t = (avl_node*)malloc(sizeof(avl_node));
        if (t == NULL) {
            exit(1);
        } else {
            t->data = e;
            t->height = 0;
            t->left = t->right = NULL;
        }
    } else if (e < t->data) {
        t->left = insert(e, t->left);
        if (height(t->left) - height(t->right) == 2) {
            if (e < t->left->data) {
                t = single_rotate_with_left(t);
            } else {
                t = double_rotate_with_left(t);
            }
        }
    } else if (e > t->data) {
        t->right = insert(e, t->right);
        if (height(t->right) - height(t->left) == 2) {
            if (e > t->right->data) {
                t = single_rotate_with_right(t);
            } else {
                t = double_rotate_with_right(t);
            }
        }
    }
 
    t->height = max(height(t->left), height(t->right)) + 1;
    return t;
}

// -------------------------------------------------------------------------------------------------

void main() {
    int r0 = 0, r1 = 0, r2 = 0, r3 = 0, r4 = 0, r5 = 0;
    int * ip = &r1;
    int64_t frames = 0;
    int halt = 0;
    int first_value = -1;
    int last_value = -1;

    avl_node * root;
    int shown = 0;

    while (halt == 0) {
        switch(*ip) {
            case   0: /* seti 123 0 2         */ r2 = 123;                 (*ip)++; frames++; 
            case   1: /* bani 2 456 2         */ r2 = r2 & 456;            (*ip)++; frames++; 
            case   2: /* eqri 2 72 2          */ r2 = (r2 == 72) ? 1 : 0;  (*ip)++; frames++; 
            case   3: /* addr 2 1 1           */ r1 = r2 + r1;             (*ip)++; frames++;  break;
            case   4: /* seti 0 0 1           */ r1 = 0;                   (*ip)++; frames++;  break;
            case   5: /* seti 0 3 2           */ r2 = 0;                   (*ip)++; frames++; 
            case   6: /* bori 2 65536 5       */ r5 = r2 | 65536;          (*ip)++; frames++; 
            case   7: /* seti 4843319 1 2     */ r2 = 4843319;             (*ip)++; frames++; 
            case   8: /* bani 5 255 4         */ r4 = r5 & 255;            (*ip)++; frames++; 
            case   9: /* addr 2 4 2           */ r2 += r4;                 (*ip)++; frames++; 
            case  10: /* bani 2 16777215 2    */ r2 = r2 & 16777215;       (*ip)++; frames++; 
            case  11: /* muli 2 65899 2       */ r2 = r2 * 65899;          (*ip)++; frames++; 
            case  12: /* bani 2 16777215 2    */ r2 = r2 & 16777215;       (*ip)++; frames++; 
            case  13: /* gtir 256 5 4         */ r4 = (256 > r5) ? 1 : 0;  (*ip)++; frames++; 
            case  14: /* addr 4 1 1           */ r1 = r4 + r1;             (*ip)++; frames++;  break;
            case  15: /* addi 1 1 1           */ r1++;                     (*ip)++; frames++;  break;
            case  16: /* seti 27 4 1          */ r1 = 27;                  (*ip)++; frames++;  break;
            case  17: /* seti 0 7 4           */ r4 = 0;                   (*ip)++; frames++; 
            case  18: /* addi 4 1 3           */ r3 = r4 + 1;              (*ip)++; frames++; 
            case  19: /* muli 3 256 3         */ r3 = r3 * 256;            (*ip)++; frames++; 
            case  20: /* gtrr 3 5 3           */ r3 = (r3 > r5) ? 1 : 0;   (*ip)++; frames++; 
            case  21: /* addr 3 1 1           */ r1 = r3 + r1;             (*ip)++; frames++;  break;
            case  22: /* addi 1 1 1           */ r1++;                     (*ip)++; frames++;  break;
            case  23: /* seti 25 0 1          */ r1 = 25;                  (*ip)++; frames++;  break;
            case  24: /* addi 4 1 4           */ r4++;                     (*ip)++; frames++; 
            case  25: /* seti 17 0 1          */ r1 = 17;                  (*ip)++; frames++;  break;
            case  26: /* setr 4 1 5           */ r5 = r4;                  (*ip)++; frames++; 
            case  27: /* seti 7 3 1           */ r1 = 7;                   (*ip)++; frames++;  break;
            case  28: /* eqrr 2 0 4           */ {
                    struct LL * cur;
                    struct LL * temp;

                    if (first_value == -1) {
                        first_value = r2;
                    }

                    if (find(r2, root)) {
                        printf("------------------------------------------------------------\n");
                        printf("------ Found end! ------------------------------------------\n");
                        printf("  Shown:       %9d\n", shown);
                        printf("  Frames:    %11I64d\n", frames);
                        printf("  First Value: %9d\n", first_value);
                        printf("  Last Value:  %9d\n", last_value);
                        printf("------------------------------------------------------------\n");
                        return;
                    }

                    last_value = r2;

                    shown++;
                    if (shown % 2500 == 1) {
                        printf("Shown: %5d, Current value: %d\n", shown, r2);
                    }

                    root = insert(r2, root);

                    r4 = (r2 == r0) ? 1 : 0;
                    (*ip)++;
                    frames++;
                }
            case  29: /* addr 4 1 1           */ r1 = r4 + r1;             (*ip)++; frames++;  break;
            case  30: /* seti 5 3 1           */ r1 = 5;                   (*ip)++; frames++;  break;
            default:                             halt = 1; break;
        }

        // fprintf(stdout, "IP: %d, Frames: %I64d, r: [%d, %d, %d, %d, %d, %d]\n", *ip, frames, r0, r1, r2, r3, r4, r5);
    }
}
