#pragma once
#include "2205026_ScopeTable.hpp"

class SymbolTable{
private:
    int table_counter = 1;
    int hash_table_size;
    HashFunction* hasher = nullptr;
    ScopeTable* current_scope = nullptr;
public:
    SymbolTable(int size, HashFunction* hasher):hash_table_size(size), hasher(hasher){
        enter_scope();
    }
    
    ~SymbolTable(){
        while(current_scope) exit_scope();
    }
    
    SymbolTable(const SymbolTable&) = delete;
    SymbolTable& operator=(const SymbolTable&) = delete;

    void enter_scope();
    void exit_scope();
    bool insert_symbol(const std::string symbol_name, const std::string symbol_type);
    bool remove_symbol(const std::string symbol_name);
    SymbolInfo* lookup_symbol(const std::string symbol_name);
    void print_current_scope();
    void print_all_scopes();
    bool on_root_scope();
};