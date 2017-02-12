#include <stdio.h>

int main(void) {
  printf("char: %d bytes\n", sizeof(char));
  printf("unsigned char: %d bytes\n", sizeof(unsigned char));
  printf("short: %d bytes\n", sizeof(short));
  printf("int: %d bytes\n", sizeof(int));
  printf("unsigned int: %d bytes\n", sizeof(unsigned int));
  printf("unsigned long: %d bytes\n", sizeof(unsigned long));
  printf("float: %d bytes\n", sizeof(float));
  return 0;
}
