import csv
from datetime import date


def fibonacci(n):
    fib1 = 0
    fib2 = 1
    while n > 0:
        fib1, fib2 = fib2, fib1 + fib2
        n -= 1
    return fib1


def date_fibonacci():
    return fibonacci(date.today().day)


def save_transactions(data):
    with open("transactions.csv", "w") as f:
        write = csv.writer(f)
        write.writerows(data)
