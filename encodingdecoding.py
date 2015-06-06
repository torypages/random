#! /usr/bin/env python2
# This are notes made based on http://nedbatchelder.com/text/unipain.html
# https://www.youtube.com/watch?v=sgHbC6udIqc

print("====SECTION 1====")
# This stores bytes.
my_string = "Hello World"
print(type(my_string))  # str
print(my_string)  # Hello World

print("++++")

# This stores "unicode code points" called unicode.
# Unicode String that stores Unicode Code Points
my_unicode = u"Hi \u2603"  # Hi snowman
print(type(my_unicode))  # unicode
print(my_unicode)  # Hi snowman

print("\n\n====SECTION 2====")
# Unicode strings have an "encode" method that will convert it into bytes.
# Byte strings have a "decode" method that will turn it into unicode.

print("++my_unicode")
my_unicode = u"\u0048\u0069"  # Hi
print(len(my_unicode)) # 2
print(my_unicode) # Hi
print(type(my_unicode))  # unicode

print("++my_utf8")
my_utf8 = my_unicode.encode('utf-8')  # Creates a byte string.
print(len(my_utf8))  # 2, for two bytes.
print(type(my_utf8))  # str
print(my_utf8)  # Hi
print('repr', repr(my_utf8))

print("++also my_utf8, better example")
my_unicode = u"Hi \u2603"  # Hi snowman
my_utf8 = my_unicode.encode('utf-8')
print(len(my_utf8))  # 6
print(type(my_utf8))  # str
print(my_utf8)  # Hi snowman
print('repr', repr(my_utf8))  # 'Hi \\xe2\\x98\\x83'"  byte hexidecimal escaped
print('repr decoded', repr(my_utf8.decode('utf-8')))
print(my_utf8.decode('utf-8'))

print("\n\n====SECTION 3====")
# Hi can be encoded in ascii but snowman cannot.
unicode_H = u"\u0048"
unicode_snowman = u"\u2603"
whatever = unicode_H.encode('ascii')  # H is part of ascii.
try:
    whatever = unicode_snowman.encode('ascii')  # Snowman is not.
except UnicodeEncodeError, e:
    # 'ascii' codec can't encode character u'\u2603' in position 0: ordinal
    # not in range(128)
    print(e)

print("\n\n====SECTION 4====")
# If you have complicated characters, like a snowman, that can't be represented
# by ascii encoded into a byte string being represented by escaped
# hexidecimals, and try and create unicode from that, that is, using the
# decode method, but you use ascii as a means of translating, you will get
# an error since there is no snowman in ascii.
unicode_snowman = u"\u2603"  # A snowman.

# Create a utf-8 encoded byte string
utf8_byte_string_snowman = unicode_snowman.encode('utf-8')
try:
    # You can't decode this with ascii because ascii does not know
    # about snowmen.
    whatever = utf8_byte_string_snowman.decode('ascii')
except UnicodeDecodeError, e:
    # 'ascii' codec can't decode byte 0xe2 in position 0:
    # ordinal not in range(128)
    print(e)
# However, it is perfectly legit to decode using 'utf-8' because utf-8
# knows about snowmen.
whatever = utf8_byte_string_snowman.decode('utf-8')
print("Got here without error.")


print("====SECTION 4.1====")
# There is such thing as invalid utf-8 encoded characters
try:
    "\x9a that is made up and does not exist".decode('utf-8')
except UnicodeDecodeError:
    # 'ascii' codec can't decode byte 0xe2 in position 0:
    # ordinal not in range(128)
    print(e)

print("\n\n====SECTION 5====")
# handling errors while encoding

unicode_hi_snowman = u"hi \u2603"
# hi ?
print(repr(unicode_hi_snowman.encode('ascii', 'replace')))

# hi &#9731;
# This is really cool for web work.
print(repr(unicode_hi_snowman.encode('ascii', 'xmlcharrefreplace')))

# 'hi '
print(repr(unicode_hi_snowman.encode('ascii', 'ignore')))

print("\n\n====SECTION 5.1====")
# handing errors while decoding
unicode_snowman = u"\u2603"  # A snowman.
# Create a utf-8 encoded byte string
utf8_byte_string_snowman = unicode_snowman.encode('utf-8')

# Now try and convert back to a Byte String using some error handling
# aka replacement strategies.
my_unicode = utf8_byte_string_snowman.decode('ascii', 'ignore')
print(repr(my_unicode))  # ""   aka nothing.

my_unicode = utf8_byte_string_snowman.decode('ascii', 'replace')
print(repr(my_unicode))  # \ufffd\ufffd\ufffd aka unicode replacement chars.
print(my_unicode)  # 3 diamonds with question marks in them

print("\n\n====SECTION 5.1====")
# implicit conversion from Byte Strings to Unicode
# world will be decoded as ascii
print(repr(u"Hello " + "world."))
# this is equivalent to
print(repr(u"Hello " + ("world".decode('ascii'))))

# It chose to use ascii based on the output of
import sys
print(sys.getdefaultencoding())
# which returns ascii

# and of course you can get the same decode errors here.
# This is why there is pain, these implicit conversions work fine
# until this implicit conversion stops working.

# These implicit conversion can happen in many places. Like with a format.

# or if standard out is unicode, you might be trying to convert ascii to
# unicode while printing.

# In any concatenation, or format, if one part is unicode, it will have
# to bump itself up to unicode from the byte strings, this means decoding.

print("++++")
# Encode is an operation on unicode strings to produce byte strings.
unicode_snowman = u"\u2603"  # A snowman.
utf8_byte_string_snowman = unicode_snowman.encode('utf-8')
print(type(utf8_byte_string_snowman))  # str, Byte String
# Okay, so, we have a byte string, byte strings do not have an encode
# method, but unicode does.
try:
    utf8_byte_string_snowman.encode('utf-8')
except UnicodeDecodeError, e:
    # 'ascii' codec can't decode byte 0xe2 in position 0:
    #  ordinal not in range(128)
    print(e)
    # An error about ascii when I was doing utf-8!?!?!??!?!?!?!
print("2++++")
# Since python knows how to encode a byte string, it will try and use the
# default ascii decoder to create a byte string first so that it can then
# do the utf-8 encode asked for. The above is akin to:
try:
    # sys.getdefaultencoding() == ascii
    a = utf8_byte_string_snowman.decode(sys.getdefaultencoding())
    print("This does not print.")
    a.encode('utf-8')  # never gets to here
except UnicodeDecodeError, e:
    # 'ascii' codec can't decode byte 0xe2 in position 0:
    #  ordinal not in range(128)
    print(e)
    # The implicit conversion is why there was the ascii error above
    # when I was asking for utf-8



""" Other random notes
I specified \u---- that is, a backslash u followed by four hex digits. Sometimes
you will need \U-------- that is the same thing but with 8 hex digits.

String is ambiguous, you need to know if it is a byte string or a
unicode string. If it is a byte string you need to know what encoding it is.
For example, utf-8. You have to be told this or guess. Cannot look at a stream
of btyes (or probably commonly refered to as text) to know this.

I/O is always bytes

Unicode sandwich: bring in byte strings, convert to unicode, output in
                  byte strings.

Know if you are dealing with bytes or unicode.

"""
