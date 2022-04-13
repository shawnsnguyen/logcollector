import os

from constants import LOG_DIR

# static util that lists files under /var/log, excluding gz and bz2 compressed files (since the codecs arent loaded in this project)
def list_files():
    file_list = [file for file in os.listdir(LOG_DIR)
                     if os.path.isfile(os.path.join(LOG_DIR, file)) and
                     not (file.endswith('.gz') or file.endswith('.bz2'))]
    return file_list