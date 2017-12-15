# coding:utf-8

from Training import add_file
import os
import re


testing_files = []
init_status_dict = dict()
trans_dict = dict()
status_set = {"S", "B", "M", "E"}
emit_dict = dict()


def init(folder="TrainingResult"):
    global init_status_dict
    global trans_dict
    global status_set
    global emit_dict
    if not folder:
        folder = "TrainingResult"
    file_list = ["InitStatus.data", "TransProbMatrix.data", "EmitProbMatrix.data"]
    data_list = [init_status_dict, trans_dict, emit_dict]
    for i in range(0, 3):
        try:
            with open(os.path.join(folder, file_list[i]), mode="r", encoding="utf-8") as file:
                data_list[i].update(eval(file.read()))
        except:
            print("Failed to load {0}.".format(file_list[i][:-5]))
            return False
        else:
            print("Load {0} successfully.".format(file_list[i][:-5]))
    return True


def segment_for_sentense(sentense):
    pass


def segment_for_file(filepath, save_path=None, sep="  "):
    global init_status_dict
    global trans_dict
    global status_set
    global emit_dict
    if not save_path:
        save_path = filepath+".result"
    with open(save_path, mode="w", encoding="utf-8", errors="ignore") as result_file:
        result_file.write("")
    with open(filepath, mode="r", encoding="utf-8", errors="ignore") as file:
        buffer = ""
        for line in file:
            raw_line = line
            line = line.strip()
            if not line:
                buffer += raw_line
                continue
            path = dict()
            v = [dict(), ]
            for status in status_set:
                v[0][status] = init_status_dict[status]*emit_dict[status].get(line[0], 0)
                path[status] = status
            length = len(line)
            #print(v, path, sep="\n")
            for i in range(1, length):
                v.append(dict())
                new_path = dict()
                for status in status_set:
                    prob, prev_status = max((v[i-1][prev_status]*trans_dict[prev_status][status]*emit_dict[status].get(line[i], 0),
                                             prev_status)
                                            for prev_status in status_set)

                    v[i][status] = prob
                    new_path[status] = path[prev_status]+status
                path = new_path
                #print(v[i], path, sep="\n")
            last_prob, last_status = max((v[length-1][status], status) for status in status_set)
            seg_line = ""
            # print(path[last_status])
            for i in range(length-1):
                if path[last_status][i] == "S" or path[last_status][i] == "E":
                    seg_line += (line[i]+sep)
                else:
                    seg_line += line[i]
            seg_line += line[length-1]
            buffer += (seg_line+"\n")
            if len(buffer) >= (1 << 10):
                with open(save_path, mode="a", encoding="utf-8", errors="ignore") as result_file:
                    result_file.write(buffer)
                buffer = ""
        if buffer:
            with open(save_path, mode="a", encoding="utf-8", errors="ignore") as result_file:
                result_file.write(buffer)
    return True


def cut_into_sentense(filepath):
    seperator_Chinese = r"！？，。：……；"
    seperator_English = r"!?,:;\n"
    seperator = seperator_Chinese+seperator_English
    sentenses = list()
    with open(filepath, mode="r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            sentenses.extend(s.strip() for s in re.findall(r".*?[{0}]+".format(seperator), line) if s.strip())
    return sentenses

if __name__ == '__main__':
    while True:
        folder = input("Please input the folder of training results:\n")
        #folder = "TrainingResult"
        if init(folder):
            break
    # print(init_status_dict)
    while True:
        path = input("Please add testing files: (Enter 0 to stop)\n")
        #path = "testing.utf8"
        if path == "0":
            break
        elif os.path.exists(path):
            add_file(path, testing_files)
        else:
            print("Can't find the file or folder!")
        # break
    if not testing_files:
        print("No testing file provided.")
        exit()
    for file in testing_files:
        print("##Start to handle {0}.".format(file))
        if segment_for_file(file):
            print("##{0} has been handled successfully.".format(file))
        else:
            print("##Failed to handle {0}.".format(file))
    print("Done!")
