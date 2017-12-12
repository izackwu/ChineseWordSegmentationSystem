# coding:utf-8
import os
import re

training_files = []
line_num = 0
all_characters_set = set()
init_status_dict = dict()
trans_dict = dict()
status_set = {"S", "B", "M", "E"}
status_count_dict = dict()
emit_dict = dict()


def add_training_file(filepath, open_folder=False):
    if os.path.isfile(filepath):
        if filepath in training_files:
            print("##{0} already exists".format(filepath))
        else:
            training_files.append(filepath)
            print("##Add {0} to training files.".format(filepath))
    elif os.path.isdir(filepath):
        if open_folder == False:
            option = input("Seems that it's a folder, so add all the files inside as training files?(y/n)\n")
            if option.lower() == "y":
                add_training_file(filepath, open_folder=True)
            else:
                print("Okay, we ignore this folder.")
        else:
            for path in os.listdir(filepath):
                add_training_file(os.path.join(filepath, path), open_folder=True)


def statistic(filepath):
    global line_num
    global all_characters_set
    global init_status_dict
    global trans_dict
    global status_set
    global status_count_dict
    global emit_dict
    with open(filepath, mode="r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            line_num += 1
            # line_characters_list = list(line.replace(" ", ""))
            line_characters_list = list(re.sub(r"[\s]{2,}", "", line))
            all_characters_set = all_characters_set | set(line_characters_list)
            line_word_list = re.split(r"[\s]{2,}", line)
            line_status_list = []
            for word in line_word_list:
                if len(word) == 1:
                    line_status_list.append("S")
                elif len(word) >= 2:
                    line_status_list.extend("B"+"M"*(len(word)-2)+"E")
            # print(line_characters_list, line_status_list, sep="\n")
            assert len(line_status_list) == len(line_characters_list), line
            length = len(line_status_list)
            for i in range(0, length):
                status = line_status_list[i]
                character = line_characters_list[i]
                status_count_dict[status] += 1
                if character in emit_dict[status].keys():
                    emit_dict[status][character] += 1
                else:
                    emit_dict[status][character] = 1
                if i == 0:
                    init_status_dict[status] += 1
                else:
                    trans_dict[line_status_list[i-1]][status] += 1


def save_training_result(folder="TrainingResult"):
    global line_num
    global all_characters_set
    global init_status_dict
    global trans_dict
    global status_set
    global status_count_dict
    global emit_dict
    folder = "TrainingResult" if not folder else folder
    if not os.path.isdir(folder):
        os.mkdir(folder)
    for status in status_set:
        init_status_dict[status] /= line_num
        for status2 in status_set:
            trans_dict[status][status2] /= status_count_dict[status]
        for character in emit_dict[status].keys():
            emit_dict[status][character] /= status_count_dict[status]
    file_list = ["InitStatus.data", "TransProbMatrix.data", "EmitProbMatrix.data"]
    data_list = [init_status_dict, trans_dict, emit_dict]
    try:
        for i in range(3):
            with open(os.path.join(folder, file_list[i]), mode="w", encoding="utf-8") as file:
                file.write(str(data_list[i]))
    except:
        print("Failed to write data into file.")
    else:
        print("##Success!")


def init():
    for status in status_set:
        init_status_dict[status] = 0
        trans_dict[status] = {s: 0 for s in status_set}
        status_count_dict[status] = 0
        emit_dict[status] = dict()


if __name__ == "__main__":
    init()
    #print(line_num, all_characters_set, init_status_dict, trans_dict, status_set, status_count_dict, emit_dict, sep="\n")
    while True:
        path = input("Please add training files: (Enter 0 to stop)\n")
        if path == "0":
            break
        elif os.path.exists(path):
            add_training_file(path)
        else:
            print("Can't find the file or folder!")
    if not training_files:
        print("No training file provided.")
        exit()
    for i, filepath in enumerate(training_files):
        print("##Start to handle {0}.".format(filepath))
        statistic(filepath)
        print("##{0} has been handled successfully.".format(filepath))
    #print(line_num, all_characters_set, init_status_dict, trans_dict, status_set, status_count_dict, emit_dict, sep="\n")
    save_folder = input("Done! Please enter in which folder to save the training results:")
    save_training_result(save_folder)
    #print(line_num, all_characters_set, init_status_dict, trans_dict, status_set, status_count_dict, emit_dict, sep="\n")
