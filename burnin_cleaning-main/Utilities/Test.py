# Define the two lists of file paths
list_a = ["file1.txt", "file2.txt", "file3.txt"]
list_b = ["file2.txt", "file4.txt", "file5.txt"]

# Create a dictionary to store the marks for list A
marked_a = {item: (True if item in list_b else False) for item in list_a}

# Create a dictionary to store the marks for list B
marked_b = {item: ("Found in A" if item in list_a else "Not found in A") for item in list_b}

# Combine the results
print("Marked List A:", marked_a)
print("Marked List B:", marked_b)
