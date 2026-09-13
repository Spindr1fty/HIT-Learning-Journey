#include <iostream>
#include <string>
using namespace std;
int main(int argc,char** argv)
{
    cout << "参数数量=" << argc << endl;
    cout << "程序名字=" << argv[0] << endl;
    string arg1 = argv[1];
    if(arg1 == "--help")
    {
        cout <<"这里是程序帮助，但是这个程序什么用都没有"<<endl;
    }
    return 0;
}