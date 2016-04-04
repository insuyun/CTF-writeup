#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <stdint.h>
#include <string.h>
#include <ctype.h>
#include <unistd.h>

#include "common.h"

void usage(char **argv)
{
	fprintf(stderr, "Usage: %s <Server IP>\n", argv[0]);
	exit(-1);
}

int main(int argc, char **argv)
{
	char buf[4096];
	bzero(buf, 4096);
	if (argc < 2) {
		usage(argv);
	}

	printf("Enter a string to capitalize => ");
	fgets(buf, 4096, stdin);
	int input_len = strnlen(buf, 4095) + 1;

	int sock = socket(AF_INET, SOCK_STREAM, 0);

	struct sockaddr_in srv_addr = {
		.sin_family = AF_INET,
		.sin_port = htons(1337),
		.sin_addr.s_addr = inet_addr(argv[1])
	};

	socklen_t addr_size = sizeof(srv_addr);

	connect(sock, (struct sockaddr *)&srv_addr, addr_size);
	request_t rq = {
		.msg_len = htonl(input_len),
		.type = 0,
	};
  rq.msg_len = htonl(4096);

	send(sock, &rq, sizeof(rq), 0);
	send(sock, buf, input_len, 0);

  while(1) {
	int size = recv(sock, buf, 4096, 0);
	size += recv(sock, buf + size, 4096, 0);
	buf[4095] = '\0';

  int i = 0;
  for (i = 0; i < 4096; i++) {
    printf("%c", buf[i]);
  }
  printf("\n");
	printf("Received: %s\n", buf);
  }

	return 0;
}
