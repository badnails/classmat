#include<iostream>
#include "2205026_ScopeTable.hpp"

int ScopeTable::get_table_index(){
    return table_index;
}

ScopeTable* ScopeTable::get_parent(){
    return parent_scope;
}

bool ScopeTable::insert_symbol(const std::string& symbol_name, const std::string& symbol_type){
    Find_Schema slot_info = find_slot(symbol_name);

    
    if(*(slot_info.address)){
        std::cout<<"\t'"<<symbol_name<<"' already exists in the current ScopeTable"<<std::endl;
        return false;
    }

    *(slot_info.address) = new SymbolInfo(symbol_name, symbol_type);
    std::cout<<"\tInserted in ScopeTable# "<<table_index<<" at position "<<slot_info.bucket<<", "<<slot_info.chain_idx<<std::endl;
    
    return true;
}


SymbolInfo* ScopeTable::lookup_symbol(const std::string& symbol_name){
    
    Find_Schema slot_info = find_slot(symbol_name);
    
    if(*(slot_info.address)!=nullptr){
        std::cout<<"\t'"<<symbol_name<<"'"<<" found in ScopeTable# "<<table_index<<" at position "<<slot_info.bucket<<", "<<slot_info.chain_idx<<std::endl;
    }

    return *(slot_info.address);
}

//returns address of slot
Find_Schema ScopeTable::find_slot(const std::string& symbol_name){
    unsigned int bucket = hasher->hash(symbol_name);
    
    SymbolInfo** it = &table[bucket];
    int chain_idx = 1;

    while((*it))
    {
        if((*it)->get_name() == symbol_name) return {it, bucket+1, chain_idx};
        
        it = &((*it)->get_next());
        chain_idx++;
    }

    return {it, bucket+1, chain_idx};
}

bool ScopeTable::delete_symbol(const std::string& symbol_name){
    Find_Schema slot_info = find_slot(symbol_name);

    if((*(slot_info.address)) == nullptr){
        std::cout<<"\tNot found in the current ScopeTable"<<std::endl;
        return false;
    }

    SymbolInfo* to_delete = *(slot_info.address);

    *(slot_info.address) = (*(slot_info.address))->get_next();

    delete to_delete;

    std::cout<<"\tDeleted '"<<symbol_name<<"' from ScopeTable# "<<table_index<<" at position "<<slot_info.bucket<<", "<<slot_info.chain_idx<<std::endl;

    return true;
}

void ScopeTable::print_table(int leading_spaces = 0) const{
    for(int i = 0; i<leading_spaces; i++) std::cout<<"\t";
    std::cout<<"ScopeTable# "<<table_index<<std::endl;

    for(int i = 0; i<size; i++){
        for(int i = 0; i<leading_spaces; i++) std::cout<<"\t";
        
        std::cout<<(i+1)<<"-->";

        const SymbolInfo* curr = table[i];
        while(curr){
            std::cout<<" ";
            std::cout<< *curr;
            curr = curr->get_next();
        }

        std::cout<<std::endl;
    }
}
