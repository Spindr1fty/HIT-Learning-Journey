#include <iostream>
#include <memory>
using namespace std;

int main()
{
    auto p1 = make_shared<string>("This is a str."); // make_shared<数据类型/类>(参数);返回值就是一个共享指针对应类的返回值
    cout << "p1的引用计数：" << p1.use_count() << "指向内存地址：" << p1.get() << endl; //1
   
    auto p2 = p1;
    cout << "p1的引用计数：" << p1.use_count() << "指向内存地址：" << p1.get() << endl; //2
    cout << "p2的引用计数：" << p2.use_count() << "指向内存地址：" << p2.get() << endl; //2

    p1.reset(); //释放引用,不指向"This is a str."所在内存
    cout << "p1的引用计数：" << p1.use_count() << "指向内存地址：" << p1.get() << endl; //0
    cout << "p2的引用计数：" << p2.use_count() << "指向内存地址：" << p2.get() << endl; //2-1=1

    cout<<"p2的指向内存地址数据："<< p2->c_str()<<endl; //调用成员方法  "This is a str"

    return 0;
}