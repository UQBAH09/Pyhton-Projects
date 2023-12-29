# Take input from the user and convert it to a list
unsortedList = list(input("Enter sentence to sort  "))

# Initialize an empty list to store ASCII values of characters
unsortedAscii = []

# Initialize an empty list to store sorted characters
sortedList = []

# Convert characters to ASCII values and store in the unsortedAscii list
for i in unsortedList:
    unsortedAscii.append(ord(i))

# Get the length of the unsortedAscii list
length = len(unsortedAscii)

# Initialize variables for sorting
num = 100000
i = 0
z = 0
length2 = length

# Perform selection sort on the ASCII values
while z != length:
    i = 0
    num = 1000
    currentLength = len(unsortedAscii)

    # Find the minimum value in the unsortedAscii list
    while i != currentLength:
        if unsortedAscii[i] < num:
            num = unsortedAscii[i]
        i = i + 1

    # Remove the minimum value from unsortedAscii and append to sortedList
    unsortedAscii.remove(num)
    sortedList.append(chr(num))
    z = z + 1

# Print the sorted string
print(''.join(sortedList))
