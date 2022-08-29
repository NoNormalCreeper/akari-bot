import math
import os
import re
import shutil
import zipfile

from PIL import Image, ImageFilter, ImageEnhance, ImageDraw

from core.logger import Logger


async def arcb30init():
    cache = os.path.abspath('./cache')
    assets_apk = os.path.abspath('./assets/arc.apk')
    if not os.path.exists(assets_apk):
        return False
    assets = os.path.abspath('./assets/arcaea')
    if os.path.exists(assets):
        shutil.rmtree(assets)
    os.mkdir(assets)
    if zipfile.is_zipfile(assets_apk):
        fz = zipfile.ZipFile(assets_apk, 'r')
        for file in fz.namelist():
            fz.extract(file, cache)
    copysongpath = f'{cache}/assets/songs'
    songdirs = os.listdir(copysongpath)
    jacket_output = os.path.abspath('./cache/jacket_output/')
    if not os.path.exists(jacket_output):
        os.makedirs(jacket_output)
    for file in songdirs:
        filename = os.path.abspath(f'{copysongpath}/{file}')
        Logger.debug(filename)
        if os.path.isdir(filename):
            file = re.sub('dl_', '', file)
            filename_base = f'{filename}/base.jpg'
            if os.path.exists(filename_base):
                shutil.copy(filename_base, f'{jacket_output}/{file}.jpg')
            filename_0 = f'{filename}/0.jpg'
            if os.path.exists(filename_0):
                shutil.copy(filename_0, f'{jacket_output}/{file}_0.jpg')
            filename_1 = f'{filename}/1.jpg'
            if os.path.exists(filename_1):
                shutil.copy(filename_1, f'{jacket_output}/{file}_1.jpg')
            filename_2 = f'{filename}/2.jpg'
            if os.path.exists(filename_2):
                shutil.copy(filename_2, f'{jacket_output}/{file}_2.jpg')
            filename_3 = f'{filename}/3.jpg'
            if os.path.exists(filename_3):
                shutil.copy(filename_3, f'{jacket_output}/{file}_3.jpg')

    shutil.copytree(jacket_output, f'{assets}/jacket')
    files = os.listdir(jacket_output)
    bluroutputpath = os.path.abspath('./cache/bluroutput')
    bluroutputpath_official = os.path.abspath('./cache/bluroutput_official')
    if not os.path.exists(bluroutputpath):
        os.makedirs(bluroutputpath)
    if not os.path.exists(bluroutputpath_official):
        os.makedirs(bluroutputpath_official)

    for file in files:
        img = Image.open(f'{jacket_output}/{file}')
        img2 = img.filter(ImageFilter.GaussianBlur(radius=2))
        downlight = ImageEnhance.Brightness(img2)
        d2 = downlight.enhance(0.65)
        if not os.path.exists(bluroutputpath):
            os.makedirs(bluroutputpath)
        d2.save(f'{bluroutputpath}/{file}')
        img3 = img.filter(ImageFilter.GaussianBlur(radius=40))
        downlight = ImageEnhance.Brightness(img3)
        d3 = downlight.enhance(0.65)
        if not os.path.exists(bluroutputpath_official):
            os.makedirs(bluroutputpath_official)
        d3.save(f'{bluroutputpath_official}/{file}')

    files = os.listdir(bluroutputpath)
    b30background_imgdir = f'{assets}/b30background_img'
    if not os.path.exists(b30background_imgdir):
        os.makedirs(b30background_imgdir)
    b30background_imgdir_official = f'{assets}/b30background_img_official'
    if not os.path.exists(b30background_imgdir_official):
        os.makedirs(b30background_imgdir_official)

    for file in files:
        img = Image.open(os.path.abspath(f'{bluroutputpath}/{file}'))
        img1 = img.resize((325, 325))
        img2 = img1.crop((0, 62, 325, 263))
        img2.save(os.path.abspath(f'{b30background_imgdir}/{file}'))
        img3 = Image.open(os.path.abspath(f'{bluroutputpath_official}/{file}'))
        img4 = img3.resize((325, 325))
        img5 = img4.crop((0, 62, 325, 263))
        img5.save(os.path.abspath(f'{b30background_imgdir_official}/{file}'))

    shutil.copytree(f'{cache}/assets/char', f'{assets}/char')
    shutil.copytree(f'{cache}/assets/Fonts', f'{assets}/Fonts')
    ratings = ['0', '1', '2', '3', '4', '5', '6', '7', 'off']
    os.mkdir(f'{assets}/ptt/')
    for rating in ratings:
        shutil.copy(
            f'{cache}/assets/img/rating_{rating}.png',
            f'{assets}/ptt/rating_{rating}.png',
        )


    worldimg = f'{cache}/assets/img/world'
    worldimglist = os.listdir(worldimg)
    os.mkdir(f'{assets}/world/')
    world_official = f'{assets}/world_official/'
    os.mkdir(world_official)
    for x in worldimglist:
        if x.find('_') == -1:
            shutil.copy(f'{cache}/assets/img/world/{x}', f'{assets}/world/{x}')
            imgw = Image.open(f'{cache}/assets/img/world/{x}')
            imgw1 = imgw.filter(ImageFilter.GaussianBlur(radius=40))
            imgw1.save(world_official + x)

    coordinate = {'left_top': [1070, 25], 'right_top': [1070, 25], 'right_bottom': [1070, 959],
                  'left_bottom': [134, 959]}
    rotate = Rotate(
        Image.open(f'{cache}/assets/img/scenery/bg_triangle.png'), coordinate
    )

    rotate.run().convert('RGBA').save(f'{assets}/triangle.png')
    cardoverlay = Image.open(os.path.abspath(f'{cache}/assets/layouts/mainmenu/card/card_overlay.png'))
    cropoverlay = cardoverlay.crop((56, 307, 971, 377))
    cropoverlay.save(os.path.abspath(f'{assets}/card_overlay.png'))
    difficult = ['0', '1', '2', '3']
    for ds in difficult:
        d = Image.open(os.path.abspath(f'{cache}/assets/img/cutoff_dia_{ds}.png'))
        cd = d.crop((0, 0, 47, 47))
        cd = cd.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
        cd.save(os.path.abspath(f'{assets}/{ds}.png'))

    return True


