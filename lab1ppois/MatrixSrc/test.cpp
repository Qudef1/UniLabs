#include "matrix.h"
#include <UnitTest++/UnitTest++.h>
#include <memory>

TEST(ConstructorTest1) {
    Matrix m(2, 3, 5.5);
    auto data = m.getData();
    CHECK_EQUAL(2, m.getRows());
    CHECK_EQUAL(3, m.getCols());
    CHECK_EQUAL(5.5, data[0][0]);
    CHECK_EQUAL(5.5, data[1][2]);
}
TEST(constructorTest2) {
    Matrix m;
    CHECK_EQUAL(0, m.getRows());
    CHECK_EQUAL(0, m.getCols());
}

TEST(constructorTest3) {
    Matrix m1;
    m1.loadFromFile("matrix.txt");
    Matrix m2(m1);
    auto data = m2.getData();
    CHECK_EQUAL(4, m2.getRows());
    CHECK_EQUAL(4, m2.getCols());
    CHECK_EQUAL(1.0, data[0][0]);
    CHECK_EQUAL(4.0, data[0][3]);
}

TEST(operatorAssignement){
    Matrix m1;
    m1.loadFromFile("matrix.txt");
    Matrix m2;
    m2 = m1;auto data = m2.getData();
    CHECK_EQUAL(4, m2.getRows());
    CHECK_EQUAL(4, m2.getCols());
    CHECK_EQUAL(1.0, data[0][0]);
    CHECK_EQUAL(4.0, data[0][3]);
}

TEST(operatorSum){
    Matrix m1;
    m1.loadFromFile("matrix.txt");
    Matrix m2 = m1;
    Matrix result = m1+m2;
    m1+=m2;
    auto data = m1.getData();
    auto resData = result.getData();
    auto m2Data = m2.getData();
    CHECK_EQUAL(m2Data[0][0]*2,resData[0][0]);
    CHECK_EQUAL(data[1][1],resData[1][1]);
    CHECK_EQUAL(data[2][2],resData[2][2]);
}

TEST(operatorMinus){
    Matrix m1;
    m1.loadFromFile("matrix.txt");
    Matrix m2 = m1;
    Matrix result = m1-m2;
    m1-=m2;
    auto data = m1.getData();
    auto resData = result.getData();
    auto m2Data = m2.getData();
    CHECK_EQUAL(0.,resData[0][0]);
    CHECK_EQUAL(data[1][1],resData[1][1]);
    CHECK_EQUAL(data[2][2],resData[2][2]);
}

TEST(NotEqualSizesThrow){
    Matrix m1(3,2);
    Matrix m2(4,4);
    CHECK_THROW(m1+m2,std::invalid_argument);
    CHECK_THROW(m1-m2,std::invalid_argument);
    CHECK_THROW(m1-=m2,std::invalid_argument);
    CHECK_THROW(m1+=m2,std::invalid_argument);
}

TEST(operatorMultiply){
    Matrix m1;
    m1.loadFromFile("matrix.txt");
    Matrix m2 = m1;
    Matrix result = m1*m2;
    m1*=m2;
    auto data = m1.getData();
    auto resData = result.getData();
    auto m2Data = m2.getData();
    CHECK_EQUAL(data[0][0],resData[0][0]);
    CHECK_EQUAL(data[1][1],resData[1][1]);
    CHECK_EQUAL(data[2][2],resData[2][2]);
    CHECK_EQUAL(170.,data[0][0]);
    CHECK_EQUAL(9012.,data[3][3]);
}

TEST(MultiplicationInvalidSizesThrows) {
    Matrix m1(2, 3);
    Matrix m2(4, 2);
    CHECK_THROW(m1 * m2, std::invalid_argument);
}

TEST(LoadFromFile) {
    Matrix m;
    m.loadFromFile("matrix.txt");
    auto data = m.getData();
    CHECK_EQUAL(4, m.getRows());
    CHECK_EQUAL(4, m.getCols());
    CHECK_EQUAL(1.0, data[0][0]);
    CHECK_EQUAL(2.0, data[0][1]);
}

