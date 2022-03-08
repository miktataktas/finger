import random
from os import listdir
from os.path import isfile, join
import os
import shutil
import glob


mypath='''H:\Görevler\Shell_Derince\Derince 4.Tır-GTI2022..001\el-2'''
target='''H:\Görevler\Toyota\el-2'''
ext='.jpg'
files=glob.glob(mypath+'**/*'+ext)

choices = []
x=0
while x<310:
    selection = random.choice(files)
    if selection not in choices:
        choices.append(selection)
        x=x+1    
for i in choices:
    shutil.copy(i, target+'\\'+os.path.basename(i))

    
    
    
    
