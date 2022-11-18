n1 = int(input())
A = set()
a = ' '
count = 0
B = set()

while a not in A and count != n1:
    count += 1
    a = input()
    A.add(a)
while count != n1:
    count += 1
    a = input()
    if a in A:
        B.add(a)

print(len(B))