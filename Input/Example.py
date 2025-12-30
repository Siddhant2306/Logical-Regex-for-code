if __name__ == "__main__":
    numbers = input().split()
    total = 0
    
    for num in numbers:  
        total += int(num)
    print(total)