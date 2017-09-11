# это задание про жанры фотографии - числа-характеристики кадра взяты около-с-потолка

class Photo:
    def __init__(self,name,aperture,exposure,iso):
        self.name = name
        self.aperture = aperture
        self.exposure = exposure
        self.iso = iso
        self.bnw = False
        self.to_delete = False
        self.sharpen = False
        
    def bnw_good(self):
        return False

    def is_bad(self):
        return False

    def not_sharp(self):
        return self.aperture <= 3.5


class Portrait(Photo):
    def bnw_good(self):
        return (self.iso < 400 and self.exposure > 0.001)

    def is_bad(self):
        return (self.iso > 800 or self.aperture > 4.0)


class Sport(Photo):
    def is_bad(self):
        return (self.exposure > 0.01 or self.aperture < 3.5)

    def not_sharp(self):
        return (self.exposure > 0.001 and self.exposure < 0.01)
        

class Landscape(Photo):
    def is_bad(self):
        return self.iso > 800


class DarkLandscape(Landscape):
    def bnw_good(self):
        return (self.iso < 200 and self.exposure < 0.001)


class Macro(Photo):
    def not_sharp(self):
        return True

    def is_bad(self):
        return self.aperture > 2.8


class Night(Photo):
    def is_bad(self):
        return self.exposure < 0.01 or self.iso < 800

    def not_sharp(self):
        return self.exposure > 0.03


class GiveMeAllPhotosNow(Photo): # класс с пропуском любой обработки
    def not_sharp(self):
        return False


class Editor:
    def __init__(self,photo):
        self.photo = photo

    def apply_bnw(self):
        if self.photo.bnw_good(): # тут проявляется полиморфизм
            self.photo.bnw = True
            print('photo "'+self.photo.name+'" is made black & white')

    def delete_photo(self):
        if self.photo.is_bad(): # тут проявляется полиморфизм
            self.photo.to_delete = True
            print('photo "'+self.photo.name+'" should be deleted')
            return True
        return False
        
    def sharpen(self):
        if self.photo.not_sharp: # тут проявляется полиморфизм
            self.photo.sharpen = True
            print('photo "'+self.photo.name+'" is sharpened')

    def edit(self):
        print('start editing photo "'+self.photo.name+'"')
        to_delete = self.delete_photo()
        if not to_delete:
            self.sharpen()
            self.apply_bnw()
        print()


if __name__ == '__main__':
    p1 = Portrait('1',1.8,0.01,100)
    e1 = Editor(p1)
    e1.edit()

    p2 = Sport('2',2.8,0.001,200)
    e2 = Editor(p2)
    e2.edit()

    p3 = Night('3',5.6,0.01,1600)
    e3 = Editor(p3)
    e3.edit() 

