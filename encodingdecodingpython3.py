#!/usr/bin/env python3
# In Python 3 quotes without a prefix is a string, a unicode string.
# So, str here means unicode str.

print("Unicode by default.")
print(type("Hello"))  # str
print(type("\u2603"))  # str, stores code points.

# You have to instead tell Python that you want a Byte String if that is
# what you want.

print("Excplicit Byte String.")
print(type(b"Hello"))  # bytes

print("No implicit conversion.")
try:
    print("Hello " + b"world!")
except TypeError as e:
    # Can't convert 'bytes' object to str implicitly
    print(e)

print("The two types cannot be equal.")
print("Hello" == b"Hello")  # False

print("Even with dict key errors.")
d = {"Hello": "world"}
try:
    print(d[b"Hello"])
except KeyError as e:
    print("There is no key " + str(e))




