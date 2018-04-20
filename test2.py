def encrypt(word):
    word = word.replace(' a', '%4%')
    word = word.replace('he', '7!')
    word = word.replace('e', '9(*9(')
    word = word.replace('y', '*%$')
    word = word.replace('u', '@@@')
    word = word.replace('an','-?')
    word = word.replace('th','!@+3')
    word = word.replace('o', '7654')
    word = word.replace('9', '2')
    word = word.replace('ck', '%4')
    return word

def decipher(word):
    word = word.replace(' a', '%4%')
    word = word.replace('he', '7!')
    word = word.replace('e', '9(*9(')
    word = word.replace('y', '*%$')
    word = word.replace('u', '@@@')
    word = word.replace('an','-?')
    word = word.replace('th','!@+3')
    word = word.replace('o', '7654')
    word = word.replace('9', '2')
    word = word.replace('ck', '%4')
    
print "--------"
original = raw_input("Enter a string to encode --> ")

print original
print "\n"
encrypted = encrypt(original)
print "Encryped as --> " = encrypted
print "Difference in length --> " + str((len(encrypted) - len(original))
deciphered = decipher(encrypted)