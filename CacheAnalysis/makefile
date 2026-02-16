# Compiler to use
CC = gcc
# Compiler flags
# -Wall -> Show all warnings
# -g    -> Include debug information
# -o    -> Specify the output file name
CFLAGS = -Wall -g
# The name of our final executable
TARGET1 = matrixMultSimple
TARGET2 = matrixBlocked

# This is the default rule that runs when you just type "make"
# It says the "all" target depends on the "matrix" target
all: $(TARGET1) $(TARGET2)

# This rule tells make how to build the target "matrixMultSimple"
$(TARGET1): matrixMultSimple.c
	$(CC) $(CFLAGS) -o $(TARGET1) matrixMultSimple.c

# This rule tells make how to build the target "matrixBlocked"
$(TARGET2): matrixBlocked.c
	$(CC) $(CFLAGS) -o $(TARGET2) matrixBlocked.c

# This is a "phony" rule to clean up compiled files
# It doesn't build a file named "clean"
.PHONY: clean
clean:
	rm -f $(TARGET1) $(TARGET2) *.o