class Rotate(object):
    def __init__(self, image: Image.Image, coordinate):
        self.image = image.convert('RGBA')
        self.coordinate = coordinate
        self.xy = [tuple(self.coordinate[k]) for k in ['left_top', 'right_top', 'right_bottom', 'left_bottom']]
        self._mask = None
        self.image.putalpha(self.mask)

    @property
    def mask(self):
        if not self._mask:
            mask = Image.new('L', self.image.size, 0)
            draw = ImageDraw.Draw(mask, 'L')
            draw.polygon(self.xy, fill=255)
            self._mask = mask
        return self._mask

    def run(self):
        image = self.rotation_angle()
        box = image.getbbox()
        return image.crop(box)

    def rotation_angle(self):
        x1, y1 = self.xy[0]
        x2, y2 = self.xy[1]
        angle = self.angle([x1, y1, x2, y2], [0, 0, 10, 0]) * -1
        return self.image.rotate(angle, expand=True)

    def angle(self, v1, v2):
        dx1 = v1[2] - v1[0]
        dy1 = v1[3] - v1[1]
        dx2 = v2[2] - v2[0]
        dy2 = v2[3] - v2[1]
        angle1 = math.atan2(dy1, dx1)
        angle1 = int(angle1 * 180 / math.pi)
        angle2 = math.atan2(dy2, dx2)
        angle2 = int(angle2 * 180 / math.pi)
        if angle1 * angle2 >= 0:
            included_angle = abs(angle1 - angle2)
        else:
            included_angle = abs(angle1) + abs(angle2)
            if included_angle > 180:
                included_angle = 360 - included_angle
        return included_angle
