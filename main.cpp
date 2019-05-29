#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <vector>
#include <iostream>
#include <string>

using std::vector;
using std::string;

#define BUFFER_SIZE 1024

void execute_cmd(const char * fmt, ...) {
	char cmd[BUFFER_SIZE];

	int ret = 0;
	va_list ap;

	va_start(ap, fmt);
	vsprintf(cmd, fmt, ap);
	system(cmd);
	va_end(ap);
}

int main(int argc, char ** argv){
	/*
		Job list
		solar
		external
		device
		solarGen
						*/
	vector<string> topics{"solar", "external", "device", "solarGen"};

	int idx = 0;
	for(auto &i : topics){
		string cmd = "nohup python3 sub.py";
		cmd += i;
		cmd += " > log_sub_" + i + ".log &";
		std::cout << cmd << std::endl;
	}
}


