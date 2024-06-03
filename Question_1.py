import csv
import pandas as pd

# Question 1:Count the number of words that contain a’s, b’s, …,z’s and create a frequency table
# Initialize a dictionary to store the count of words containing each letter

letter_counts = {chr(letter): 0 for letter in range(ord('a'), ord('z') + 1)}
#print(letter_counts)

# Read the CSV file
with open('word_list.csv', mode='r') as file:
    reader = csv.reader(file)
    # TAke the words in the first column of the CSV
    words = [row[0] for row in reader]
    # print(words)


# Count the number of words containing each letter
for word in words:
    unique_letters = set(word)  # Use a set to avoid counting the same letter multiple times in a word
                                # Example "aback" =>"abck"   a: 1, b: 1, c: 1, k :1
    # print(unique_letters)
    for letter in unique_letters:
        if letter in letter_counts:
            letter_counts[letter] += 1

"""# Print the results
for letter, count in letter_counts.items():
    print(f"{letter}: {count}")"""


df = pd.DataFrame(letter_counts.items(), columns=['Letter', 'Frequency'])
df.index = df.index + 1
# print(df)


# Question 2: Which letters only appear once in every word?

"""
    'abcac' : b
    'abcabce': e
    'ebfacb': a, e
    final output:
    table
    word        letter_once
    'abcac'         b
    'abcabce'       e
    'ebfacb'        a, e
    """

result = []
for word in words:
    letter_count_per_word = {chr(letter): 0 for letter in range(ord('a'), ord('z') + 1)}
    letter_once_count = {chr(letter): 0 for letter in range(ord('a'), ord('z') + 1)}
    table = {}
    for letter in word:
        if letter in letter_count_per_word:
            letter_count_per_word[letter] += 1
    # at the end of iteration we will have for abbey word 
    # letter_count_per_word = {'a': 1, 'b': 2, 'e' :1, 'f': 1}
    # Find letters that appear exactly once
    letter_list = [letter for letter, count in letter_count_per_word.items() if count == 1]
    # Append the word and its unique letters to the result list
    result.append({'Word': word, 'Unique_letters': letter_list})

# Create a DataFrame from the result list
df_2 = pd.DataFrame(result, columns=['Word', 'Unique_letters'])
df_2.index += 1
#print(df_2)

# Question 3: Count the number of words that contain aa, ab,…, zz and create a frequency table 
"""
Letter1     Letter2     Frequency
a           a           0
b           a           35
c           a           53
.
.
.
g           t           ??
z           z           ??


1. generate a list of letter combinaison: ["aa", "ba", "ca", ...."zz"]
2. check for each word the frequency of each combinaison: "aback"
    aa      0
    ab      1
    ac      1
    .
    .
    ba      1
    .
    .
    .
    kc      1    
"""
def check_word(word, combination):
    """
    aback
    """
    for i in range(len(word) + 1 ):
        try:
            string_1 = word[i]
            string_2 =  word[i + 1]
            to_compare = string_1 + string_2
            if to_compare in combination:
                combination[to_compare] += 1
                #print(word)
                #print('value found: ', to_compare)
            #print(to_compare)
        except IndexError:
            pass


# Create a list of all possible letter combinations
letter_combinations = {chr(letter2) + chr(letter1): 0 for letter1 in range(ord('a'), ord('z') + 1) for letter2 in range(ord('a'), ord('z') + 1)}
#print(letter_combinations)

for word in words:
    check_word(word, letter_combinations)
"""df_3 = pd.DataFrame(letter_combinations.items, columns=["letters", "frequency"])
print(df_3)"""
# Create a list of dictionaries with the desired format
formatted_data = [{"Letter1": pair[0], "Letter2": pair[1], "Frequency": freq} for pair, freq in letter_combinations.items()]

df_combinations = pd.DataFrame(formatted_data)
df_combinations.index += 1
print(df_combinations)


# Question4: Publish tables in html file
# filtered table
df_combinations_filtered = df_combinations[df_combinations['Frequency'] > 100]
print(df_combinations_filtered)

# save tables in the html file
with open('output.html', 'w') as f:
    f.write(df.to_html(index=False, justify='center', border=0, classes='table table-striped'))
    f.write('<br><br>')
    f.write(df_combinations_filtered.to_html(index=False, justify='center', border=0, classes='table table-striped'))