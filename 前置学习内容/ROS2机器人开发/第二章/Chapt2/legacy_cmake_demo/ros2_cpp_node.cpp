#include <rclcpp/rclcpp.hpp>
#include <iostream>
using namespace std;
int main(int argc,char** argv)
{
    // : 为域名解析符
    rclcpp::init(argc,argv);//初始化
    //auto为自动类型推导,在此创建一个rclcpp下的node的共享指针
    auto node = std::make_shared <rclcpp::Node> ("cpp_node");
    //这是一个宏定义
    RCLCPP_INFO(node->get_logger(),"你好C++节点");
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}