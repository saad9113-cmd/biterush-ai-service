# class Rectangle :
#     def __init__ (self , length , width):
#         self.length = length
#         self.width = width
#     def area  (self):
#         return self.length * self.width
#     def perimeter (self):
#         return 2 * self.length + self.width
# r = Rectangle (4 , 2)
# print (r.area())
# print (r.perimeter ( ))



# class Employee:
#     count=0
#     def __init__ (self,name):
#         self.name = name
#         Employee.count +=1
# e1 = Employee("Broo")
# e2 = Employee ("yours")
# print (Employee.count)



# class BankAccount:
#     def __init__ (self,balance=0):
#         if balance < 0:
#             raise ValueError
#         self._balance = balance
#     def deposit (self , amount):
#         if amount <= 0:
#             raise ValueError
#         self._balance += amount
#     def withdraw (self , amount):
#         if amount > self._balance:
#             raise ValueError
#         self._balance -= amount
# acc = BankAccount(1000)
# acc.deposit(500)
# acc.withdraw(200)
# print(acc._balance)

# class	Person:
# 				def	__init__(self,	name,	age):
# 								self.name	=	name
# 								self.age	=	age
# 				@classmethod
# 				def	from_string(cls,	data_str):
# 								name,	age	=	data_str.split(",")
# 								return	cls(name.strip(),	int(age.strip()))
# 				def	__repr__(self):
# 								return	f"Person({self.name},	{self.age})"
# p	=	Person.from_string("John,25")
# print(p)