TEST(LoadFromInvalidFileThrows) {
    Matrix m;
    CHECK_THROW(m.loadFromFile("n.txt"), std::runtime_error);
}

TEST(DetAndNormTest){
    Matrix m;
    m.loadFromFile("matrix.txt");
    double det = m.det();
    CHECK_EQUAL(-924.,det);
    std::vector<std::vector<double>> data = {{1,2},{3,4}};
    Matrix m2(data);
    CHECK_EQUAL(sqrt(30.),m2.norm());
}

TEST(DeterminantNonSquareThrows) {
    Matrix m(2, 3);
    CHECK_THROW(m.det(), std::invalid_argument);
}

TEST(checkZero){
    Matrix m;
    m.loadFromFile("zero.txt");
    CHECK_EQUAL(2,m.matrixType());
}

TEST(checkSquared){
    Matrix m;
    m.loadFromFile("squared.txt");
    CHECK_EQUAL(1,m.matrixType());
}

TEST(checkDiagonal){
    Matrix m;
    m.loadFromFile("diagonal.txt");
    CHECK_EQUAL(3,m.matrixType());
}

TEST(checkIntedent){
    Matrix m;
    m.loadFromFile("intedent.txt");
    CHECK_EQUAL(4,m.matrixType());
}

TEST(checkSymmentric){
    Matrix m(5,5,9.0);
    CHECK_EQUAL(5,m.matrixType());
}

TEST(checkUpperTriagonal){
    Matrix m;
    m.loadFromFile("upperTriagonal.txt");
    CHECK_EQUAL(7,m.matrixType());
}

TEST(checkLowerTriagonal){
    Matrix m;
    m.loadFromFile("lowerTriagonal.txt");
    CHECK_EQUAL(6,m.matrixType());
}

TEST(checkNoneType){
    Matrix m;
    m.loadFromFile("none.txt");
    CHECK_EQUAL(0,m.matrixType());
}

TEST(scalarSum){
    Matrix m;
    m.loadFromFile("matrix.txt");
    Matrix result = m+8.;
    m+=2.;
    auto data = m.getData();
    auto resData = result.getData();
    CHECK_EQUAL(3.,data[0][0]);
    CHECK_EQUAL(4.,data[0][1]);
    CHECK_EQUAL(5.,data[0][2]);
    CHECK_EQUAL(9.,resData[0][0]);
    CHECK_EQUAL(10.,resData[0][1]);
    CHECK_EQUAL(11.,resData[0][2]);
}
TEST(scalarMinus){
    Matrix m;
    m.loadFromFile("matrix.txt");
    Matrix result = m-1.;
    m-=2.;
    auto data = m.getData();
    auto resData = result.getData();
    CHECK_EQUAL(-1.,data[0][0]);
    CHECK_EQUAL(0.,data[0][1]);
    CHECK_EQUAL(1.,data[0][2]);
    CHECK_EQUAL(0.,resData[0][0]);
    CHECK_EQUAL(1.,resData[0][1]);
    CHECK_EQUAL(2.,resData[0][2]);
}
TEST(scalarMult){
    Matrix m;
    m.loadFromFile("matrix.txt");
    Matrix result = m*8.;
    m*=2.;
    auto data = m.getData();
    auto resData = result.getData();
    CHECK_EQUAL(2.,data[0][0]);
    CHECK_EQUAL(4.,data[0][1]);
    CHECK_EQUAL(6.,data[0][2]);
    CHECK_EQUAL(8.,resData[0][0]);
    CHECK_EQUAL(16.,resData[0][1]);
    CHECK_EQUAL(24.,resData[0][2]);
}
TEST(PreIncrement){
    Matrix m;
    m.loadFromFile("matrix.txt");
    ++m;
    auto data = m.getData();
    
    CHECK_EQUAL(2.,data[0][0]);
    CHECK_EQUAL(3.,data[0][1]);
    CHECK_EQUAL(4.,data[0][2]);
}
TEST(PostIncrement){
    Matrix m;
    m.loadFromFile("matrix.txt");
    Matrix result = m++;
    auto data = m.getData();
    auto resData = result.getData();
    CHECK_EQUAL(2.,data[0][0]);
    CHECK_EQUAL(3.,data[0][1]);
    CHECK_EQUAL(4.,data[0][2]);
    CHECK_EQUAL(1.,resData[0][0]);
    CHECK_EQUAL(2.,resData[0][1]);
    CHECK_EQUAL(3.,resData[0][2]);
}
TEST(PreDecrement){
    Matrix m;
    m.loadFromFile("matrix.txt");
    --m;
    auto data = m.getData();
    
    CHECK_EQUAL(0.,data[0][0]);
    CHECK_EQUAL(1.,data[0][1]);
    CHECK_EQUAL(2.,data[0][2]);
}
TEST(PostDecrement){
    Matrix m;
    m.loadFromFile("matrix.txt");
    Matrix result = m--;
    auto data = m.getData();
    auto resData = result.getData();
    CHECK_EQUAL(0.,data[0][0]);
    CHECK_EQUAL(1.,data[0][1]);
    CHECK_EQUAL(2.,data[0][2]);
    CHECK_EQUAL(1.,resData[0][0]);
    CHECK_EQUAL(2.,resData[0][1]);
    CHECK_EQUAL(3.,resData[0][2]);
}

