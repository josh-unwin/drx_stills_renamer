# TODO:
# 1. Add a confirmation before renaming?
# 2.

from os import listdir, rename
from os.path import isfile, isdir, join, splitext, exists, dirname, basename
import sys
from bs4 import BeautifulSoup
from timecode import Timecode


ACCEPTED_FILES = [".dpx", ".jpx", ".drx", ".png", ".tif"]


def main():
    filelist = args_parser_get_file_list()
    roll_list = {}
    drx_count = 0

    if filelist["folderpath"] is not None:
        for file in filelist["files"]:
            if get_file_extension(file) == ".drx":
                file_data = extract_file_data_from_drx(join(filelist["folderpath"], file))
                new_filename = format_filename(file_data)
                rename_files(filelist["folderpath"], filelist["files"], file, new_filename)
                add_to_roll_list(new_filename, roll_list)
                print(roll_list)
                add_to_edl(new_filename, file_data, roll_list)
                drx_count += 1
        save_edl_files(roll_list, filelist["folderpath"])
        quit_program(f"Finished! Renamed {drx_count} images, created {len(roll_list.keys())} stills EDLs")
    else:
        quit_program("An error occurred when parsing arguments.")


def args_parser_get_file_list():
    filelist = {
        "folderpath": None,
        "files": []
    }

    if len(sys.argv) == 2:
        if isdir(sys.argv[1]):
            filelist["folderpath"] = sys.argv[1]
            filelist["files"] = get_file_list_from_folder(filelist["folderpath"])
        else:
            quit_program("Argument was not a single folder or list of files")
    elif len(sys.argv) > 2:
        for i, argument in enumerate(sys.argv[1:], start=1):
            if exists(argument) and get_file_extension(argument) in ACCEPTED_FILES:
                if i == 1: filelist["folderpath"] = dirname(argument)
                if dirname(argument) == filelist["folderpath"]:
                    filelist["files"].append(basename(argument))
                else:
                    quit_program("All files must be in come from the same folder! Quitting...")
            else:
                quit_program("At least one file is invalid. Ensure files exist and are one of the following: "
                             + ', '.join(ACCEPTED_FILES)
                             )
    else:
        quit_program("No arguments provided. Quitting...")

    print(filelist)
    return filelist


def quit_program(message):
    print(message)
    sys.exit()


def add_to_roll_list(filename, roll_list):
    if "NO_REELNAME" in filename and "NO_REELNAME" not in roll_list.keys():
        roll_list["NO_REELNAME"] = []
    elif filename[:4] not in roll_list.keys():
        roll_list[filename[:4]] = []


def save_edl_files(roll_list, folderpath):
    for roll, clips_list in roll_list.items():
        edl_header = f"TITLE: {roll}_STILLS_EDL.edl\nFCM: NON-DROP FRAME\n\n"
        f = open(f"{folderpath}/_{roll}_STILLS.edl", "w")
        f.write(edl_header)
        f.write(''.join(clips_list))
        f.close()


def add_to_edl(filename, data, roll_list):
    edl_clip_num = len(roll_list[filename[:4]]) + 1
    rec_out = Timecode('24', data['rec_tc']) + Timecode('24', '00:00:00:00')
    edl_entry = f"{edl_clip_num:03}  {filename} V     C        00:00:00:00 00:00:00:01 {data['rec_tc']} {rec_out}  \n"
    roll_list[filename[:4]].append(edl_entry)


def get_file_list_from_folder(folderpath):
    return [f for f in listdir(folderpath) if exists(join(folderpath, f)) and get_file_extension(f) in ACCEPTED_FILES]


def get_file_extension(filename):
    return splitext(filename)[1]


def get_file_name_without_extension(filename):
    return splitext(filename)[0]


def extract_file_data_from_drx(filepath):
    data = {}

    with open(filepath) as file:
        soup = BeautifulSoup(file, 'lxml')
        data["reelname"] = soup.reelname.string
        data["rec_tc"] = soup.rectc.string
        data["src_tc"] = soup.srctc.string

        return data


# Renames all files that have the same name as original_filename, with any extension.
def rename_files(folderpath, filelist, original_filename, new_filename):
    for file in filelist:
        if get_file_name_without_extension(file) == get_file_name_without_extension(original_filename):
            extension = get_file_extension(file)
            if extension in ACCEPTED_FILES:
                rename(join(folderpath, file), join(folderpath, new_filename + extension))


def format_filename(file_data):
    return f"{file_data['reelname']}___srctc_{file_data['src_tc'].replace(':', '-')}"


if __name__ == '__main__':
    main()
