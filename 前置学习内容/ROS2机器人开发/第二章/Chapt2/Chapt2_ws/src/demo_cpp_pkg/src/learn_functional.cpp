#include <iostream>
#include <functional>
using namespace std;

// 自由函数

void save_with_free_fun(const string &file_name)
{
    cout << "自由函数：" << file_name << endl;
}

// 成员函数

class FileSave
{
private:
    /* data */
public:
    FileSave(/* args */) = default;
    ~FileSave() = default;

    void save_with_member_fun(const string &file_name)
    {
        cout << "成员方法函数：" << file_name << endl;
    };
};

int main()
{
    FileSave file_save;

    // Lambda函数

    auto save_with_lambda_fun = [](const string &file_name) -> void
    {
        cout << "Lambda函数：" << file_name << endl;
    };

    //三个函数功能一样但是调用的方法不一样
    //函数包装器可以将两种调用方法统一成一种
    /*
    save_with_free_fun("file.txt");
    file_save.save_with_member_fun("file.txt");
    save_with_lambda_fun("file.txt");
    */
    function<void(const string& )> save1 = save_with_free_fun;
    function<void(const string& )> save2 = save_with_lambda_fun;
    //成员函数放入包装器，在这里用到绑定语法，因为成员函数不能直接赋值
    //绑定语法：使用 bind 来进行二次绑定，bind 的参数有:
    //1.指针，这个指针是 file_save 这个对应类型的这个函数的指针，其可以让 bind 找到该函数的模板
    //为：&FileSave::save_with_member_fun
    //2.第二个参数是我们要替换的 file_save.save_with_member_fun 中 file_save 的这个对象
    //为：&file_save
    //3.第三个参数是要包装的这个目标函数的参数的数量和位置的这样一个占位符
    //因为在此就一个函数 save_with_member_function 含有一个参数，所以一个参数我们就用一个占为符即可
    //为：placeholders::_1
    function<void(const string& )> save3 = bind(&FileSave::save_with_member_fun,&file_save,placeholders::_1);

    //通过包装器包装后调用：
    //后续在学习ROS2的回调函数的时候经常会把成员函数作为回调函数使用
    //统一的调用方法：
    save1("file.txt"); 
    save2("file.txt");
    save3("file.txt");

    return 0;
}
