#include "set.h"

set::set() : size(0) {}

set::set(std::initializer_list<int> lst) : size(0) {
    for(auto el : lst){
        add(el); // Используем add для проверки уникальности
    }
}


set::set(std::initializer_list<Element> init) : size(0) {
    for(const auto& el : init){
        if(std::holds_alternative<int>(el)){
            add(std::get<int>(el));
        } else {
            add(std::get<std::shared_ptr<set>>(el));
        }
    }
}

set::set(std::string x){
    Parser parser;
    auto parsed = parser.parse(x);
    this->elements = parsed->elements;
    this->size = parsed->size;
}

set::set(const char* x):set(std::string(x)){}

set& set::operator+=(const set& other){
    
    
    for(auto other_el : other.elements){
        if(std::holds_alternative<int>(other_el)){
            if(!contains(std::get<int>(other_el))){
                this->elements.emplace_back(other_el);
                this->size++;
            }
        }else{
            if(!contains(std::get<std::shared_ptr<set>>(other_el))){
                this->elements.emplace_back(other_el);
                this->size++;
            }
        }
    }
    return *this;
}
set set::operator+(const set& other)const{
    set result;
    result.elements = elements;
    result.size = size;
    for(auto other_el : other.elements){
        if(std::holds_alternative<int>(other_el)){
            if(!contains(std::get<int>(other_el))){
                result.elements.emplace_back(other_el);
                result.size++;
            }
        }else{
            if(!contains(std::get<std::shared_ptr<set>>(other_el))){
                result.elements.emplace_back(other_el);
                result.size++;
            }
        }
    }
    return result;
}
set set::operator*(const set& other)const{
    set result;
    
    for(auto other_el : other.elements){
        if(std::holds_alternative<int>(other_el)){
            if(contains(std::get<int>(other_el))){
                result.elements.emplace_back(other_el);
                result.size++;
            }
        }else{
            if(contains(std::get<std::shared_ptr<set>>(other_el))){
                result.elements.emplace_back(other_el);
                result.size++;
            }
        }
    }
    return result;
}
set& set::operator*=(const set& other){
    
    set result = *this;
    result.elements.clear();
    result.size = 0;
    for(auto other_el : other.elements){
        if(std::holds_alternative<int>(other_el)){
            if(contains(std::get<int>(other_el))){
                result.elements.emplace_back(other_el);
                result.size++;
            }
        }else{
            if(contains(std::get<std::shared_ptr<set>>(other_el))){
                result.elements.emplace_back(other_el);
                result.size++;
            }
        }
    }
    this->elements = result.elements;
    this->size = result.size;
    return *this;
}
set set::operator-(const set& other)const{
    set result;
    result.elements = elements;
    result.size = size;
    for(auto other_el : other.elements){
        if(std::holds_alternative<int>(other_el)){
            if(contains(std::get<int>(other_el))){
                result.remove(other_el);
                
            }
        }else{
            if(contains(std::get<std::shared_ptr<set>>(other_el))){
                result.remove(other_el);
                
            }
        }
    }
    return result;
}

set& set::operator=(const set& other){
    this->elements = other.elements;
    this->size = other.size;
    return *this;
}
set& set::operator-=(const set& other){
    
    
    for(auto other_el : other.elements){
        if(std::holds_alternative<int>(other_el)){
            if(contains(std::get<int>(other_el))){
                this->remove(other_el);
                
            }
        }else{
            if(contains(std::get<std::shared_ptr<set>>(other_el))){
                this->remove(other_el);
                
            }
        }
    }
    return *this;
}

bool set::operator==(const set& other) const {
    if (size != other.size) {
        return false;
    }
    
    for(auto& el : elements){
        bool found = false;
        for (const auto& other_el : other.elements){
            if (el.index() == other_el.index()) {
                if (std::holds_alternative<int>(el)) {
                    if (std::get<int>(el) == std::get<int>(other_el)) {
                        found = true;
                        break;
                    }
                } else {
                    auto nested1 = std::get<std::shared_ptr<set>>(el);
                    auto nested2 = std::get<std::shared_ptr<set>>(other_el);
                    if (*nested1 == *nested2) { // Рекурсивный вызов
                        found = true;
                        break;
                    }
                }
            }
        }
        if (!found) return false;
    }
    return true;
}
bool set::operator[](Element x){
    if(std::holds_alternative<int>(x)){
        int value = std::get<int>(x);
        return contains(value);
    }
    else if(std::holds_alternative<std::shared_ptr<set>>(x)){
        auto value = std::get<std::shared_ptr<set>>(x);
        return contains(value);
    }
    else{
        return false;
    }
}
bool set::contains_int(int x) const {
    for (const auto& el : elements){
        if(std::holds_alternative<int>(el)){
            if(std::get<int>(el) == x){
                return true;
            }
        }
    }
    return false;
}

bool set::contains(std::shared_ptr<set> x) const {
    for(const auto& el : elements){
        if(std::holds_alternative<std::shared_ptr<set>>(el)){
            auto my_set_ptr = std::get<std::shared_ptr<set>>(el);
            if(*my_set_ptr == *x){
                return true;
            }
        }
    }
    return false;
}

