#include "2205026_HashFunction.hpp"

class SDBM_HashFunction: public HashFunction{
public:
    SDBM_HashFunction(int hash_table_size):HashFunction(hash_table_size){}
    ~SDBM_HashFunction(){};
    unsigned int hash(std::string target) override {
        unsigned int hash  = 0;
        unsigned int len = target.length();

        for(unsigned int i = 0; i<len; i++){
            hash = ((target[i]) + (hash << 6) + (hash << 16) - hash) % size;
        }

        return hash;
    }
};
