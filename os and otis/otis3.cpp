#include <iostream>
#include <pthread.h>
#include <unistd.h>
#include <chrono>
#include <thread>
#include <random>

/*
    g++ -std=c++17 -pthread -O2 otis3.cpp -o otis3 && ./otis3
*/

const int N = 5;
pthread_mutex_t forks[N];  // Мьютексы — по одному на каждую вилку
pthread_mutex_t print_mutex;

std::mt19937_64 rng(std::chrono::steady_clock::now().time_since_epoch().count());

int rand_ms(int lo=2000,int hi=5000){
    std::uniform_int_distribution<int> dist(lo,hi);
    return dist(rng);
}

void think(int id) {
    int t = rand_ms();
    pthread_mutex_lock(&print_mutex);
    std::cout << "Philosopher " << id << " thinking " << t << " ms\n";
    pthread_mutex_unlock(&print_mutex);
    std::this_thread::sleep_for(std::chrono::milliseconds(t));
}

void eat(int id) {
    int t = rand_ms(2000, 10000);
    pthread_mutex_lock(&print_mutex);
    std::cout << "Philosopher " << id << " eating " << t << " ms\n";
    pthread_mutex_unlock(&print_mutex);
    std::this_thread::sleep_for(std::chrono::milliseconds(t));
}

void* philosopher(void* arg) {
    int id = *(int*)arg;
    int left = id;
    int right = (id + 1) % N;

    for (int i = 0; i < 2; ++i) {  
        think(id);

        // Стратегия предотвращения взаимной блокировки
        if (id % 2 == 0) {
            pthread_mutex_lock(&forks[left]);

            pthread_mutex_lock(&print_mutex);
            std::cout << "Philosopher " << id << " took left fork " << left << "\n";
            pthread_mutex_unlock(&print_mutex);


            pthread_mutex_lock(&forks[right]);

            pthread_mutex_lock(&print_mutex);
            std::cout << "Philosopher " << id << " took right fork " << right << "\n";
            pthread_mutex_unlock(&print_mutex);
        } else {
            pthread_mutex_lock(&forks[right]);

            pthread_mutex_lock(&print_mutex);
            std::cout << "Philosopher " << id << " took right fork " << right << "\n";
            pthread_mutex_unlock(&print_mutex);

            pthread_mutex_lock(&forks[left]);

            pthread_mutex_lock(&print_mutex);
            std::cout << "Philosopher " << id << " took left fork " << left << "\n";
            pthread_mutex_unlock(&print_mutex);

        }

        eat(id);

        pthread_mutex_unlock(&forks[left]);
        pthread_mutex_unlock(&forks[right]);

        pthread_mutex_lock(&print_mutex);
        std::cout << "Philosopher " << id << " took forks down\n";
        pthread_mutex_unlock(&print_mutex);
    }
    pthread_mutex_lock(&print_mutex);
    std::cout << "Philosopher " << id << " ended eating.\n";
    pthread_mutex_unlock(&print_mutex);
    return nullptr;
}

int main() {
    pthread_t threads[N];
    int ids[N];

    // Инициализация мьютексов
    for (int i = 0; i < N; ++i) {
        pthread_mutex_init(&forks[i], nullptr);
    }

    // Запуск философов
    for (int i = 0; i < N; ++i) {
        ids[i] = i;
        pthread_create(&threads[i], nullptr, philosopher, &ids[i]);
    }

    // Ожидание завершения
    for (int i = 0; i < N; ++i) {
        pthread_join(threads[i], nullptr);
    }

    // Уничтожение мьютексов
    for (int i = 0; i < N; ++i) {
        pthread_mutex_destroy(&forks[i]);
    }

    std::cout << "all philosophers ended.\n";
    return 0;
}