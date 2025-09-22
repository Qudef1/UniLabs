#include "matrix.h"
#include <iomanip>

Matrix::Matrix() : rows(0), cols(0) {}

Matrix::Matrix(int rows, int cols) 
    : rows(rows), cols(cols), data(rows, std::vector<double>(cols, 0.0)) {}

Matrix::Matrix(int rows, int cols, double value)
    : rows(rows), cols(cols), data(rows, std::vector<double>(cols, value)) {}

Matrix::Matrix(const std::vector<std::vector<double>>& input_data) {
    if (input_data.empty()) {
        rows = 0;
        cols = 0;
        data = input_data;
        return;
    }
    
    rows = input_data.size();
    cols = input_data[0].size();
    
    
    for (size_t i = 1; i < rows; ++i) {
        if (input_data[i].size() != cols) {
            throw std::invalid_argument("All rows must have the same length");
        }
    }
    data = input_data;
}

Matrix::Matrix(const Matrix& other) : rows(other.rows), cols(other.cols), data(other.data) {}

Matrix& Matrix::operator++() {
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            ++data[i][j];
        }
    }
    return *this;
}

Matrix& Matrix::operator--() {
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            --data[i][j];
        }
    }
    return *this;
}

Matrix Matrix::operator++(int) {
    Matrix temp = *this;
    ++(*this);
    return temp;
}

Matrix Matrix::operator--(int) {
    Matrix temp = *this;
    --(*this);
    return temp;
}

Matrix& Matrix::reshape(size_t new_rows,size_t new_cols){
    if(rows==0||cols==0){
        throw std::invalid_argument("matrix is empty");
    }
    if(new_rows*new_cols!= rows*cols){
        throw std::invalid_argument("reshape invalid");
    }
    std::vector<double> temp;
    temp.reserve(rows*cols); 
    for(int i = 0;i<rows;i++){
        for(int j=0;j<cols;j++){
            temp.emplace_back(data[i][j]);
        }
    }
    
    rows = new_rows;
    cols = new_cols;
    data.clear();
    data.resize(rows);

    int index = 0;
    for(int i = 0;i<rows;i++){
        data[i].resize(cols);
        for(int j = 0;j<cols;j++){
            data[i][j] = temp[index++];
        }
    }
    return *this;
    
}

Matrix Matrix::submatrix(size_t temp_rows,size_t temp_cols){
    if(temp_rows > rows|| temp_rows*temp_cols == 0||temp_cols>cols){
        throw std::invalid_argument("submatrix must be smaller or equal to parental one");
    }

    Matrix result(temp_rows,temp_cols);
    
    for(int i=0;i<temp_rows;i++){
        for(int j=0;j<temp_cols;j++){
            result.data[i][j]=data[i][j];
        }
    }
    return result;
}

bool Matrix::isSquared(){
    if(rows == cols && rows!=0 && cols!=0){
        return true;
    }else{
        return false;
    }
}
bool Matrix::isDiagonal(){
    if(this->isSquared()){
        for(int i = 0;i<rows;i++){
            for(int j = 0;j<cols;j++){
                if(data[i][j]!=0 && i!=j){
                    return false;
                }
                if(data[i][j]==0 &&i==j){
                    return false;
                }
            }
        }
        return true;
    }else{
        return false;
    }
}
bool Matrix::isZero(){
    if(rows==0||cols==0){
        return false;
    }
    for(int i = 0;i<rows;i++){
        for(int j = 0;j<cols;j++){
            if(data[i][j]!=0.){
                return false;
            }
        }
    }
    return true;
}
bool Matrix::isIdentity(){
    if(this->isSquared()&&this->isDiagonal()){
        for(int i = 0;i<rows;i++){
            for(int j = 0;j<cols;j++){
                if(data[i][j]!=1. && i==j){
                    return false;
                }
                
            }
        }
        return true;
    }else{
        return false;
    }
}
bool Matrix::isSymmetric(){
    if(this->isSquared()&&!this->isDiagonal()){
        for(int i = 0;i<rows;i++){
            for(int j = i;j<cols;j++){
                if(data[i][j] != data[j][i]){
                    return false;
                }
            }
        }
        return true;
    }else{
        return false;
    }
}
bool Matrix::isUpperTriagonal(){
    if(this->isSquared()&&!this->isDiagonal()){
        for(int i = 0;i<rows;i++){
            for(int j = 0;j<i;j++){
                if(data[i][j] != 0){
                    return false;
                }
            }
        }
        return true;
    }else{
        return false;
    }
}
bool Matrix::isLowerTriagonal(){
    if(this->isSquared()&&!this->isDiagonal()){
        
        for(int i = 0;i<rows;i++){
            for(int j = i+1;j<cols;j++){
                if(data[i][j] != 0){
                    return false;
                }
            }
        }
        return true;
    }else{
        return false;
    }
}
int Matrix::matrixType(){
    // 0 - none,1-squared,2-zero,3-diagonal,4-identity,5-symmetric,6-upperTriagonal,7-lowerTriagonal
    if(this->isZero()){
        return 2;
    }
    else if(this->isLowerTriagonal()){
        return 6;
    }
    else if(this->isUpperTriagonal()){
        return 7;
    }
    else if(this->isIdentity()){
        return 4;
    }
    else if(this->isDiagonal()){
        return 3;
    }
    else if(this->isSymmetric()){
        return 5;
    }
    else if(this->isSquared()){
        return 1;
    }
    else{
        return 0;
    }
}

