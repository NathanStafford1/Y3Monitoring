import copy

print("Hello, World")

# Arithmetic operators

print(1+1)
print(1-1)
print(5*10)
print(10/5)
print(((6+9)*3)+3)
print(6 % 2)
# ** raises to the power of
print(6**2)
# //
print(13/2)
print(13//2)

print(6 ^ 2)

# Variables
age = 20

# integers are immutable in Python

a = 1
b = a
a = "Hello, world"
print(b)

a = 1
b = a
a = a - 1
print(b)

# Lists are mutable in Python
list_1 = [1, 2, 3]
list_2 = list_1
list_2 = [2, 3, 4]

list_1 = [6, 7, 8]
list_2 = list_1
list_1[0] = 22
print(list_2)

# Shallow and Deep Copies
a = [1, 3, 4, 7]
b = copy.copy(a)
b[0] = -1
print(a)
print(b)

a = [1, 3, 5, 7]
b = [2, 4, 6, 8]
c = [a, b]
d = copy.copy(c)
a[0] = -1
c[0][1] = -3
print(d)

# Deep copy
a = [1, 3, 5, 7]
b = [2, 4, 6, 8]
c = [a, b]
d = copy.deepcopy(c)
a[0] = -1
c[0][1] = -3
print(d)

# Equality
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)
print(a == c)
print(a is c)
print(a is b)

# Problems with dynamically typed languages
a = [1, 2, 3]
a = 1
#a[0] = 1

# Variables
age, name, gender = 25, "John", "Male"
# Use snake_case, stick to Python coding conventions
# https://realpython.com/python-pep8/#naming-styles
blood_type = "AB"

# Numeric Python
very_big_number = 5000000000
print(very_big_number)

x = 7
y = 3
z = x/y
print(z)
print(type(z))

print(int(7/3.5))

# Strings
movie_title = "Scarface"
print(movie_title.upper())
print(movie_title.count('a'))

# Collections in Python
# List

names = ["Teodor", "Vincent", "Angel"]
print(names[2])
#print(names[100])

random_variables = [True, False, 'Hello', 1, 1.2]
print(len(random_variables))
length = len(random_variables)
print(random_variables[-2])

# Booleans
this_course_is_awesome = True
this_course_is_not_awesome = False
comparison = 1 > 2
print(comparison)

# and, or, not
print((1 < 2) or (2 < 3))
print((1 < 2) or (2 > 3))
print((1 < 2) and (2 > 3))
print(not(1 < 2))

# region Methods
movie_title = "American History X"
print(movie_title.upper())
print(movie_title.lower().count('a'))
# endregion

# region Lists
names = ["Tim", "Kyle", "KevinG", "KevinB"]
print(names[0])
#print(names[100])

random_variables = [True, False, "Hello", 1, 1.2]
#print(len(random_variables))
length = len(random_variables)
print(random_variables[length-1])
print(random_variables[-1])

ordered_numbers = list(range(0, 101))
print(ordered_numbers)
print(ordered_numbers[2:11])
print(ordered_numbers[int(len(ordered_numbers)/2):])
print(ordered_numbers[:len(ordered_numbers)//2])

print(list(range(100)))
print(list(range(0, 101, 5)))

show_title = "The Office"
print(show_title[2])
print(show_title[4:])

months = ['Jan', 'Feb', 'Mar']
print('Jan' in months)
print('Jun' in months)

best_show = "The Office"
print('the' in best_show.lower())
# endregion

# region Mutability
grocery_list = ['Bananas', 'Apples', 'Cauliflower']
grocery_list[2] = 'Broccoli'
print(grocery_list)

misspelled_vegetable = "Cucomber"
correctly_spelled_veg = "Cucumber"
print(misspelled_vegetable)

name = "Nikita"
other_name = name
name = "Tim"
print(name)
print(other_name)

books = ["The Collection of Sherlock Holmes", "The BFG", "Time shelter"]
more_books = books
books[0] = "Better C++"
print(books[0])
print(more_books)

# Common functions and methods for lists

numbers = [4, 5, 6, 7]
print(len(numbers))
print(max(numbers))
names = ["KevinG", "KevinB", "Conor", "Vincent", "1", "-1", "a"]
print(max(names))
print(min(names))

print(sorted(numbers))

print('-'.join(['Jan', 'Feb', 'Mar']))
print(' '.join(['Jan', 'Feb', 'Mar']))

print('This person is {}, {} and {}'.format('tall', 'thin', 'old'))

months = ['Jan', 'Feb', 'Mar']
months.append('Apr')
print(months)
# endregion

# region Tuples
# Tuples immutable, ordered
traits = ('tall', 'slim', 23)
# height = traits[0]
# build = traits[1]
# age = traits[2]
height, build, age = traits
# endregion

# region Sets
# Mutable, unordered, unique elements
duplicate_numbers = [1, 1, 2, 2, 3, 3]
unique_numbers = set(duplicate_numbers)
print(unique_numbers)
unique_numbers.add(4)
unique_numbers.add(3)
print(2 in unique_numbers)

# endregion

# region Dictionaries
# Mutable, Unordered, keys must be unique and immutable
inventory = {'bananas': 1.59, 'apples': 1.29, 'grapes' : 3.99}
print(inventory['bananas'])
inventory['bananas'] = 1.49
bananas_price = inventory.get('bananas')
strawberries_price = inventory.get('strawberries')
print(strawberries_price)
print('celery' in inventory)

grocery_items = {'bananas': {'price': 1.49, 'country_of_origin': 'Brazil'}, 'apples': {'price': 1.29, 'country_of_origin': 'Ireland'}}
print(grocery_items['bananas']['country_of_origin'])

# endregion

# region if
item = 'cabbage'
price = 5.99
if item in grocery_items:
    print("Found the item")
elif price > 5.00:
    print("Too expensive. Not adding")
else:
    print("Not found")
    grocery_items.update({'cabbage': {'price': 0.79, 'country_of_origin': 'Ireland'}})

print(grocery_items)


def type_of_flow(reynolds_value):
    if reynolds_value < 2000:
        print("Laminar")
    elif reynolds_value >=2000 and reynolds_value < 10000:
        print("Transitional")
    else:
        print("Turbulent")


type_of_flow(1000)
type_of_flow(8000)
type_of_flow(12000)

months = ['Jan', 'Feb', 'Mar']
for month in months:
    print(month)

for number in range(0, 100):
    print(number)

names = ['kevin silvester', 'nathan', 'annas']
for index in range(len(names)):
    names[index] = names[index].capitalize()
print(names)

movies = {'The Goonies': 1982, 'Shawshank Redemption': 1994, 'Titanic': 1997}

for key in movies:
    print(key)

for key, value in movies.items():
    print(key, value)

for key, value in movies.items():
    print("The movie {}, was released in {}".format(key, value))


random_number = 20
while random_number < 30:
    print(random_number)
    random_number+=1


numbers = list(range(10))
print(numbers)

for number in numbers:
    if number % 2 != 0:
        break
    print(number)

the_best_student = 'David'


def square(n):
    print(the_best_student)
    return n*n

print(the_best_student)



print(square(5))

# region Higher Order Functions
numbers = [1, 2, 3, 4, 5, 6]
print(numbers)

def even_or_odd(number):
    return number % 2 == 0


print(list(filter(even_or_odd, numbers)))
# endregion

# region Lambda Functions
# Lambda, anonymous function, used once
print(list(filter(lambda num: num % 2 == 0, numbers)))

# endregion













# endregion