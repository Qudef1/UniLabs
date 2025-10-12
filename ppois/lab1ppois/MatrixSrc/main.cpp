#include "matrix.h"

int main(){
    std::cout << "Creating m1..." << std::endl;
        Matrix m1(3, 3, 5.0);
        std::cout << "Matrix m1 created:\n" << m1 << std::endl;
        
        std::cout << "Creating m2..." << std::endl;
        Matrix m2(3,3,2.0);
        
        std::cout << "Loading m3 from file..." << std::endl;
        Matrix m3;
        m3.loadFromFile("matrix.txt");
        std::cout << "Loaded from file:\n" << m3 << std::endl;
        
        std::cout << "Loading m4 from file..." << std::endl;
        Matrix m4;
        m4.loadFromFile("matrix2.txt");
        std::cout << "m4 loaded:\n" << m4 << std::endl;
        
        std::cout << "Transposing m1..." << std::endl;
        m1.T();
        std::cout << "Transposed m1:\n" << m1 << std::endl;
        
        std::cout << "Incrementing m1..." << std::endl;
        ++m1;
        std::cout << "After ++m1:\n" << m1 << std::endl;
        
        std::cout << "Adding m3 + m4..." << std::endl;
        Matrix sub = m3 + m4;
        std::cout << "Submatrix:\n" << sub << std::endl;
        
        std::cout << "Saving to file..." << std::endl;
        sub.saveToFile("output.txt");
        
        std::cout << "Checking matrix type..." << std::endl;
        int type = m1.matrixType();
        std::cout << "Matrix type: " << type << std::endl;
        std::cout<<"det "<<m4.det()<<std::endl;
        std::cout<<"norm "<<m4.norm()<<std::endl;
}