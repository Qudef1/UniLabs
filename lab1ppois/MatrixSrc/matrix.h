/**
 * @file matrix.h
 * @brief класс вещественной матрицы с возможностью пересечения объединения рахности и других операций
 * @author qudef
 */
#pragma once
#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <algorithm>
#include <cmath>
/**
 * @class Matrix
 * @brief реализует класс вещественной матрицы
 * содержит в себе методы и поля нужные для реализации матрицы.
 */
class Matrix{
    private:
    int rows;///< количество рядов
    int cols;///< количество столбцов
    std::vector<std::vector<double>> data;///< данные матрицы
    /**
     * @brief метод для проверки квадратная ли матрица
     * @return true - да, false - нет
     */
    bool isSquared();
    /**
     * @brief метод для проверки диагональная ли матрица
     * @return true - да, false - нет
     */
    bool isDiagonal();
    /**
     * @brief метод для проверки нулевая ли матрица
     * @return true - да, false - нет
     */
    bool isZero();
    /**
     * @brief метод для проверки единичная ли матрица
     * @return true - да, false - нет
     */
    bool isIdentity();
    /**
     * @brief метод для проверки симметричная ли матрица
     * @return true - да, false - нет
     */
    bool isSymmetric();
    /**
     * @brief метод для проверки верхне-треугольная ли матрица
     * @return true - да, false - нет
     */
    bool isUpperTriagonal();
    /**
     * @brief метод для проверки нижне-треугольная ли матрица
     * @return true - да, false - нет
     */
    bool isLowerTriagonal();
    /**
     * @brief метод для нахождения минора матрицы, используется для нахождения детерминанта матрицы.
     * @return минор размером(rows-1,cols-1)
     * 
     */
    Matrix getMinor(int,int);
    public:
    /**
     * @brief обычные конструктор без параметров
     */
    Matrix();
    /**
     * @brief создает матрицу размером (rows,cols) и заполняет ее нулями
     * @param rows - число рядов
     * @param cols - число столбцов
     */
    Matrix(int rows, int cols);
    /**
     * @brief создает матрицу размером (rows,cols) и заполняет ее value
     * @param rows - число рядов
     * @param cols - число столбцов
     * @param value - значение для заполнения
     */
    Matrix(int rows, int cols, double value);
    /**
     * @brief создает матрицу на основе двумерного вектора
     * @param data - двумерный вектор, считывается количество строк и столбцов и заполняется матрица.
     */
    Matrix(const std::vector<std::vector<double>>& data);
    /**
     * @brief конструктор копирования
     * @param other - откуда копируется значение для матрицы
     */
    Matrix(const Matrix& other);
    
