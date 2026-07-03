#pragma once
#include "2205026_SymbolInfo.hpp"
#include "2205026_HashFunction.hpp"

struct Find_Schema{
    SymbolInfo** address;
    unsigned int bucket;
    int chain_idx;
};

class ScopeTable{
private:
    int table_index;
    int size;
    SymbolInfo** table = nullptr;
    ScopeTable* parent_scope = nullptr;
    HashFunction* hasher = nullptr;

    Find_Schema find_slot(const std::string& symbol_name);
public:
    ScopeTable(int index, int size, HashFunction* hasher, ScopeTable* parent_scope = nullptr)
        :table_index(index), size(size), hasher(hasher), parent_scope(parent_scope){
        
        table = new SymbolInfo*[size]();
    }

    ~ScopeTable(){
        
        for(int i = 0; i<size; i++){
            SymbolInfo* it = table[i];
            while(it){
                SymbolInfo* next = it->get_next();
                delete it;
                it = next;
            }
        }

        delete[] table;
    }

    ScopeTable(const ScopeTable& other) = delete;
    ScopeTable& operator=(const ScopeTable& other) = delete;

    int get_table_index();
    ScopeTable* get_parent();

    bool insert_symbol(const std::string& symbol_name, const std::string& symbol_type);
    SymbolInfo* lookup_symbol(const std::string& symbol_name);
    bool delete_symbol(const std::string& symbol_name);
    void print_table(int leading_spaces) const;
};