#include <stdio.h>
#include "hello.h"
#include "goodbye.h"

int main(int argc, char* argv[])
{
    printf("-----main-----\n");
    for(int i = 0; i < argc ; i++) {
        printf("argv[%d] = %s\n", i, argv[i]);
    }

    hello_world(3);
    goodbye_name("Jack");

    return 0;
}
