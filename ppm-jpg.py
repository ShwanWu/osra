import os
import pandas as pd
from PIL import Image
import scipy.misc as misc
from scipy.misc import imread, imresize, imsave
from rdkit import Chem
from rdkit.Chem import Draw

# 执行：cmd命令,并返回cmd输出的结果
def execCmd(cmd):
    result = os.popen(cmd)
    text = result.read()
    return text

# 执行：将结果（SMILES）写入CSV文件
def writeFile(filename, data):
    f = open(filename, "w")
    f.write(data)
    f.close()

# 从PDF中解析出ppm图片,存在文件夹ppm文件夹中
# cmd: pdfimages ~/Documents/bitbucket/ppm-jpg/Michael_similar.pdf
#      ~/Documents/bitbucket/ppm-jpg/Michael_similar/image
def read_pdf_ppm(pdf_path, ppm_path):
    cmd1 = "pdfimages" + " " + pdf_path + " " + ppm_path
    os.system(cmd1)

# 把ppm转化为jpg格式,存在文件夹jpg文件夹中
def tansfer_ppm_jpg(n):
    for i in range(n):
        # i从0开始, j是一个三位数字
        if i < 10:     # 0-9 -> 000 - 009
            j = "00" + str(i)
        elif i < 100:  # 10-99 -> 010-099
            j = "0" + str(i)
        else:          # 100-599
            j = str(i)
        ppm_name = "Michael_similar/ppm/image-" + j + ".ppm"
        # save in current path and create a jpg file
        jpg_name = "Michael_similar/jpg/" + str(i) + ".jpg"
        img = Image.open(ppm_name)
        img.save(jpg_name)

def findStart(n):
    # 从起始点start_index开始找:
    start_list = []
    for i in range(0, n):
        jpg_name_this = "Michael_similar/jpg/" + str(i) + ".jpg"
        img_this = Image.open(jpg_name_this)
        if img_this.size != (36, 13):
            try:  # 加入该文件的上一个文件存在，那么判断该文件是不是start
                jpg_name_last = "Michael_similar/jpg/" + str(i-1) + ".jpg"
                img_last = Image.open(jpg_name_last)
                if img_last.size != (36, 13):
                    start_list.append(i)
            except Exception as e:  # 假如找不到上一文件因此产生异常，则该文件序号必然是start=0.
                start_list.append(i)
    return start_list

def findEnd(n):
    # 从起始点start_index开始找:
    # 最后一张图片没有next
    end_list = []
    for i in range(n):
        jpg_name_this = "Michael_similar/jpg/" + str(i) + ".jpg"
        img_this = Image.open(jpg_name_this)
        if img_this.size != (36, 13):
            try:
                jpg_name_next = "Michael_similar/jpg/" + str(i+1) + ".jpg"
                img_next = Image.open(jpg_name_next)
                if img_next.size != (36, 13):
                    end_list.append(i)
            except Exception as e:  # 假如找不到下一文件因此产生异常，则该文件序号必然是end=n.
                end_list.append(i)
    return end_list

def seperateRP(start_index, end_index):
    reactor_list = []
    product_list = []
    # 每一个反应的每一个图片
    arrow_index = 0
    for i in range(start_index, end_index): # 如i=[3, 8]
        try:
            # 找出反应箭头来区别反应物和产物
            jpg_name_last = "Michael_similar/jpg/" + str(i-1) + ".jpg"
            jpg_name_next = "Michael_similar/jpg/" + str(i+1) + ".jpg"
            img_last = Image.open(jpg_name_last)
            img_next = Image.open(jpg_name_next)
            if img_last.size != (36, 13) and img_next.size != (36, 13):
                arrow_index = i
        except Exception as e:
            pass
    # after find arrow, seperate reactants and products to 2 list
    for j in range(start_index, arrow_index):
        jpg_name = "Michael_similar/jpg/" + str(j) + ".jpg"
        img = Image.open(jpg_name)
        if img.size != (36, 13):
            cmd = "osra" + " " + path + jpg_name
            reactor_list.append(execCmd(cmd))
    for k in range(arrow_index, end_index + 1):
        jpg_name = "Michael_similar/jpg/" + str(k) + ".jpg"
        img = Image.open(jpg_name)
        if img.size != (36, 13):
            cmd = "osra" + " " + path + jpg_name
            product_list.append(execCmd(cmd))
    return reactor_list, product_list

def mergeData(n):
    start_list = findStart(600)
    end_list = findEnd(600)
    data = {'reactors': [], 'products': []}
    for i in range(len(end_list)):
        # 对每一个反应，分析出反应物和产物列表
        reactors, products = seperateRP(start_list[i], end_list[i])
        data['reactors'].append(reactors + (3 - len(reactors)) * [''])
        data['products'].append(products + (2 - len(products)) * [''])
    return data

# path = "~/Documents/bitbucket/ppm-jpg/"
# pdf_path = path + "Michael_similar.pdf"
# ppm_path = path + "Michael_similar/ppm/image"
# read_pdf_ppm(pdf_path, ppm_path)
# total_number = 600
# tansfer_ppm_jpg(total_number)
# print(findStart(total_number))
# print(findEnd(total_number))
# data = mergeData(total_number)
# print(pd.DataFrame(data))
# if __name__ =="__main__":
#
#     picture = '/home/ywu672/Desktop/21.jpg'
#
#
#     for ii in range(500):
#         commend_line = 'osra -r '
#         commend_line += str(ii*5)+ ' '
#
#         commend_line += picture
#
#         print(execCmd(commend_line))

# def plot_mol(smiles, legends, molsPerRow=5):
#     rd_mols = [Chem.MolFromSmiles(sm) for sm in smiles]
#     img = Draw.MolsToGridImage(rd_mols, molsPerRow=molsPerRow, subImgSize=(200, 200), legends=legends)
#     return img
#
I = imread("Michael_similar/jpg/" + str(23) + ".jpg")
help(misc.imread)
resize_image = misc.imresize(I, [224, 224], interp='lanczos')
imsave("Michael_similar/" + str(23) + ".jpg", resize_image,)
commend_line = 'osra '
commend_line += '~/Documents/bitbucket/ppm-jpg/'
commend_line += "Michael_similar/" + str(23) + ".jpg"
smiles = execCmd(commend_line)
print (smiles)

mol = Chem.MolFromSmiles(smiles)
print (mol)
plot_mol(['CCCC[N](=C)C(=CC(=C)C)C'], [" "])
