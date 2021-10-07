from PIL import Image, ImageDraw
import glob
import os


files = glob.glob('C:Users/Ionut/Desktop/Memes/*.jpg')
files += glob.glob('C:Users/Ionut/Desktop/Memes/*.png')
watermark = Image.open('C:Users/Ionut/Desktop/clipart2569207.png').convert("RGBA")
width1, height1 = watermark.size
watermark = watermark.resize((int(width1/8), int(height1/8)), Image.ANTIALIAS)
margin = 60
i = 0

if not os.path.exists('D:/Watermarking/edited'):
    os.makedirs('D:/Watermarking/edited')

for file in files :
    image = Image.open(file).convert('RGBA')
    print(image.tostring())
    width, height = image.size
    #print(f'widht: {width}, height: {height}')
    position = (margin//2, height - margin)
    newImage = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    newImage.paste(image, (0, 0))
    newImage.paste(watermark, position, watermark)
    if i == 0 :
        newImage.show()
        break
    #newImage.save(f'edited/newImage{i}.png',format='PNG')
    i += 1
