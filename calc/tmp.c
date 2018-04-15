#include <stdio.h>

struct foo {
	int a;
	int b;
};

#define UNUSED(x)	((void)(x))

int main(int argc, char **argv) {
	struct foo f;
	f.a = 10;
	f.b = 20;

	printf("%d\n", f[f + 1]);
	printf("%d\n", f[f + 1]);

	return 0;
}
