#include <stdio.h>

double bytes2double(int high_byte, int low_byte)
{
	int bytes = high_byte * 256 + low_byte;
	double value = (double)bytes;
	printf("hb = %d lb = %d\n bytes = %d\n value = %f\n", high_byte, low_byte, bytes, value);	
	return value;
}
