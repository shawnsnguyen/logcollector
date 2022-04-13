import os

# static util that lists files under /var/log, excluding gz and bz2 compressed files (since the codecs arent loaded in this project)
def list_files(log_dir):
    file_list = [file for file in os.listdir(log_dir)
                     if os.path.isfile(os.path.join(log_dir, file)) and
                     not (file.endswith('.gz') or file.endswith('.bz2'))]
    return file_list
