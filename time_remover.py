with open(input("Input file: "), "r", encoding="UTF-8") as input_file:
    lines = input_file.readlines()

lines_n = []
for line in lines:
    if not line.startswith("0"):
        lines_n.append(line)

with open(input("Output file: "), "w+", encoding="UTF-8") as output_file:
    output_file.writelines(lines_n)
