#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
  long hex;

  if (argc != 2) {
    printf("Usage: %s <int>\n", argv[0]);
    return 0;
  }

  hex = strtol(argv[1], NULL, 16);
  if ((hex & 14) == 14 || (hex & 13) == 13 || (hex & 11) == 11 || (hex & 7) == 7) {
    puts("3 of last 4 bits are on");
  } else {
    puts("3 of last 4 bits are not set");
  }

  printf("pre-reversal: %x\n", hex & 0x0000FFFF);
  printf("bytes reversed: %x\n", (hex << 8 | ((hex >> 8) & 0xFF)) & 0xFFFF);
  printf("rotated 4 bits: %x\n", (hex >> 4 | ((hex & 0xF) << 12)) & 0xFFFF);

  return 0;
}
