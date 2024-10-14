#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

int main(void){

	unsigned long *ptr;
	int idx, val;

	printf("address: ");
	scanf("%ld", &ptr);
	
	printf("value: ");
	scanf("%i", &val);

	*ptr = (*ptr & ~((1<<16)-1)) | ((*ptr & 0xff) ^ ((val & 0xff) ^ ((val & 0xff) >> 1))) | (*ptr & 0xffff &~0xff);	
	
	exit(0);
}

__attribute__((constructor))
void init(void){
	setbuf(stdin, NULL);
	setbuf(stdout, NULL);
	setbuf(stderr, NULL);
}
