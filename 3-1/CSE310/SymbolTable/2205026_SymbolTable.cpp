#include<iostream>
#include "2205026_SymbolTable.hpp"

void SymbolTable::enter_scope(){
    ScopeTable* newtable = new ScopeTable(table_counter, hash_table_size, hasher, current_scope);
    current_scope = newtable;
    std::cout<<"\tScopeTable# "<<table_counter++<<" created"<<std::endl;
}
void SymbolTable::exit_scope(){
    ScopeTable* parent = current_scope->get_parent();
    int deleted_index = current_scope->get_table_index();
    delete current_scope;
    current_scope = parent;

    std::cout<<"\t"<<"ScopeTable# "<<deleted_index<<" removed"<<std::endl;
}
bool SymbolTable::insert_symbol(const std::string symbol_name, const std::string symbol_type){
    return current_scope->insert_symbol(symbol_name, symbol_type);
}
bool SymbolTable::remove_symbol(const std::string symbol_name){
    return current_scope->delete_symbol(symbol_name);
}
SymbolInfo* SymbolTable::lookup_symbol(const std::string symbol_name){
    ScopeTable* current = current_scope;
    SymbolInfo* ret = nullptr;
    
    while(current){
        ret = current->lookup_symbol(symbol_name);
        
        if(ret!=nullptr) return ret;
        current = current->get_parent();
    }

    std::cout<<"\t'"<<symbol_name<<"'"<<" not found in any of the ScopeTables"<<std::endl;
    return nullptr;
}
void SymbolTable::print_current_scope(){
    current_scope->print_table(1);
}
void SymbolTable::print_all_scopes(){
    ScopeTable* curr = current_scope;
    int space_multiplier = 1;
    while(curr){
        curr->print_table(space_multiplier);
        curr = curr->get_parent();
        space_multiplier++;
    }
}

bool SymbolTable::on_root_scope(){
    if(current_scope->get_parent() == nullptr) return true;
    return false;
}