Matrix& Matrix::T(){
    if(rows == 0&&cols == 0){
        throw std::invalid_argument("matrix is empty");
    }
     std::vector<std::vector<double>> temp(cols, std::vector<double>(rows));
    
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            temp[j][i] = data[i][j];
        }
    }
    
    std::swap(rows, cols);
    data = temp;
    return *this;
}

std::ostream& operator<<(std::ostream& os, const Matrix& matrix) {
    os << std::fixed << std::setprecision(4);
    for (size_t i = 0; i < matrix.rows; ++i) {
        os << "[ ";
        for (size_t j = 0; j < matrix.cols; ++j) {
            os << std::setw(8) << matrix.data[i][j] << " ";
        }
        os << "]" << std::endl;
    }
    return os;
}

// Загрузка из файла
void Matrix::loadFromFile(const std::string& filename) {
    std::ifstream file(filename);
    if (!file.is_open()) {
        throw std::runtime_error("Cannot open file: " + filename);
    }
    
    std::vector<std::vector<double>> new_data;
    std::string line;
    
    while (std::getline(file, line)) {
        if (line.empty()) continue;
        
        std::vector<double> row;
        std::istringstream iss(line);
        double value;
        
        while (iss >> value) {
            row.push_back(value);
        }
        
        if (!row.empty()) {
            new_data.push_back(row);
        }
    }
    
    if (new_data.empty()) {
        throw std::runtime_error("File is empty or contains no valid data");
    }
    
    // Проверка одинаковой длины строк
    size_t first_row_size = new_data[0].size();
    for (size_t i = 1; i < new_data.size(); ++i) {
        if (new_data[i].size() != first_row_size) {
            throw std::runtime_error("All rows in file must have the same number of elements");
        }
    }
    
    // Устанавливаем новые данные
    rows = new_data.size();
    cols = first_row_size;
    data = new_data;
}

// Сохранение в файл
void Matrix::saveToFile(const std::string& filename) const {
    std::ofstream file(filename);
    if (!file.is_open()) {
        throw std::runtime_error("Cannot create file: " + filename);
    }
    
    file << std::fixed << std::setprecision(6);
    for (size_t i = 0; i < rows; ++i) {
        for (size_t j = 0; j < cols; ++j) {
            file << data[i][j];
            if (j < cols - 1) file << " ";
        }
        if (i < rows - 1) file << std::endl;
    }
}
std::vector<std::vector<double>> Matrix::getData(){
    return data;
}
int Matrix::getCols(){
    return cols;
}
int Matrix::getRows(){
    return rows;
}

Matrix& Matrix::operator=(const Matrix& x){
    if(this!=&x){
        rows = x.rows;
        cols = x.cols;
        data = x.data;
    }
    return *this;
}

Matrix Matrix::operator+(double x){
    Matrix result = *this;
    result.data.reserve(rows);
    for(int i = 0; i<rows;i++){
        result.data[i].reserve(cols);
        for( int j = 0;j<cols;j++){
            result.data[i][j]+=x;
        }
    }
    return result;
}

Matrix Matrix::operator-(double x){
    Matrix result = *this;
    result.data.reserve(rows);
    for(int i = 0; i<rows;i++){
        result.data[i].reserve(cols);
        for( int j = 0;j<cols;j++){
            result.data[i][j]-=x;
        }
    }
    return result;
}

Matrix Matrix::operator*(double x){
    Matrix result = *this;
    result.data.reserve(rows);
    for(int i = 0; i<rows;i++){
        result.data[i].reserve(cols);
        for( int j = 0;j<cols;j++){
            result.data[i][j]*=x;
        }
    }
    return result;
}

Matrix Matrix::operator/(double x){
    Matrix result = *this;
    result.data.reserve(rows);
    for(int i = 0; i<rows;i++){
        result.data[i].reserve(cols);
        for( int j = 0;j<cols;j++){
            result.data[i][j]/=x;
        }
    }
    return result;
}

Matrix Matrix::operator^(double x){
    Matrix result = *this;
    result.data.reserve(rows);
    for(int i = 0; i<rows;i++){
        result.data[i].reserve(cols);
        for( int j = 0;j<cols;j++){
            result.data[i][j] = pow(result.data[i][j],x);
        }
    }
    return result;
}

Matrix& Matrix::operator+=(double x){
    for(int i = 0;i<rows;i++){
        for(int j = 0;j<cols;j++){
            data[i][j]+=x;
        }
    }
    return *this;
}

Matrix& Matrix::operator-=(double x){
    for(int i = 0;i<rows;i++){
        for(int j = 0;j<cols;j++){
            data[i][j]-=x;
        }
    }
    return *this;
}

