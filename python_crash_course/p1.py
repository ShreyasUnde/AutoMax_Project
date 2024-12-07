# def sum(a,b):
#     return (a+b)

# a=int(input("Enter 1st number: "))
# b=int(input("Enter 2nd number: "))

# print(f'Sum of {a} and {b} is {sum(a,b)}')

#single line comment
'''
For 
Multi 
Line 
Comment
'''

# ==========================================================

# name=input("Enter your name ")
# print(f'Hello {name}!!')

# name="Sahil"
# print(type(name))


# ============================================================

# x="Hello I am Global Variable"


# def func():
#     global y     #made the func variable global so we can use it anywhere within the code
#     y="Hello I am Local Variable"

# print(x)
# func()   #to access y first I have call the func
# print(y)

# ============================================================

# name="Sahil Somnath Thorat"
# print(name)
# print(name[0])
# print(len(name))


#How to print multi lines
# intro="""
#         My name is Sahil
#         I am 20 years old
#         I am currently studying in SAKEC in Computer Department

#     """
# print(intro)

#how to perform concatenation on strings

x=input("Enter Your First Name ")
y=input("Enter Your Second Name ")
z=input("Enter Your Third Name ")
age=int(input("Enter your age "))
# print(x+y+z)
# print(f'Hello {x} {y} {z} I got it your age is {age}')
s='{} {} {} I got it your age is {}'.format(x,y,z,age)
print(s)
