#include "2205026_SymbolTable.hpp"
#include "2205026_SDBM.cpp"

#include<iostream>
#include<fstream>
#include<limits>
#include<unordered_set>
#include<string>
#include<sstream>
#include<vector>
using namespace std;

int cmd_counter = 1;

void mismatch(const string code){
    cout<<"\tNumber of parameters mismatch for the command "<<code<<endl;
}

void print_HEADER(string command){
    cout<<"Cmd "<<cmd_counter++<<": ";
    cout<<command<<endl;
}


bool INSERT_FUNCTION_handler(string& type, int argnum, vector<string>& args){
    if(argnum<4){
        mismatch("I");
        return false;
    }

    type.append(",");
    
    string return_type = args[2];

    type.append(return_type + "<==" + "(");
    
    for(int i = 3; i<argnum; i++){
        if(i>3) type.append(",");
        type.append(args[i]);
    }

    type.append(")");
    return true;
}

bool INSERT_SU_handler(string& type, int argnum, vector<string>& args){
    if(argnum%2){
        mismatch("I");
        return false;
    }

    int i = 2;
    int j = 3;

    type.append(",{");

    for(; i<argnum-1 && j<argnum; i+=2, j+=2){ 
        if(i>2) type.append(",");

        type.append("("+args[i]+","+args[j]+")");
    }
    type.append("}");
    return true;
}

int main(int argc, char* argv[])
{
    if(argc!=3){
        cout<<"malformed args"<<endl;
    }

    ifstream in(argv[1]);;
    ofstream out(argv[2]);

    cout.rdbuf(out.rdbuf());
    cin.rdbuf(in.rdbuf());

    int hash_table_size;
    cin>>hash_table_size;
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    string command;

    unordered_set<string> valid_codes = {"I", "L", "D", "P", "S", "E", "Q"};

    SDBM_HashFunction hasher(hash_table_size);

    SymbolTable symbol_table(hash_table_size, &hasher);

    while(true){
        getline(cin, command);
        
        if(command.empty()){
            return 0;
        }

        stringstream ss(command);

        string code;
        string arg;
        vector<string> args;

        ss>>code;

        if(valid_codes.find(code) == valid_codes.end()) continue;

        while(ss>>arg){
            args.push_back(arg);
        }

        int argnum = args.size();

        if(code == "I"){
            print_HEADER(command);
            if(argnum<2){
                mismatch("I");
                continue;
            }

            string key = args[0];
            string type = args[1];

            if(type == "FUNCTION"){
                bool res = INSERT_FUNCTION_handler(type, argnum, args);
                if(!res) continue;
            }
            else if(type == "STRUCT" || type == "UNION"){
                bool res = INSERT_SU_handler(type, argnum, args);
                if(!res) continue;
            }
            else{
                if(argnum!=2){
                    mismatch("I");
                    continue;
                }
            }
            symbol_table.insert_symbol(key, type);

        }
        else if(code == "L"){
            print_HEADER(command);
            if(argnum!=1){
                mismatch("L");
                continue;
            }

            symbol_table.lookup_symbol(args[0]);
        }
        else if(code == "D"){
            print_HEADER(command);
            if(argnum!=1){
                mismatch("D");
                continue;
            }

            symbol_table.remove_symbol(args[0]);
        }
        else if(code == "P"){
            if(argnum!=1){
                print_HEADER(command);
                mismatch("P");
                continue;
            }
            
            if(args[0]!="A" && args[0]!="C") continue;

            print_HEADER(command);

            if(args[0] == "A"){
                symbol_table.print_all_scopes();
            }
            else if(args[0] == "C"){
                symbol_table.print_current_scope();
            }
        }
        else if(code == "S"){
            print_HEADER(command);
            if(argnum!=0){
                mismatch("S");
                continue;
            }
            symbol_table.enter_scope();
        }
        else if(code == "E"){
            if(argnum!=0){
                print_HEADER(command);
                mismatch("E");
                continue;
            }
            
            if(symbol_table.on_root_scope()) continue;
            
            print_HEADER(command);
            symbol_table.exit_scope();
        }
        else if(code == "Q"){
            print_HEADER(command);
            if(argnum!=0){
                mismatch("Q");
                continue;
            }
            return 0;
        }
    }
}