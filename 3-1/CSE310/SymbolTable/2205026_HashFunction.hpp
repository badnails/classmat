#pragma once
#include<string>

class HashFunction{
protected:
    int size;
public:
    HashFunction(const int size):size(size){}
    virtual ~HashFunction(){}
    virtual unsigned int hash(std::string target) = 0;
};