#include <iostream>
#include <algorithm>
using namespace std;

int main()
{
    auto add = [](int a, int b) -> int
    { return a + b; };
    int sum = add(100, 100);
    auto print_sum = [sum]() -> void //特殊写法：[&]表示上下文的所有的参数全部捕获
    {
        cout << sum << endl;
    };

    print_sum();

    return 0;
}