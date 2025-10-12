/** 
 * @file set.h
 * @author qudef
 * @brief Множество, поддерживающее вложенность 
 * 
 * Класс `set` представляет из себя множество, способное содержать вложенные множества и целые числа
 * вложенность реализуется с помощью библиотеки `std::variant`. Вложенные множества хрянятся в качестве `std::shared_ptr<set>`.
 * Поддерживает операции пересечения, объединения, разности и булеана. Множество может быть задано задано через строку, массив типа char
 * или через std::initializer_list.
 * 
 */
#pragma once
#include <iostream>
#include <vector>
#include <variant>
#include <string>
#include <memory>
#include <initializer_list>
#include <algorithm>

/**
 * @class set
 * @brief Реализует поставленную задачу(вложенное множество). Хранит в себе необходимые поля и методы.
 */
class set;
using Element = std::variant<int, std::shared_ptr<set>>;
// документация doxygen
class set{
private:
    std::vector<Element> elements;///< Вектор, которые представляет из себя множество.
    int size;///< Поле размера
    /**
     * @brief Проверяет содержится ли чило в множестве.
     * @param value - целое чило которое нужно проверить.
     * @return Возвращает содержится ли элемент в множестве.
     */
    bool contains_int(int) const;
    /**
     * @brief Аналогичный методу contains_int
     * @param Указатель на set.
     * @return Возвращает содержится ли элемент в множестве.
     */
    bool contains_set(std::shared_ptr<set>) const;
    /**
     * @struct Парсер для обработки строк.
     * @brief Содержит в себе необходимые методы и поля для обработки строки.
     */
    struct Parser{

        private:
        
        std::string input;///< Обрабатываемая строка
        int pos=0;///< Текущая позиция
        /**
         * @brief пропускает пробелы
         */
        void ignore_w();
        /**
         * @brief парсит один элемент 
         * @return возвращает распознанный элемент (либо int, либо shared_ptr<set>)
         */
        Element parse_element();
        /**
         * @brief вспомогательный метод для parse_element()
         * @return возвращает обработанное целое число
         */
        int parse_int();
        /**
         * @brief вспомогательный метод для parse_element()
         * @return возвращает указатель на обработанное множество.
         */
        std::shared_ptr<set> parse_set();
        public:
        /**
         * @brief Публичный метод для запуска парсера.
         * @param str строка для парсинга.
         * @return указатель на обработанное множество.
         * @see set::set(std::string)
         */
        std::shared_ptr<set> parse(std::string str);
    };
public:
    /**
     * @brief Конструктор по умолчанию(пустое множество).
     */
    set();
    /**
     * @brief Конструктор через initializer_list
     * @param список целых чисел для инициализации
     */
    set(std::initializer_list<int>);
    /**
     * @brief Конструктор через initializer_list
     * @param список целых чисел и указателей на set
     */
    set(std::initializer_list<Element>); 
    /**
     * @brief Конструктор через строку
     * @param str содержащую множество вида ({1,{2}})
     */
    set(std::string);
    /**
     * @brief Конструктор через массив char.
     * @param Массив char в стиле С-string.
     */
    set(const char*);
    
    /**
     * @brief метод добавления int в множество
     * @param value - целое число
     * Вызывает внутри себя метод contains 
     * @see contains(int)
     */
    void add(int);
    /**
     * @brief метод добавления вложенного множества в множество
     * @param s - указатель на множество
     * Вызывает внутри себя метод contains 
     * @see contains(std::shared_ptr<set>)
     */
    void add(std::shared_ptr<set>);
    /**
     * @brief проверяет пустое ли множество.
     * @return возвращает true - пустое, false - содержит элементы.
     */
    bool is_null() const;
    /**
     * @brief метод проверки включения вложенного множества в множество
     * @param s - указатель на множество
     * @return true - содержится, false - не содержится
     */
    bool contains(std::shared_ptr<set>) const;
    /**
     * @brief метод проверки включения числа в множество
     * @param value - целое число
     * @return true - содержится, false - не содержится
     */
    bool contains(int) const;
    /**
     * @brief геттер размера множества.
     * @return параметр value.
     */
    int get_size() const;
    /**
     * @brief метод удаления элемента из множества
     * @param целое число или указатель на множество
     * @return true - удаление призведено false - нет.
     */
    bool remove(const Element&);
    /**
     * @brief Создание булеана множества.
     * @return возвращает множества булеана.
     */
    set boolean();
    /**
     * @brief оператор присваивания, заполняет поля текущего объекта, полями другого.
     * @param s - другое множество
     * @return возвращает ссылку this
     */
    set& operator=(const set&);
    /**
     * @brief перегруженный оператор +, выполняет объединение двух множеств.
     * @param s - второе множество.
     * @return результат объединения множеств.
     */
    set operator+(const set&) const;
    /**
     * @brief перегруженный оператор +=, выполняет объединение двух множеств.
     * @param s - второе множество.
     * @return результат объединения множеств записывается в исходное.
     */
    set& operator+=(const set&);
    /**
     * @brief перегруженный оператор *, выполняет пересечение двух множеств.
     * @param s - второе множество.
     * @return результат пересечения множеств.
     */
    set operator*(const set&) const;
    /**
     * @brief перегруженный оператор *=, выполняет объединение двух множеств.
     * @param s - второе множество.
     * @return результат пересечения множеств записывается в исходное.
     */
    set& operator*=(const set&);
    /**
     * @brief перегруженный оператор -, выполняет пересечение двух множеств.
     * @param s - второе множество.
     * @return результат разности множеств.
     */
    set operator-(const set&) const;
    /**
     * @brief перегруженный оператор -=, выполняет объединение двух множеств.
     * @param s - второе множество.
     * @return результат разности множеств записывается в исходное.
     */
    set& operator-=(const set&);
    /**
     * @brief перегруженный оператор [], выполняет проверку содержания элемента в множестве.
     * @param el - либо целое число, либо указатель для множества.
     * @return true - содержится, false - нет.
     * @see contains() - вызывается внутри функции.
     */
    bool operator[](Element);
    /**
     * @brief перегруженный оператор ==, выполняет сравнение двух множеств.
     * @param s - другое множество.
     * @return true - совпадает, false - нет.
     */
    bool operator==(const set&) const; 
    /**
     * @brief перегруженный оператор !=, выполняет сравнение двух множеств.
     * @param s - другое множество.
     * @return true - не совпадают, false - совпадают.
     */
    bool operator!=(const set&) const;
    /**
     * @brief оператор ввода множества из потока.
     * @param is - Входной поток
     * @param s - Множество для записи.
     * @return ссылка на входной поток
     * @see Parser
     */
    friend std::istream& operator>>(std::istream&,set&);
    /**
     * @brief оператор вывода множества в поток.
     * @param os - Выходной поток
     * @param s - Множество для вывода.
     * @return ссылка на входной поток
     */
    friend std::ostream& operator<<(std::ostream&,set);
    /**
     * @brief Создает указатель на вложенное множество.
     * @param init - список элементов для инициализации.
     * @return указатель на новое множество.
     * @see set(initializer_list).
     */
    static std::shared_ptr<set> make_nested_set(std::initializer_list<Element> init = {}); 
};
//g++ -std=c++17 -fprofile-arcs -ftest-coverage set.cpp test.cpp -I/usr/include -lUnitTest++ -o tests && ./tests && gcov tests-set.gcov


