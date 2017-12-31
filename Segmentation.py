# coding:utf-8

from Training import add_file, cut_into_sentence
import os
import re


testing_files = []
init_status_dict = dict()
trans_dict = dict()
status_set = {"S", "B", "M", "E"}
emit_dict = dict()
lexicon = set()
max_length = 0
inited = False
INF = 1e-10


def init(folder="Result/sentence/sentence_TrainingResult/"):
    global init_status_dict
    global trans_dict
    global status_set
    global emit_dict
    global inited
    global lexicon
    global max_length
    if not folder:
        folder = "TrainingResult"
    file_list = ["InitStatus.data", "TransProbMatrix.data", "EmitProbMatrix.data", ]
    data_list = [init_status_dict, trans_dict, emit_dict]
    try:
        with open(os.path.join(folder, "Lexicon.data"), mode="r", encoding="utf-8") as file:
            max_length = int(file.readline())
            for line in file:
                lexicon.add(line.strip())
    except:
        print("Failed to load Lexicon.")
        return False
    else:
        print("Load Lexicon successfully.")
    for i in range(0, 3):
        try:
            with open(os.path.join(folder, file_list[i]), mode="r", encoding="utf-8") as file:
                data_list[i].update(eval(file.read()))
        except:
            print("Failed to load {0}.".format(file_list[i][:-5]))
            return False
        else:
            print("Load {0} successfully.".format(file_list[i][:-5]))
    inited = True
    return True


def segment_for_sentence_HMM(sentence, sep="  "):
    global inited
    assert inited, "Please run init() first!"
    path = dict()
    v = [dict(), ]
    for status in status_set:
        v[0][status] = init_status_dict[status]*emit_dict[status].get(sentence[0], 0)
        path[status] = status
    length = len(sentence)
    #print(v, path, sep="\n")
    for i in range(1, length):
        v.append(dict())
        new_path = dict()
        for status in status_set:
            prob, prev_status = max((v[i-1][prev_status]*trans_dict[prev_status][status]*emit_dict[status].get(sentence[i], INF),
                                     prev_status)
                                    for prev_status in status_set)

            v[i][status] = prob
            new_path[status] = path[prev_status]+status
        path = new_path
        #print(v[i], path, sep="\n")
    last_prob, last_status = max((v[length-1][status], status) for status in status_set)
    result = ""
    # print(path[last_status])
    for i in range(length):
        if path[last_status][i] == "S" or path[last_status][i] == "E":
            result += (sentence[i]+sep)
        else:
            result += sentence[i]
    return result


def segment_for_sentence(sentence, sep="  "):
    global inited
    global lexicon
    global max_length
    assert inited, "Please run init() first!"
    result_list = list()
    unknown_string = ""
    while sentence:
        #print("sentence:", sentence)
        current_max_length = min(max_length, len(sentence))
        find = ""
        for i in range(current_max_length, 1, -1):
            # print(sentence[:i])
            if sentence[:i] in lexicon:
                find = sentence[:i]
                #print("find:", sentence[:i])
                sentence = sentence[i:]
                break
        if not find:
            unknown_string = unknown_string + sentence[0]
            sentence = sentence[1:]
        elif unknown_string:
            #print([word for word in segment_for_sentence_HMM(unknown_string, sep).split(sep) if word.strip()])
            result_list.extend(word for word in segment_for_sentence_HMM(unknown_string, sep).split(sep) if word.strip())
            result_list.append(find)
            unknown_string = ""
        else:
            result_list.append(find)
    if unknown_string:
        result_list.extend(word for word in segment_for_sentence_HMM(unknown_string, sep).split(sep) if word.strip())
    return sep.join(result_list)+sep


def segment_for_text(text, sep="  ", mode="default"):
    text = text.replace("\r\n", "\n")
    lines = text.split("\n")
    # print(lines)
    result = ""
    for line in lines:
        sentences_or_line = cut_into_sentence(string=line+"\n") if mode == "sentence" else [line+"\n", ]
        # print(sentences_or_line)
        for sentence in sentences_or_line:
            sentence = sentence.strip()
            if not sentence:
                continue
            result += segment_for_sentence(sentence, sep=sep)
        result += "\n"
    return result


def segment_for_file(filepath, save_path=None, sep="  ", mode="default"):
    global init_status_dict
    global trans_dict
    global status_set
    global emit_dict
    global inited
    assert inited, "Please run init() first!"
    if not save_path:
        save_path = filepath+".result"
    with open(save_path, mode="w", encoding="utf-8", errors="ignore") as result_file:
        result_file.write("")
    with open(filepath, mode="r", encoding="utf-8", errors="ignore") as file:
        buffer = ""
        for real_line in file:
            sentences_or_line = cut_into_sentence(string=real_line) if mode == "sentence" else [real_line, ]
            for sentence in sentences_or_line:
                sentence = sentence.strip()
                result = segment_for_sentence(sentence, sep=sep)
                buffer += result
            buffer += "\n"
            if len(buffer) >= (1 << 10):
                with open(save_path, mode="a", encoding="utf-8", errors="ignore") as result_file:
                    result_file.write(buffer)
                buffer = ""
        if buffer:
            with open(save_path, mode="a", encoding="utf-8", errors="ignore") as result_file:
                result_file.write(buffer)
    return True


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
        if segment_for_file(file, mode="sentence"):
            print("##{0} has been handled successfully.".format(file))
        else:
            print("##Failed to handle {0}.".format(file))
    print("Done!")
