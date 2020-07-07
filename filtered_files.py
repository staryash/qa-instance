# -*- coding: utf-8 -*-
import shutil
import os

URL_LIST_FILE = './noisy2hin2.txt'

# src_base_dir = './noisy_student_clips_1lk' not needed
dest_base_dir = './noisy2hin2/'

lines = open(URL_LIST_FILE).readlines()

for src_file in lines:
  dest_file = dest_base_dir + src_file.rstrip()
  print('src_file:', src_file, ', dest_file:', dest_file)
  os.makedirs(os.path.dirname(dest_file), exist_ok=True)
  shutil.copy(src_file.rstrip(), dest_file)