Matrix& Matrix::operator*=(double x){
    for(int i = 0;i<rows;i++){
        for(int j = 0;j<cols;j++){
            data[i][j]*=x;
        }
    }
    return *this;
}

Matrix& Matrix::operator/=(double x){
    for(int i = 0;i<rows;i++){
        for(int j = 0;j<cols;j++){
            data[i][j]/=x;
        }
    }
    return *this;
}

Matrix& Matrix::operator^=(double x){
    for(int i = 0;i<rows;i++){
        for(int j = 0;j<cols;j++){
            data[i][j]=pow(data[i][j],x);
        }
    }
    return *this;
}

Matrix Matrix::operator+(Matrix x){
    if (this->rows!=x.rows||this->cols!=x.cols||this->cols==0||this->rows==0||x.rows==0||x.cols==0)
    {
        throw std::invalid_argument("Matrix must be the same size");
    }
     Matrix result(rows, cols);
    
    for (size_t i = 0; i < rows; i++) {
        for (size_t j = 0; j < cols; j++) {
            result.data[i][j] = data[i][j] + x.data[i][j];
        }
    }
    return result;
}
Matrix Matrix::operator-(Matrix x){
    if (this->rows!=x.rows||this->cols!=x.cols||this->cols==0||this->rows==0||x.rows==0||x.cols==0)
    {
        throw std::invalid_argument("Matrix must be the same size");
    }
     Matrix result(rows, cols);
    
    for (size_t i = 0; i < rows; i++) {
        for (size_t j = 0; j < cols; j++) {
            result.data[i][j] = data[i][j] - x.data[i][j];
        }
    }
    return result;
}

Matrix& Matrix::operator+=(Matrix x){
    if (this->rows!=x.rows||this->cols!=x.cols||this->cols==0||this->rows==0||x.rows==0||x.cols==0)
    {
        throw std::invalid_argument("Matrix must be the same size");
    }
    
    for (size_t i = 0; i < rows; i++) {
        for (size_t j = 0; j < cols; j++) {
            data[i][j] += x.data[i][j];
        }
    }
    return *this;
}

Matrix& Matrix::operator-=(Matrix x){
    if (this->rows!=x.rows||this->cols!=x.cols||this->cols==0||this->rows==0||x.rows==0||x.cols==0)
    {
        throw std::invalid_argument("Matrix must be the same size");
    }
    
    for (size_t i = 0; i < rows; i++) {
        for (size_t j = 0; j < cols; j++) {
            data[i][j] -= x.data[i][j];
        }
    }
    return *this;
}


Matrix Matrix::operator*(Matrix x){
    if(this->cols!=x.rows||this->cols==0||this->rows==0||x.rows==0||x.cols==0){
        throw std::invalid_argument("rows must fit cols");
    }
    Matrix result(rows,x.cols);
    for(int i = 0;i<rows;i++){
        
        for(int j = 0;j<x.cols;j++){
            result.data[i][j] = 0;
            for(int k = 0;k<cols;k++){
                result.data[i][j] += data[i][k]*x.data[k][j];
            }
        }
    }
    return result;
}

Matrix& Matrix::operator*=(Matrix x){
    if(this->cols!=x.rows||this->cols==0||this->rows==0||x.rows==0||x.cols==0){
        throw std::invalid_argument("rows must fit cols");
    }
    Matrix result(rows,x.cols);
    for(int i = 0;i<rows;i++){
        
        for(int j = 0;j<x.cols;j++){
            result.data[i][j] = 0;
            for(int k = 0;k<cols;k++){
                result.data[i][j] += data[i][k]*x.data[k][j];
            }
        }
    }
    this->data = result.data;
    this->cols = result.cols;
    this->rows = result.rows;
    return *this;
}

double Matrix::det(){
    if(!isSquared()){
        throw std::invalid_argument("not squared matrix");
    }
    if(rows==0){
        return 1.0;
    }
    if(rows==1){
        return data[0][0];
    }
    if(rows==2){
        return data[0][0]*data[1][1]-data[1][0]*data[0][1];
    }
    double det = 0.0;
    int sign = 1;
    for(int i = 0;i<rows;i++){
        Matrix minor = getMinor(i,0);
        det+=sign*minor.det()*data[i][0];
        sign = -sign;
    }
    return det;
}

Matrix Matrix::getMinor(int rowToRemove,int colToRemove){
    Matrix minor(rows-1,cols-1);
    int minor_i=0;
    for(int i = 0;i<rows;i++){
        if(i==rowToRemove) continue;

        int minor_j = 0;
        for(int j = 0;j<cols;j++){
            if(j==colToRemove) continue;
            minor.data[minor_i][minor_j] = data[i][j];
            minor_j++;
        }
        minor_i++;
        

    }
    return minor;
}

double Matrix::norm(){
    if(rows==0||cols==0){
        return 0.0;
    }
    double result=0;
    for(int i = 0;i<rows;i++){
        for(int j = 0;j<cols;j++){
            result+=data[i][j]*data[i][j];
        }
    }
    result = sqrt(result);
    return result;
}






