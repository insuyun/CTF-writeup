int main()
{
  int t = time(0);
  srand(t);
  int i;
  for (i = 0; i < 1024; i++)
  {
    printf("%x\n", rand());
  }
}
