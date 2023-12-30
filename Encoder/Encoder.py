# Import the random module for generating random numbers
import random

# Ask the user whether they want to encode or decode
choice = input("Welcome to encoder.io. Do you want to encode or decode. (en/de)")

if choice == "en":
    # If the choice is to encode, take a sentence as input
    word = list(input("Enter a sentence to encode:\n"))
    length = len(word)

    # Initialize lists for the encoding key and the encoded word
    encodeKey = []
    encodedWord = []

    i = 0
    while i != length:
        # Get the ASCII value of the current character
        AsciiNum = ord(word[i])

        # Generate a random encoding key and subtract it from the ASCII value
        encodeKey.append(random.randint(0, 3))
        num = AsciiNum - encodeKey[i]

        # Append the encoded character to the list
        encodedWord.append(chr(num))

        # Convert the encoding key to a string for display
        encodeKey[i] = str(encodeKey[i])
        i = i + 1

    # Print the encoded word and the encoding key
    print("Your encoded word is:", ''.join(encodeKey))
    print("Your encoded word is:", ''.join(encodedWord))

elif choice == "de":
    # If the choice is to decode, take an encoded sentence and the encoding key as input
    encodedWord = list(input("Enter a sentence to decode:\n"))
    encodeKey = list(input("Enter a key to decode:\n"))
    length = len(encodedWord)

    # Initialize lists for the ASCII values and the decoded word
    num = []
    decodedWord = []

    i = 0
    while i != length:
        # Get the ASCII value of the current encoded character
        AsciiNum = ord(encodedWord[i])

        # Add the encoding key to the ASCII value to decode
        num.append(AsciiNum + int(encodeKey[i]))

        # Append the decoded character to the list
        decodedWord.append(chr(num[i]))
        i = i + 1

    # Print the decoded word
    print("Your decoded word is:", ''.join(decodedWord))
