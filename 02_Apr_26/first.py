def show_series(n):
    current = 2
    jump = 10
    for i in range(1, n+2):
        print(current, end=" ")
        if i % 4 == 0:
            current += jump
            jump += 10
        else:
            current += 2
n = int(input("Enter n: "))
show_series(n)