TEST(Transpose){
    Matrix m(5,2);
    m.T();
    Matrix m2;
    CHECK_THROW(m2.T(),std::invalid_argument);
    CHECK_EQUAL(2,m.getRows());
    CHECK_EQUAL(5,m.getCols());
}
TEST(Reshape){
    Matrix m(4,4);
    m.reshape(16,1);
    CHECK_EQUAL(16,m.getRows());
    CHECK_EQUAL(1,m.getCols());
    CHECK_THROW(m.reshape(2,2),std::invalid_argument);
}
TEST(ReshapeError){
    Matrix m(4,4);
    CHECK_THROW(m.reshape(2,2),std::invalid_argument);
}
TEST(vectorError){
    std::vector<std::vector<double>> m;
    m.push_back(std::vector<double>({1,2,3}));
    m.push_back(std::vector<double>({1,2}));
    CHECK_THROW(Matrix M(m),std::invalid_argument);
}
TEST(SubmatrixTest){
    Matrix m;
    m.loadFromFile("matrix.txt");
    Matrix submatrix = m.submatrix(3,3);
    auto data = m.getData();
    auto submatrix_data = submatrix.getData();
    CHECK_EQUAL(submatrix_data[0][0],data[0][0]);
    CHECK(submatrix_data[1][1]==data[1][1]);
}
TEST(scalarDiv){
    Matrix m;
    m.loadFromFile("matrix.txt");
    Matrix result = m/2.;
    m/=2.;
    auto data = m.getData();
    auto resData = result.getData();
    CHECK_EQUAL(0.5,data[0][0]);
    CHECK_EQUAL(1.,data[0][1]);
    CHECK_EQUAL(1.5,data[0][2]);
    CHECK_EQUAL(0.5,resData[0][0]);
    CHECK_EQUAL(1.,resData[0][1]);
    CHECK_EQUAL(1.5,resData[0][2]);
}
TEST(scalarPow){
    Matrix m;
    m.loadFromFile("matrix.txt");
    Matrix result = m^2;
    m^=2;
    auto data = m.getData();
    auto resData = result.getData();
    CHECK_EQUAL(1.,data[0][0]);
    CHECK_EQUAL(4.,data[0][1]);
    CHECK_EQUAL(9.,data[0][2]);
    CHECK_EQUAL(1.,resData[0][0]);
    CHECK_EQUAL(4.,resData[0][1]);
    CHECK_EQUAL(9.,resData[0][2]);
}



int main() {
    return UnitTest::RunAllTests();
}

//g++ -std=c++17 -fprofile-arcs -ftest-coverage matrix.cpp test.cpp -I/usr/include -lUnitTest++ -o tests && ./tests && gcov tests-test.gcda


