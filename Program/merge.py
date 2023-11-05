import csv

def generate_boolean_table(n):
    # Generate all possible combinations for n-bits
    return [(bin(i)[2:]).zfill(n) for i in range(2**n)]

# Get the boolean table
table = generate_boolean_table(8)

# Write the table to a CSV file
with open('boolean_table.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for row in table:
        writer.writerow(list(row))

