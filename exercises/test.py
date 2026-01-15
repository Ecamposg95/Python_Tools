# Function to check if a number is prime
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

# Function to find prime numbers in the given interval
def find_primes(start, end):
    if start > end:
        start, end = end, start
    primes = [num for num in range(start, end + 1) if is_prime(num)]
    return primes

# Read input values
start = int(input())
end = int(input())

# Find prime numbers
prime_numbers = find_primes(start, end)

# Print results
print(len(prime_numbers))          # n (cantidad de primos)
print(*prime_numbers)              # res (lista de primos separados por espacio)
