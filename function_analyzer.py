import sys
# a very crude script to get stats on the functions of a class I made.
# supply file as argument.

my_file = """

    def heythere():
      '''
      stufff
      '''
      def jjj():
         bbb

      more stuff
      # thing


    def thing():
      {}
      sdlkfj
      sdfsdf
      sdfsdf
      {}

      code
      more code
""".format('"""', '"""')

if len(sys.argv) == 2:
    f = open(sys.argv[1])
else:
    from cStringIO import StringIO
    f = StringIO(my_file)

line_count = 0
sizes = []
first_func = True
in_comment = False
for line in f.readlines():
    if not line.strip():
        continue
    line = line[4:]
    line = line.rstrip()

    if line.startswith('def'):
        if not first_func:
            sizes.append(line_count)
            line_count = 0
            print('+++++++++++++++++++++++++++++++++++++++')
        else:
            first_func = False
        continue

    line = line.strip()
    if not line or line.startswith('#'):
        continue

    if line.startswith("'''") or line.startswith('"""'):
        if in_comment:
            in_comment = False
        else:
            in_comment = True
        continue

    if in_comment:
        continue

    line_count += 1
    print(line)
sizes.append(line_count)

print('max', max(sizes))
print('average', float(sum(sizes))/len(sizes))
print('min', min(sizes))
