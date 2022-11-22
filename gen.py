import random
amount = input("How many tokens do you want to generate? ")

genned = []
def gen():
    ar = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    return random.choice(ar)

try:
  amount = int(amount)
  for x in range(amount):
    token = ""
    for x in range(40):
      newLetter = gen()
      token = token + newLetter
    print(token)
    genned.append(token)
  f = open('tokens.txt', 'w')
  f.write("\n".join(genned))
except Exception as e:
    print("You didn't enter a number.")
