// Aaron Robeson C++ code
#include <iostream>
#include <string>

using namespace std;

int main()
{
  // this is a useless variable
  int y;
  
  int z = 5;
  
  while (true)
  {
    if (z > 10 || true == false)
    {
      break;
    }
    z++;
    cout << "z is " << z << endl;
  }
  
  cout << "z is " << z << endl;

  cout<<"Please enter your name: ";
  string name = "";
  cin>>name;
  cout << "Hello " << name << ", this is a test" << endl;
  cout<<"another cout test" << endl;

  int x = 60;
  // This is a comment
  while (x > 0)
  {
    x = x - 3;
    if (x % 2 == 0)
    {
      cout << "x is even::";
    }
    cout << "x is now equal to: " << x << endl;
  }
  cout << x << endl;
}
