#include "set.h"
#include <iostream>
#include <memory>

int main(){
    set s1(std::string("{{1,2},1,4,5,{{1},2,{3}}}"));
    std::cout<<s1.get_size();
    s1+=s1;
    set s2 = s1+s1;
    
    std::cout<<std::endl;
    std::cout<<s1.get_size()<<std::endl;
    std::cout<<s2.get_size()<<std::endl;
    
    return 0;
}