#include <rclcpp/rclcpp.hpp>
using namespace std;

class PersonNode : public rclcpp::Node  //定义一个PersonNode类让其继承于node
{
//添加属性，在C++中有私有成员，公共成员和保护成员这样区分
//声明
private:  //私有成员
    std::string name_;
    int age_;
public:  //添加完属性,构造函数在C++里面就要跟类的名字一模一样，没有任何返回值
    PersonNode(const std::string &node_name,const std::string &name,const int &age)
    :Node(node_name)  //因为我们继承到这里还有一个额外的要求，要求调用父类
    //传入之后要把它赋值到类内部的属性里面去
    {
        this->name_ = name;
        this->age_ = age;
    };
    //const作用是不希望用户在函数内做修改
    void eat(const std::string & food_name)  //方法
    {
        RCLCPP_INFO(this->get_logger(),"我是%s,%d岁,爱吃%s",this->name_.c_str(),this->age_,food_name.c_str());
        //C++版本:  (this->get_logger(),"我是" <<this->name_ << "," << this->age_ << "岁，爱吃" << food_name);
        //用这个类跟用cpp_node方法一样
    };
};


int main(int argc,char** argv)
{
    rclcpp::init(argc,argv);
    auto node = std::make_shared<PersonNode>("person_node","李斯",18);
    RCLCPP_INFO(node->get_logger(),"Hello");
    //此处node是一个指针
    node->eat("鱼香肉丝");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}