import re

# Sample text
txt = "the python is easy"

# Find all occurrences of the substring 'th' in the text
output = re.findall('th', txt)  # Returns a list of all matches
print(output)  # Output: ['th','th']

# Search for the first occurrence of a space character
output = re.search('\s', txt)  # Returns a match object for the first space
print(output.start())  # Output: 3 (position of the first space character)

# Split the string by spaces, limiting the split to 1 occurrence
output = re.split('\s', txt, 1)  # Splits only once at the first space
print(output)  # Output: ['the', 'python is easy']

# Replace all space characters with '9'
print(re.sub("\s", "9", txt))  # Output: 'the9python9is9easy'

# Replace only the first space character with '9'
print(re.sub("\s", "9", txt, 1))  # Output: 'the9python is easy'

# New text for testing word boundary and match
txt = "The rain in Spain"

# Search for a word starting with 'S'
x = re.search(r"\bS\w+", txt)  # \b matches a word boundary, \w+ matches one or more word characters

# Output the matched word
print(x.group())  # Output: 'Spain'

# Output the position of the match in the text
print(x.span())  # Output: (15, 20) (Start and end positions of the match)






