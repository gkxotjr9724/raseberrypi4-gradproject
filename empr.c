#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <signal.h>
#include <string.h>

#define MAX_BUFF 32
int main(void)
{
	int push_dev;
	int fnd_dev;
	int text_lcd_dev;
	int motor_dev;
	int dot_dev;

	unsigned char string[40] = "Welcome to 3leg squid game! \n";
	unsigned char retval2;
	unsigned char verify[4];
	unsigned char pb_buff[9];
	int buff_size;
	buff_size = sizeof(push_sw_buff);
	int str_size;
	
	unsigned char fpga_number[10][10] = {
		{0x3e, 0x7f, 0x63, 0x73, 0x73, 0x6f, 0x67, 0x63, 0x7f, 0x3e}, // 0
		{0x0c, 0x1c, 0x1c, 0x0c, 0x0c, 0x0c, 0x0c, 0x0c, 0x0c, 0x1e}, // 1
		{0x7e, 0x7f, 0x03, 0x03, 0x3f, 0x7e, 0x60, 0x60, 0x7f, 0x7f}, // 2
		{0xfe, 0x7f, 0x03, 0x03, 0x7f, 0x7f, 0x03, 0x03, 0x7f, 0x7e}, // 3
		{0x66, 0x66, 0x66, 0x66, 0x66, 0x66, 0x7f, 0x7f, 0x06, 0x06}, // 4
		{0x7f, 0x7f, 0x60, 0x60, 0x7e, 0x7f, 0x03, 0x03, 0x7f, 0x7e}, // 5
		{0x60, 0x60, 0x60, 0x60, 0x7e, 0x7f, 0x63, 0x63, 0x7f, 0x3e}, // 6
		{0x7f, 0x7f, 0x63, 0x63, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03}, // 7
		{0x3e, 0x7f, 0x63, 0x63, 0x7f, 0x7f, 0x63, 0x63, 0x7f, 0x3e}, // 8
		{0x3e, 0x7f, 0x63, 0x63, 0x7f, 0x3f, 0x03, 0x03, 0x03, 0x03}, // 9
	};
	dot_dev = open("/dev/fpga_dot", O_WRONLY);
	push_dev = open("/dev/fpga_push_switch",O_RDWR);
	fnd_dev = open("/dev/fpga_push_switch",O_RDWR);
	text_lcd_dev = open("/dev/fpga_push_switch",O_RDWR);
	motor_dev = open("/dev/fpga_push_switch",O_RDWR);

	if(push_dev<0)
	{
		printf("PS error\n");
		close(push_dev);
		return -1;
	}	
	if(fnd_dev<0)
	{
		printf("FND error\n");
		close(fnd_dev);
		return -1;
	}
	if(text_lcd_dev<0)
	{
		printf("Tlcd error\n");
		close(text_lcd_dev);
		return -1;
	}
	if(motor_dev<0)
	{
		printf("motor error\n");
		close(motor_dev);
		return -1;
	}
	if(dot_dev<0)
	{
		printf("Dot error \n");
		close(dot_dev);
		return -1;
	}
	while(1)
	{
	char* text_value = "5678";
	retval = write(fnd_dev, text_value, 4);
	
	write(text_lcd_dev"                                ", MAX_BUFF);
	write(text_lcd_dev"Welcome to 3leg squid game!",MAX_BUFF);

	for(int i = 0; i<str_size; i++)
	{
		verify[i] = text_value[i] - 0x30;
	}
	write(dot_dev, fpga_number[7], str_size);
	usleep(1000000);

	}
	close(push_dev);
	close(dot_dev);
	close(fnd_dev);
	clode(text_lcd_dev);

	return 0
}
