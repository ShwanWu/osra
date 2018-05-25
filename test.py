from PIL import Image

jpg_name_last = "Michael_similar/jpg/" + str(0) + ".jpg"
img = Image.open(jpg_name_last)
print(img.size != (36, 13))
