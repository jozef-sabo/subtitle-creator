import os

config = {
    "LINE_LENGTH": 46,
    "ACCEPTED_DIFFERENCE": 20
}


def welcome_screen():
    print("""
 _____       _     _   _ _   _           
/  ___|     | |   | | (_) | | |          
\ `--. _   _| |__ | |_ _| |_| | ___ _ __ 
 `--. \ | | | '_ \| __| | __| |/ _ \ '__|
/\__/ / |_| | |_) | |_| | |_| |  __/ |   
\____/ \__,_|_.__/ \__|_|\__|_|\___|_|   
        Created by Jozef Sabo
""")


def options_screen():
    print("What do yout want to do?\n"
          "1    | Create subtitles\n"
          "2    | Check subtitles compatibility\n"
          "3    | Translate subtitles to text\n"
          "4    | Edit config\n"
          "5    | End the program")


def show_subtitle_in_list(line_number: int, subs_list: list, selector: int, number_of_showed_lines: int = 10) -> int:
    starting_line = max(0, line_number - number_of_showed_lines // 2)
    ending_line = min(len(subs_list), line_number + number_of_showed_lines // 2)

    for line_order in range(starting_line, ending_line):
        if line_order == selector - 1:
            print(">", end="")
        print(f"{str(line_order + 1).zfill(4)} | {subs_list[line_order]}")
    selection = input("Select line number or +/- to go up/down: ").strip()

    if selection == "+":
        selection = show_subtitle_in_list(line_number + number_of_showed_lines // 2, subs_list, selector)
    if selection == "-":
        selection = show_subtitle_in_list(line_number - number_of_showed_lines // 2, subs_list, selector)

    return int(selection)


def splitter(helper_list: list):
    pos_dot = 0
    pos_comma = 0
    pos_space = 0
    for pos in range(config["LINE_LENGTH"] - 1, -1, -1):
        if helper_list[-1][pos] in [".", "!", "?"]:
            pos_dot = pos
            break

    for pos in range(config["LINE_LENGTH"] - 1, -1, -1):
        if helper_list[-1][pos] in [",", ":"]:
            pos_comma = pos
            break

    for pos in range(config["LINE_LENGTH"] - 1, -1, -1):
        if helper_list[-1][pos] == " ":
            pos_space = pos
            break

    pos = config["LINE_LENGTH"]

    if pos_dot:
        pos = pos_dot

    if pos_comma:
        pos = pos_dot
        if pos_dot + config["ACCEPTED_DIFFERENCE"] < pos_comma:
            pos = pos_comma

    if pos_space:
        if pos + config["ACCEPTED_DIFFERENCE"] < pos_space:
            pos = pos_space

    text = helper_list[-1]
    helper_list[-1] = text[:pos + 1]
    helper_list.append(text[pos + 1:].strip())
    return helper_list


def create_subtitles():
    subtitle_menus = [
        "1    | Run\n2    | Configure",
        "1    | Remove first lines\n2    | Remove last lines\n3    | Remove name in replica\n4    | Remove empty "
        "lines\n5    | Renumber only"
    ]

    path_to_file = input("Enter the path to file: ")
    while not os.path.isfile(path_to_file):
        path_to_file = input("Enter the path to file: ")

    with open(path_to_file, "rt") as sub_file:
        file_lines = [x.strip() for x in sub_file.readlines()]

    remove_first = 0
    remove_last = 0
    remove_name_in_replica = False
    remove_empty_lines = False
    renumber = False

    print(subtitle_menus[0])
    option = int(input("Select the number: "))
    while option != 1:
        if option == 2:
            print(subtitle_menus[1])
            option = int(input("Select the option: "))

            if option == 1:
                remove_first = show_subtitle_in_list(remove_first, file_lines, remove_first + 1) - 1

            if option == 2:
                remove_last = len(file_lines) - (show_subtitle_in_list(len(file_lines) - remove_last, file_lines,
                                                                       len(file_lines) - remove_last) - 1) - 1

            if option == 3:
                remove_name_in_replica = not remove_name_in_replica
                print(f"Remove names in replica was set to {remove_name_in_replica}")

            if option == 4:
                remove_empty_lines = not remove_empty_lines
                print(f"Remove names in replica was set to {remove_empty_lines}")

            if option == 5:
                renumber = not renumber
                print(f"Renumber was set to {renumber}")

        print(subtitle_menus[0])
        option = int(input("Select the option: "))

    path = os.path.dirname(path_to_file)
    filename = os.path.basename(path_to_file).replace(".txt", ".srt")

    if renumber:
        with open(os.path.join(path, filename), "w+", encoding="ansi") as output_file:
            while not file_lines[0]:
                file_lines.pop(0)

            if not file_lines:
                return
            line_counter = 1
            if file_lines[0].isnumeric():
                file_lines[0] = line_counter

            output_file.write(f"{file_lines[0]}\n")

            for line_index in range(1, len(file_lines)):
                if not file_lines[line_index - 1] and file_lines[line_index].isnumeric():
                    line_counter += 1
                    file_lines[line_index] = line_counter
                output_file.write(f"{file_lines[line_index]}\n")
            output_file.write("\n")
        return

    offset = -remove_first
    with open(os.path.join(path, filename), "w+", encoding="ansi") as output_file:
        for line_number in range(remove_first, len(file_lines) - remove_last):
            if remove_name_in_replica:
                if file_lines[line_number].isupper():
                    file_lines[line_number] = ""

                list_to_remove = file_lines[line_number].split(":")
                if len(list_to_remove) > 1:
                    list_to_remove.pop(0)

                file_lines[line_number] = ":".join(list_to_remove).strip()

            if remove_empty_lines:
                if not file_lines[line_number]:
                    offset -= 1
                    continue

            helper_list = [file_lines[line_number]]
            while len(helper_list[-1]) > config["LINE_LENGTH"]:
                helper_list = splitter(helper_list)

            offset -= 1
            for splitted_line_num in range((len(helper_list) - 1)//2 + 1):
                offset += 1
                line_number_offset = line_number + offset
                sec = str(line_number_offset % 60).zfill(2)
                minute = line_number_offset // 60
                hour = str(minute // 60).zfill(2)
                minute = str(minute % 60).zfill(2)

                opening_time = f"{hour}:{minute}:{sec},000"
                closing_time = f"{hour}:{minute}:{sec},999"

                output_file.write(f"{line_number_offset + 1}\n")
                output_file.write(f"{opening_time} --> {closing_time}\n")
                output_file.write(f"{helper_list[splitted_line_num * 2]}\n")
                if len(helper_list) > splitted_line_num * 2 + 1:
                    output_file.write(f"{helper_list[splitted_line_num * 2 + 1]}\n")
                output_file.write("\n")

    print()


def option_selector(option: int):
    if 0 > option or option > 4:
        print("Select the number between 1 and 5")
        return

    if option == 1:
        create_subtitles()


def run_worker():
    option = int(input("Select the number: "))
    print()
    while option != 5:
        option_selector(option)

        options_screen()
        option = int(input("Select the number: "))
        print()


if __name__ == '__main__':
    welcome_screen()
    options_screen()
    run_worker()
