#include <fcntl.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>
#include <signal.h>

#define PHONE_NUMBER_SIZE 0x100
#define NAME_SIZE 0x100
#define PASSWORD_SIZE 32*2
#define ID_SIZE 0x40

typedef struct _node {
  char phone_number[PHONE_NUMBER_SIZE];
  char *name;
  struct _node* next;
} node;

char root_credential[PASSWORD_SIZE + ID_SIZE + 1];
node* header = NULL;

void signal_handler(int signo)
{
        exit(0);
}

void read_string(char* buf, int size)
{
  fgets(buf, size, stdin);
  int str_size = strlen(buf);
  if (str_size >= 1 && buf[str_size - 1] == '\n')
    buf[str_size - 1] = '\0';
}

void add()
{
  char name[NAME_SIZE];
  char phone_number[PHONE_NUMBER_SIZE];
  write(1, "Enter your name\n", 16);
  read_string(name, NAME_SIZE);
  write(1, "Enter your phone number\n", 24);
  read_string(phone_number, PHONE_NUMBER_SIZE);

  node* new = calloc(1, sizeof(node));
  strcpy(new->phone_number, phone_number);
  new->name = strdup(name);

  if (header == NULL)
    header = new;
  else
  {
    node* ptr = header;
    while(ptr->next != NULL)
    {
      ptr = ptr->next;
    }
    ptr->next = new;
  }
  write(1, "Successfully added\n", 19);
}
int get_num()
{
	char buf[2];
	read(0, buf, 2);
	return atoi(buf);
}

void delete()
{
  int num = 0;
  write(1, "Enter node number to delete\n", 28);
  num = get_num();

  if (num == 0)
  {
    if(header == NULL)
    {
      write(1, "Error : no such phone number\n", 29);
      return ;
    }
    //delete header
    free(header->name);
    free(header);
    header = header->next;
  }
  else
  {
    node* ptr = header;
    node* prev = NULL;
    int i = 0;
    for (i = 0; i < num; i++)
    {
      ptr = ptr->next;
      prev = ptr;

      if (ptr == NULL)
      {
        write(1, "Error : no such phone number\n", 29);
        return;
      }

    }

    prev->next = ptr->next;
    free(ptr->name);
    free(ptr);
  }
}

void show()
{
  node* ptr = header;
  write(1, "Printing phone number\n", 22);
  while(ptr != NULL)
  {
    printf("[*] Name : %s, Phone number : %s\n", ptr->name, ptr->phone_number);
    ptr = ptr->next;
  }
}

void print_banner()
{
  write(1, "==================================\n", 35);
  write(1, "Welcome to the phonebook\n", 25);
  write(1, "==================================\n", 35);
}

void hidden_menu()
{
  unsigned char credential[ID_SIZE + PASSWORD_SIZE + 1 + 3 + 10];
  unsigned char id[ID_SIZE + 1];
  unsigned char password[PASSWORD_SIZE + 1];

  write(1, "I want to get a shell\n", 22);
  write(1, "Enter ID\n", 9);
  fgets(id, ID_SIZE + 1, stdin);
  write(1, "Enter Password\n", 15);
  fgets(password, PASSWORD_SIZE + 1, stdin);
  sprintf(credential, "ID=%s&PW=%s", id, password);

  if (!strcmp(root_credential, credential))
  {
	system("/bin/sh");
  }
  else
  {
    write(1, "Authentication failed\n", 22);
  }
}

void create_root_credential()
{
  unsigned char chr;
  unsigned char p[3];
  int i = 0;
  int fd = open("/home/phonebook/key", O_RDONLY);

  strcpy(root_credential, "ID=ROOT&PW=");
  read(fd, root_credential + 11, 20);
  root_credential[11+20] = '\0';
  close(fd);
}

void print_menu()
{
  write(1, "Choose a menu\n", 14);
  write(1, "1. Add\n", 7);
  write(1, "2. Delete\n", 10);
  write(1, "3. Show\n", 8);
  write(1, "4. Bye\n", 7);
}

int main()
{
	char choice[2];
	char buf[3];
	//alarm(5);
	signal(SIGALRM, signal_handler);
	print_banner();
	create_root_credential();

        while(true)
        {
    print_menu();
    read(0, choice,  2);

    switch(choice[0])
    {
      case '1':
        add();
        break;
      case '2':
        delete();
        break;
       case '3':
        show();
        break;
       case '4':
        write(1, "Thank you :)\n", 13);
        exit(0);
        break;
       case '5':
        hidden_menu();
        break;
       default:
        write(1, "Wrong menu number.\n", 19);
        break;
    }
        }

}

