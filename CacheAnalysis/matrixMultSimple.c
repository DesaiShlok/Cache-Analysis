#include <stdio.h>

#define SIZE 64

int main() {
    // Initialize two 64x64 matrices
    int A[SIZE][SIZE];
    int B[SIZE][SIZE];
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            A[i][j] = i + j;
            B[i][j] = i * j;
        }
    }

    // Result matrix, initialized to zeros
    int CMult[SIZE][SIZE] = {{0}};

    // Perform standard matrix multiplication
    for (int i = 0; i < SIZE; i++) {
        for (int j = 0; j < SIZE; j++) {
            for (int k = 0; k < SIZE; k++) {
                CMult[i][j] += A[i][k] * B[k][j];
            }
        }
    }
    printf("Matrix multiplication complete");

    return 0;
}