#include <stdio.h>
#include "sdk.h"

int main(int argc, char* argv[]) {
    int i;
    int a=1, b=1;

    for(i = 0; i < argc; i++) {
        printf("[%d]: %s\n", i, argv[i]);
    }

    printf("sdk_add(%d, %d) = %d\n", a, b, sdk_add(a, b));

    return 0;
}
