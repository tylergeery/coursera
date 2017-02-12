#include <stdio.h>

#define ARRAY_LENGTH(arr) (sizeof(arr)/sizeof(arr[0]))

int main(void) {
  const char chars[] = {'t', 'B', '1', '\n', '\t', ' '};

  for (int i = 0, l = ARRAY_LENGTH(chars); i < l; i++) {
    int code = (int)chars[i];
    printf("char: %c, char code: %d\n", chars[i], code);

    if ((code == 10) || (code == 9) || (code == 32)) {
      puts("whitespace");
    } else if (code < 65) {
      puts("digit");
    } else if (code < 91) {
      puts("uppercase");
    } else {
      puts("lowercase");
    }
  }
}
