from testEngine import O
import random
from math import floor

class sample:
    def __init__(self, maxNumber):
        self.max = maxNumber
        self.n = 0
        self.sorted = False
        self.some = []

    def sampleInc(self, x):
        self.n += 1
        now = len(self.some)
        if now < self.max:
            self.sorted = False
            self.some.append(x)
        elif random.random() < (now / self.n):
            self.sorted = False
            #print(floor(0.5 + (random.random() * now)))
            self.some[int(random.random() * now)] = x
        return x

    def sampleSorted(self):
        if self.sorted == False:
            self.sorted == True
        self.some.sort()
        return self.some

    def nth(self, n):
        s = self.sampleSorted()
        return s[min(len(s), max(1, floor(0.5 + len(s) * n)))]

#testing
@O.k
def testing():
    random.seed(1)
    s = []
    for i in range(5, 11):
        s.append(sample(2 ** i))

    for obj in s:
        for i in range(1, 1001):
            #print(i)
            random_number = random.random()
            #print(random_number)
            obj.sampleInc(random_number)

    for obj in s:
        assert abs(obj.nth(0.5) - 0.5) < 0.2

if __name__== "__main__":
  O.report()