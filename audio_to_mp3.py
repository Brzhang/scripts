#!/usr/bin/python
# -*- coding: utf-8 -*-


from subprocess import call             # for calling mplayer and lame
import sys                              # allows user to specify input and output directories
import os                               # help with file handling


def check_file_exists(directory, filename, extension):
    path = directory + "/" + filename + extension
    return os.path.isfile(path)


def convert_audio_to_mp3(in_dir, out_dir):
    try:
        # check specified folders exist
        if not os.path.exists(in_dir):
            exit("Error: Input directory \'" + in_dir + "\' does not exist. (try prepending './')")
        if not os.path.exists(out_dir):
            exit("Error: Output directory \'" + out_dir + "\' does not exist.")
        if not os.access(out_dir, os.W_OK):
            exit("Error: Output directory \'" + out_dir + "\' is not writeable.")

        print("[{0} audio files] --> [{1} mp3 format file]".format(in_dir, out_dir))

        # get a list of all convertible files in the input directory
        file_list = [os.path.join(root[len(in_dir):], file) for root, dirs, files in os.walk(in_dir)
                     for file in files]
        '''for root, dirs, files in os.walk(in_dir):
            for file in files:
                if file.endswith(".mp3"):
                    file_list.append(os.path.join(root, file))'''
        # remove files that have already been outputted from the list
        file_list[:] = [f for f in file_list if not check_file_exists(out_dir, os.path.splitext(f)[0], ".mp3")]
    except OSError as e:
        exit(e)
    
    if len(file_list) == 0:
        exit("Could not find any files needs to convert.")

    # convert all unconverted files
    for filename in file_list:
        print("-- converting {0}{2} to {1}{2} --".format(in_dir, out_dir, filename))
        call(['ffmpeg', '-i', in_dir + '/' + filename,
             out_dir + '/' + os.path.splitext(filename)[0] + '.mp3'])


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print('You must enter the file path')
        exit(1)

    # if only input directory is set, make the output directory the same
    input_dir = sys.argv[1]
    output_dir = sys.argv[1]
    if len(sys.argv) == 3:
        output_dir = sys.argv[2]
    convert_audio_to_mp3(input_dir, output_dir)