    /**
     * @brief пре-декремент оператор, сначала уменьшает на 1, потом делает операцию
     */
    Matrix& operator--();
    /**
     * @brief пре-инкремент оператор, сначала увеличивает на 1, потом делает операцию
     */
    Matrix& operator++();//pre
    /**
     * @brief пост-инкремент оператор, сначала делает операцию, потом увеличивает значение на 1
     */
    Matrix operator++(int);
    /**
     * @brief пост-декремент оператор, сначала делает операцию, потом уменьшает значение на 1
     */
    Matrix operator--(int); //post
    /**
     * @brief меняет размер матрицы в пределах ее прежних размеров
     * @param rows - новые ряды матрицы
     * @param cols - новые столбцы матрицы
     * @return прежнюю матрицу с новыми размерами
     * Если новые габариты матрицы не совпадают с прежними, бросается исключение
     */
    Matrix& reshape(size_t,size_t);
    /**
     * @brief возвращает подматрицу заданного размера
     * @param rows - ряды подматрицы
     * @param cols - столбцы подматрицы
     * @return подматрицу заданного размера
     * Если новые габариты матрицы не совпадают с прежними, бросается исключение
     */
    Matrix submatrix(size_t,size_t);
    /**
     * @brief определение типа матрицы
     * @see isSquared(),isDiagonal(),isZero(),isSymmetric(),isUpperTriagonal(),isLowerTriagonal(),isIdentity()
     * @return 0 - none,1-squared,2-zero,3-diagonal,4-identity,5-symmetric,6-upperTriagonal,7-lowerTriagonal
     */
    int matrixType();
    /**
     * @brief выполняет транспонирование матрицы
     * @return транспонированную матрицу
     */
    Matrix& T();
    /**
     * @brief оператор для вывода матрицы в поток
     * @param os - поток для вывода
     * @param matrix - матрица которую нужно вывести
     * @return указатель на поток
     */
    friend std::ostream& operator<<(std::ostream& os, const Matrix& matrix);
    /**
     * @brief загрузка из файла матрицы
     * @param filename - откуда загружать матрицу
     */
    void loadFromFile(const std::string& filename);
    /**
     * @brief загрузка матрицы в файл
     * @param filename - куда загружать матрицу
     */
    void saveToFile(const std::string& filename) const;
    /**
     * @brief оператор присваивания 
     * @param other - откуда присваивать 
     * @return прежнюю матрицу с значениями other
     */
    Matrix& operator=(const Matrix& other);
    /**
     * @brief сложение двух матриц.
     * @param x - другая матрица
     * @return результат сложения двух матриц
     */
    Matrix operator+(Matrix);
    /**
     * @brief сложение матрицы с числом
     * @param x - число
     * @return результат сложения матрицы и числа
     */
    Matrix operator+(double);
    /**
     * @brief присваивающее сложение двух матриц.
     * @param x - другая матрица
     * @return результат сложения двух матриц записывается в прежнюю
     */
    Matrix& operator+=(Matrix);
    /**
     * @brief присваивающее сложение матрицы с числом
     * @param x - число
     * @return результат сложения матрицы и числа записывается в прежнюю
     */
    Matrix& operator+=(double);
    /**
     * @brief разность двух матриц.
     * @param x - другая матрица
     * @return результат разности двух матриц
     */
    Matrix operator-(Matrix);
     /**
     * @brief разность матрицы и числа
     * @param x - число
     * @return результат разности матрицы и числа
     */
    Matrix operator-(double);
    /**
     * @brief присваивающая разность двух матриц.
     * @param x - другая матрица
     * @return результат разности двух матриц записывается в прежнюю
     */
    Matrix& operator-=(Matrix);
    /**
     * @brief присваивающая разность матрицы с числом
     * @param x - число
     * @return результат разности матрицы и числа записывается в прежнюю
     */
    Matrix& operator-=(double);
    /**
     * @brief произведение двух матриц.
     * @param x - другая матрица
     * @return результат произведения двух матриц
     */
    Matrix operator*(Matrix);
     /**
     * @brief произведение матрицы на число
     * @param x - число
     * @return результат произведения матрицы на число
     */
    Matrix operator*(double);
    /**
     * @brief присваивающее произведение матрицы с числом
     * @param x - число
     * @return результат произведения матрицы и числа записывается в прежнюю
     */
    Matrix& operator*=(double);
    /**
     * @brief присваивающее произведение двух матриц.
     * @param x - другая матрица
     * @return результат произведения двух матриц записывается в прежнюю
     */
    Matrix& operator*=(Matrix);
    /**
     * @brief деление матрицы на число
     * @param x - число
     * @return результат деления матрицы на число
     */
    Matrix operator/(double);
    /**
     * @brief присваивающее деление матрицы на число
     * @param x - число
     * @return результат деления матрицы на число записывается в прежнюю
     */
    Matrix& operator/=(double);
    /**
     * @brief возведение матрицы в степень
     * @param x - показатель степени
     * @return результат возведения матрицы в степень x
     */
    Matrix operator^(double);
    /**
     * @brief присваивающее возведение матрицы в степень
     * @param x - показатель степени
     * @return результат возведения матрицы в степень x записывается в прежнюю
     */
    Matrix& operator^=(double);
    /**
     * @brief метод для вычисления определителя матрицы
     * @see getMinor()
     * @return возвращает значение детерминанта, если он может существовать, иначе бросает исключение
     */
    double det();
    /**
     * @brief геттер данных матрицы
     * @return возвращает двумерный массив, состоящий из элементов матрицы
     */
    std::vector<std::vector<double>> getData();
    /**
     * @brief геттер количества строк матрицы
     * @return возвращает целое число - количество строк матрицы
     */
    int getRows();
    /**
     * @brief геттер количества столбцов матрицы
     * @return возвращает целое число - количество столбцов матрицы
     */
    int getCols();
    /**
     * @brief вычисляет норму фробениуса для матрицы.
     * @return возвращает численное значение нормы фробениуса.
     */
    double norm();
};