#include <iostream>
#include <thread> //多线程
#include <chrono> //跟时间相关的头文件
#include <functional> //函数包装器
#include <cpp-httplib/httplib.h> //下载相关
using namespace std;

class Download
{
private:
    /* data */
public:
    void download(const string& host,const string& path,
    const function<void(const string&,const string&) > &callback_word_count)
    {
        cout<<"线程"<<this_thread::get_id()<<endl;
        httplib::Client client(host);
        auto response = client.Get(path);
        if(response && response->status==200) //http规定响应码200表示成功响应
        {
            callback_word_count(path,response->body);
        }
        else
        {
            cout<<"下载失败"<<path<<"status="<<(response?to_string(response->status):string("连接失败/无响应"))<<endl;
        }
    };
    
    //启动下载函数
    //start_download主要用来创建线程
    void start_download(const string& host,const string& path,
    const function<void(const string&,const string&) > &callback_word_count)
    {
        auto download_fun = bind(&Download::download,this,placeholders::_1,placeholders::_2,placeholders::_3);
        thread t(download_fun,host,path,callback_word_count);
        //C++线程和Py线程不太一样，在创建好后会立马运行，但是会堵塞当前线程
        t.detach(); //从当前线程中分离出去
    };
};

int main()
{
    auto d = Download();
    auto word_count = [](const string& path,const string& result) -> void
    {
        cout<<"下载完成"<<path<<" "<<result.length()<< "->" << result.substr(0,9)<<endl;
    };
    
    //因为要区分 host 和 path 所以在这把域名拆分为两块
    d.start_download("http://0.0.0.0:8000","/novel1.txt",word_count);
    d.start_download("http://0.0.0.0:8000","/novel2.txt",word_count);
    d.start_download("http://0.0.0.0:8000","/novel3.txt",word_count);

    this_thread::sleep_for(chrono::milliseconds(1000*10)); //休眠10s


    return 0;
}

