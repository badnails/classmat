#include<iostream>
#include "2205026_SymbolInfo.hpp"

SymbolInfo::SymbolInfo(const std::string& key, const std::string& value):name(key), type(value){}

std::ostream& operator<<(std::ostream& os, const SymbolInfo& to_print){
    os<<"<";
    os<<to_print.name;
    os<<",";
    os<<to_print.type;
    os<<">";

    return os;
}

std::string SymbolInfo::get_name() const {
    return name;
}

std::string SymbolInfo::get_type() const {
    return type;
}

SymbolInfo*& SymbolInfo::get_next(){
    return next;
}

const SymbolInfo* SymbolInfo::get_next() const{
    return next;
}

void SymbolInfo::set_name(const std::string& name){
    this->name = name;
}

void SymbolInfo::set_type(const std::string& type){
    this->type = type;
}

void SymbolInfo::chain(SymbolInfo* tail){
    SymbolInfo* temp = this;
    
    while(temp->next){
        temp = temp->next;
    }

    temp->next = tail;
}