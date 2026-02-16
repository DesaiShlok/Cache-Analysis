#include <stdio.h>
#include <stdlib.h> // For malloc (if using dynamic allocation)

#define DIM 100 // Total dimension of the square matrices
#define BLOCK_SIZE 40 // Example block size (choose based on cache size)

int main() {
    // Declare matrices
    int src1[DIM][DIM];
    int src2[DIM][DIM];
    int tmp[DIM][DIM]; // To store the result

    // Initialize matrices (example initialization)
    // You can use a more complex init if you like
    for (int i = 0; i < DIM; i++) {
        for (int j = 0; j < DIM; j++) {
            src1[i][j] = i + j;
            src2[i][j] = i * j;
            tmp[i][j] = 0; // Initialize result matrix to zero
        }
    }

    // Compute the matrix product using tiling
    for (int row = 0; row < DIM; row += BLOCK_SIZE) {
        for (int col = 0; col < DIM; col += BLOCK_SIZE) {
            // These two loops iterate through blocks
            for (int blockRow = row; blockRow < row + BLOCK_SIZE; blockRow++) {
                for (int blockCol = col; blockCol < col + BLOCK_SIZE; blockCol++) {
                    double result = 0.0; // Use double for result to avoid overflow with large sums

                    // Compute the dot product for one element of the result matrix (tmp[blockRow][blockCol])
                    for (int dot = 0; dot < DIM; dot++) {
                        result += (double)src1[blockRow][dot] * src2[dot][blockCol];
                    }
                    tmp[blockRow][blockCol] = (int)result; // Store the result, cast back to int if needed
                }
            }
        }
    }

    printf("Tiled matrix multiplication complete\n");
    // Optionally print a value to verify
    // printf("Result tmp[0][0] = %d\n", tmp[0][0]);

    return 0;
}