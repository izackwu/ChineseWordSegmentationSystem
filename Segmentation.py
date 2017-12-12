# coding:utf-8

from Training import add_file
import os


testing_files = []
init_status_dict = dict()
trans_dict = dict()
status_set = {"S", "B", "M", "E"}
emit_dict = dict()


def init(folder):
    global init_status_dict
    global trans_dict
    global status_set
    global emit_dict
    file_list = ["InitStatus.data", "TransProbMatrix.data", "EmitProbMatrix.data"]
    data_list = [init_status_dict, trans_dict, emit_dict]
    for i in range(0, 3):
        try:
            with open(os.path.join(folder, file_list[i]), mode="r", encoding="utf-8") as file:
                data_list = eval(file.read())
        except:
            print("Failed to load {0}.".format(file_list[i][:-5]))
            return False
        else:
            print("Load {0} successfully.".format(file_list[i][:-5]))
    return True

if __name__ == '__main__':
    while True:
        folder = input("Please input the folder of training results:\n")
        if init(folder):
            break
    while True:
        path = input("Please add testing files: (Enter 0 to stop)\n")
        if path == "0":
            break
        elif os.path.exists(path):
            add_file(path, testing_files)
        else:
            print("Can't find the file or folder!")
    if not training_files:
        print("No testing file provided.")
        exit()
