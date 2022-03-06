import os
import subprocess
from database import db

def size(filename):
    """Function to get message size that can be hidden
    in the text file.

    Args:
        filename (str): Name of the cover file

    Returns:
        str: Size of the message in byte string.
    """
    cmd = subprocess.Popen(['snow', '-S', filename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = cmd.communicate()
    return str(stdout, 'utf-8').split()[-2]


def encode(passwd, infile, coverfile, is_file = None, message = None):
    """Function to encode given message or text file in the
    specified text file


    Args:
        passwd (str): Password given
        infile (str): Name of text file to be hidden.
        coverfile (): File to hide the message in.
        is_file (bool, optional): Specifies if a file. Defaults to None.
        message (_type_, optional): If text message to be hidden. Defaults to None.
    """
    if message is not None:
        
        command = 'snow -C -Q -p "{}" -m "{}" {} {}'.format(passwd, message, infile, coverfile)
        os.system('cmd /c' + command)
        db.format_txt(coverfile, passwd)
    elif is_file is not None:
        
        command = 'snow -C -Q -p "{}" -f {} {} {}'.format(passwd, is_file, infile, coverfile)
        os.system('cmd /c' + command)
        db.format_txt(coverfile, passwd)


def decode(passwd, file):
    """Function to get hidden message from a file.

    Args:
        passwd (str): Password to decode the file.
        file (str): Name of the file containing the message.

    Returns:
        _type_: _description_
    """
    cmd = subprocess.Popen(['snow', '-C', '-p', passwd, file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = cmd.communicate()
    return str(stdout, 'utf-8')



