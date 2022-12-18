import os
import shutil
import win32timezone
from kivy.lang import Builder
from kivy.app import App


class TestApp(App):

    def orders(self):
        path = self.root.ids['txtinput'].text
        list_group = os.listdir(path)
        os.mkdir(path + '/' + '000')
        for group in list_group:
            path1 = path + '/' + group
            lst = group.split('_')
            ds = lst[0]
            gr = lst[1]
            self.ds_with_sizefolder(path1, ds, gr)
        self.root.ids['txtinput'].text = self.root.ids['txtinput'].text + '\\000'

    def ds_with_sizefolder(self, path, ds, group):
        pathfolder = path + '/../000/' + ds
        if not os.path.isdir(pathfolder):
            os.mkdir(pathfolder)
        pathfolder = pathfolder + '/' + group
        if not os.path.isdir(pathfolder):
            os.mkdir(pathfolder)
        list_group = os.listdir(path)
        for size in list_group:
            if '.txt' not in size:
                lst_size = size.split('x')
                width = str(lst_size[0])
                height = str(lst_size[1])
                count = str(lst_size[2])
                self.replace_folder_with_photo(path + '/' + size, width, height, count, ds, group)

    # копирование фоток из папок размеров с фотками
    def replace_folder_with_photo(self, path, width, height, count, ds, group):
        folder = width + 'x' + height
        pathfolder = path + '/../../000/' + ds + '/' + group + '/' + folder
        if not os.path.isdir(pathfolder):
            os.mkdir(pathfolder)
        list_photo = os.listdir(path)
        for photo in list_photo:
            photo = path + '/' + photo
            for i in range(1, int(count) + 1):
                os.rename(photo, photo[:-4] + '___' + str(i) + '.jpg')
                photo = photo[:-4] + '___' + str(i) + '.jpg'
                shutil.copy2(photo, pathfolder)
                os.rename(photo, photo[:-8] + '.jpg')
                photo = photo[:-8] + '.jpg'

    def count_photos(self):
        result = ''
        way = self.root.ids['txtinput'].text
        lst = os.listdir(way)
        for ds in lst:
            result = result + ds + '\n' + '---------------------' + '\n' + self.count_photo(way + '\\' + ds) + '\n\n\n'
        self.root.ids['txtcount'].text = result

    def count_photo(self, way):
        dic = {}
        # way = self.root.ids['txtinput'].text
        for dirpath, dirnames, filenames in os.walk(way):
            for filename in filenames:
                photo = os.path.join(dirpath, filename)
                if photo[-4:].lower() == '.jpg':
                    lst = photo.split('\\')
                    folders = lst[-2]
                    if folders not in dic:
                        dic[folders] = 1
                    else:
                        dic[folders] = dic[folders] + 1

        s = []
        for key, values in dic.items():
            s.append(key + '\t' + str(values))
        s.sort()
        res = '\n'.join(s)
        return res


TestApp().run()

