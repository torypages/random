# Yeah I bet there are easier way of doing this, but I wanted to remind myself
# of this pattern.

# Output should be a recursive list of files in a filesystem tree.

from os import listdir
from os.path import join, expanduser, isdir

def file_list(the_path):
    directory_contents = listdir(the_path)
    rtrn = []
    for afile in directory_contents:
        afile = join(the_path, afile)
        if isdir(afile):
            rtrn.extend(file_list(join(the_path, afile)))
        else:
            rtrn.append(afile)
    return rtrn

print(file_list(expanduser('~/recursiveTest')))