bool set::contains(int a) const {
    return contains_int(a);    
}

void set::add(int el){
    if(!contains(el)){
        elements.emplace_back(el);
        size++;
    }
}

void set::add(std::shared_ptr<set> el){
    if(!contains(el)){
        elements.emplace_back(el);
        size++;
    }
}

std::shared_ptr<set> set::make_nested_set(std::initializer_list<Element> init) {
    return std::make_shared<set>(init);
}

bool set::is_null() const {
    return size == 0;
}

int set::get_size() const {
    return size;
}

bool set::remove(const Element& el) {
    if (std::holds_alternative<int>(el)) {
        int value = std::get<int>(el);
        for (auto it = elements.begin(); it != elements.end(); ++it) {
            if (std::holds_alternative<int>(*it) && std::get<int>(*it) == value) {
                elements.erase(it);
                size--;
                return true;
            }
        }
    } else {
        auto removable = std::get<std::shared_ptr<set>>(el);
        for (auto it = elements.begin(); it != elements.end(); ++it) {
            if (std::holds_alternative<std::shared_ptr<set>>(*it)) {
                if (*std::get<std::shared_ptr<set>>(*it) == *removable) {
                    elements.erase(it);
                    size--;
                    return true;
                }
            }
        }
    }
    return false;
    
}

set set::boolean() {
    std::vector<set> result = {set{}};
    
    for (auto el : elements){
        int current_size = result.size();
        for (int i = 0;i<current_size;i++){
            set new_subset = result[i];

            if (std::holds_alternative<int>(el)) {
                new_subset.add(std::get<int>(el));
            } else {
                new_subset.add(std::get<std::shared_ptr<set>>(el));
            }
            
            
            result.push_back(new_subset);
        }
    }
    set final_res;
    for( auto el : result){
        final_res.add(std::make_shared<set>(el));
    }
    return final_res;
}

void set::Parser::ignore_w(){
    while (pos < input.size() && std::isspace(input[pos])) {
        pos++;
    }
}

bool set::operator!=(const set& other) const{
    if(!(*this==other)){
        return true;
    }
    else{
        return false;
    }
}

int set::Parser::parse_int(){
    int start = pos;
    if(input[pos]=='-'){
        pos++;
    }
    while (pos < input.size() && std::isdigit(input[pos])) {
        pos++;
    }
    return std::stoi(input.substr(start, pos - start));
}

std::istream& operator>>(std::istream& is,set& s){
    std::string input;
    std::getline(is,input);
    set::Parser parser;
    try{
        auto parsed_set = parser.parse(input);
        s.elements = parsed_set->elements;
        s.size = parsed_set->size;
    }
    catch(std::exception e){
        std::cout<<e.what()<<std::endl;
    }
    return is;
}

std::ostream&operator<<(std::ostream& os,set s){
    os<<"{";
    for(int i = 0;i<s.size;i++){
        if(std::holds_alternative<int>(s.elements[i])){
            os<<std::get<int>(s.elements[i]);
        }
        else{
            os<<*std::get<std::shared_ptr<set>>(s.elements[i]);
        }
        if(i<s.size-1){
            os<<", ";
        }
    }
    os<<"}";
    return os;
}

Element set::Parser::parse_element(){
    ignore_w();
    if (pos >= input.size()) {
        throw std::runtime_error("end reached");
    }
    if (input[pos] == '{') {
        return parse_set();
    }
    else if (std::isdigit(input[pos])||(input[pos]=='-'&&pos+1<input.size()&&std::isdigit(input[pos + 1]))) {
        return parse_int();
    }
    else {
        throw std::runtime_error("unexpected char");
    }
}

std::shared_ptr<set> set::Parser::parse_set(){
    if(input[pos]!='{'){
        throw std::runtime_error("expected {");
    }
    pos++;
    auto result = std::make_shared<set>();
    bool first_el = true;
    while(true){
        ignore_w();
        if(pos<input.size()&&input[pos]=='}'){
            pos++;
            break;
        }
        Element el = parse_element();
        if(std::holds_alternative<int>(el)){
            result->add(std::get<int>(el));
        }
        else{
            result->add(std::get<std::shared_ptr<set>>(el));
        }
        ignore_w();
        if(pos<input.size()&&input[pos]==','){
            pos++;
        }
        else if(pos>= input.size()|| input[pos]!='}'){
            throw std::runtime_error("no symbol } or ,");
        }
    }
    return result;
}

std::shared_ptr<set> set::Parser::parse(std::string str) {
    input = str;
    pos = 0;
    ignore_w();
    if (pos >= input.size()) {
        throw std::runtime_error("Empty input");
    }
    if (input[pos] != '{') {
        throw std::runtime_error("Input must start with '{'");
    }
    auto result = parse_set();
    ignore_w();
    if (pos != input.size()) {
        throw std::runtime_error("Unexpected characters at the end");
    }
    return result;
}
