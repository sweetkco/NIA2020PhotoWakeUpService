import argparse
import os

parser = argparse.ArgumentParser(description='Photo Wake Up')
parser.add_argument('--input_folder',type=str,default='./input_images', help='input images')
parser.add_argument('--save_folder',type=str,default='./results',help='results saved')

config = parser.parse_args(args=[])

print(config.input_folder)

class PhotoWakeUp(object):
    def __init__(self):
        self.input_lists = [list for list in os.listdir(config.input_folder)]


