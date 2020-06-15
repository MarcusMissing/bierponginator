from pathlib import Path
from ast import literal_eval
import os
import shutil


def label_img():
    paths = []
    mainlist_2 = []
    dataset = "bilder"
    paths.extend([str(p) for p in Path(dataset).rglob("*" + ".jpg")])

    with open('../resource/cup_placement.txt') as f:
        mainlist = [list(literal_eval(line)) for line in f]

    for label in mainlist:
        for ii in range(10):
            mainlist_2.append(label)

    for i, label in enumerate(mainlist_2):
        if os.path.exists("bilder_labeles/" + str(label)[1:-1].replace(", ", "")+ "/" + str(label)[1:-1].replace(", ",
                                                                                                               "") + ".9" + ".jpg"):
            print("bilder_labeles/" + str(label)[1:-1].replace(", ", "") + ".jpg")
            print("as: " + str(paths[i]))
        else:
            if i % 10 == 0:
                dest = "bilder_labeles/" + str(label)[1:-1].replace(", ", "") + "/" + str(label)[1:-1].replace(", ",
                                                                                                               "") + ".0" + ".jpg"
            if os.path.exists(dest):
                num = int(dest[-5]) + 1
                dest = "bilder_labeles/" + str(label)[1:-1].replace(", ", "") + "/" + str(label)[1:-1].replace(", ",
                                                                                                               "") + "." + str(
                    num) + ".jpg"
            path = paths[i]
            if os.path.exists("bilder_labeles/" + str(label)[1:-1].replace(", ", "")) is False:
                os.mkdir("bilder_labeles/" + str(label)[1:-1].replace(", ", ""))
            shutil.copy(path, dest)


if __name__ == '__main__':
    label_img()
