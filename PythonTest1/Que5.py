# Print all the uppercase letters in s, one at a time
# s = 'steganograpHy is the practicE of conceaLing a file, message, image, or video within another fiLe, message, image, Or video.'

s = 'steganograpHy is the practicE of conceaLing a file, message, image, or video within another fiLe, message, image, Or video.'


remove_space="".join(s.strip().split())
remove_coma=remove_space.replace(",","")
remove_dot=remove_coma.replace(".","")
# print(result)
for char in remove_dot:
    if char == char.upper():
        print(char)
