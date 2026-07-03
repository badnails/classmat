#pragma once
#include <ostream>
#include<string>

class SymbolInfo{
private:
    std::string name;
    std::string type;
    SymbolInfo* next = nullptr;

public:
    SymbolInfo(){}
    SymbolInfo(const std::string& key, const std::string& value);
    friend std::ostream& operator<<(std::ostream& os, const SymbolInfo& to_print);
    std::string get_name() const;
    std::string get_type() const;
    SymbolInfo*& get_next();
    const SymbolInfo* get_next() const;
    void set_name(const std::string& name);
    void set_type(const std::string& type);
    void chain(SymbolInfo* tail);
};