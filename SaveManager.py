from menu import *
import xml.etree.ElementTree as ET


tree1 = ET.parse('saves/base.xml')
root1 = tree1.getroot()
saves = root1[0][0]


def load1(name):
    return name.text


def save1(name, data):
    name.text = data
    tree1.write('saves/base.xml')


class save:
    def __init__(self):
        self.SAVE = root1[0][0]
        self.tree = ET.parse('saves/' + self.SAVE.text)
        self.root = self.tree.getroot()

        self.curent_map = self.root[0][0]
        self.curent_entry = self.root[0][1]
        self.spawn_map = self.root[0][2]
        self.spawn_point = self.root[0][1]

        self.HP = self.root[1][0]
        self.MaxHP = self.root[1][1]

        self.DoubleJump = self.root[2][0]
        self.WallSlide = self.root[2][1]

    def load(self, name):
        return float(name.text)

    def save(self, name, data, file):
        name.text = str(data)
        self.tree.write('saves/' + file)
