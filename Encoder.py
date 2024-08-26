import os
import cv2
import pywt
import numpy as np

path = input('Path for the image file: ')
out_txt = input('Save output file as: ')

key = int(input('Enter a Key: '))

rmvstg = input('Remove Steganography (y/n): ')


def invrotateMatrix(mat):
    if not len(mat):
        return

    top = 0
    bottom = len(mat) - 1

    left = 0
    right = len(mat[0]) - 1

    nmat = np.array([[[0, 0, 0] for _ in range(right + 1)] for _ in range(bottom + 1)])

    while left < right and top < bottom:

        prev = mat[top + 1][right]

        for i in range(right, left - 1, -1):
            curr = mat[top][i]
            nmat[top][i] = prev
            prev = curr

        top += 1

        for i in range(top, bottom + 1):
            curr = mat[i][left]
            nmat[i][left] = prev
            prev = curr

        left += 1

        for i in range(left, right + 1):
            curr = mat[bottom][i]
            nmat[bottom][i] = prev
            prev = curr

        bottom -= 1

        for i in range(bottom, top - 1, -1):
            curr = mat[i][right]
            nmat[i][right] = prev
            prev = curr

        right -= 1

        prev = mat[top + 1][left]

        for i in range(left, right + 1):
            curr = mat[top][i]
            nmat[top][i] = prev
            prev = curr

        top += 1

        for i in range(top, bottom + 1):
            curr = mat[i][right]
            nmat[i][right] = prev
            prev = curr

        right -= 1

        for i in range(right, left - 1, -1):
            curr = mat[bottom][i]
            nmat[bottom][i] = prev
            prev = curr

        bottom -= 1

        for i in range(bottom, top - 1, -1):
            curr = mat[i][left]
            nmat[i][left] = prev
            prev = curr

        left += 1

    return nmat


img = cv2.imread(path)
if rmvstg == 'y':
    image = img

    r_image = []
    g_image = []
    b_image = []
    for i in image:
        r_img = []
        g_img = []
        b_img = []
        for j in i:
            r_img.append(j[0])
            g_img.append(j[1])
            b_img.append(j[2])
        r_image.append(r_img)
        b_image.append(b_img)
        g_image.append(g_img)

    coeffs = pywt.dwt2(r_image, 'db2')

    approximation = coeffs[0]

    details = coeffs[1]

    approximation_no_stegano = approximation
    details_no_stegano = [np.zeros_like(c) for c in details]

    r_no_stegano = pywt.idwt2((approximation_no_stegano, details_no_stegano), 'db2')

    coeffs = pywt.dwt2(g_image, 'db2')

    approximation = coeffs[0]

    details = coeffs[1]

    approximation_no_stegano = approximation
    details_no_stegano = [np.zeros_like(c) for c in details]

    g_no_stegano = pywt.idwt2((approximation_no_stegano, details_no_stegano), 'db2')

    coeffs = pywt.dwt2(b_image, 'db5')

    approximation = coeffs[0]

    details = coeffs[1]

    approximation_no_stegano = approximation
    details_no_stegano = [np.zeros_like(c) for c in details]

    b_no_stegano = pywt.idwt2((approximation_no_stegano, details_no_stegano), 'db5')

    image_no_stegano = []
    m = len(r_no_stegano[1])
    for i in range(len(r_no_stegano)):
        row = []
        for j in range(m):
            row.append([r_no_stegano[i][j], g_no_stegano[i][j], b_no_stegano[i][j]])
        image_no_stegano.append(row)

    image_no_stegano = np.array(image_no_stegano)
    ext = path.split('.')

    if ext[-1] == 'jpg':
        cv2.imwrite('temp.png', image_no_stegano)
        img = cv2.imread('temp.png')
        os.remove('temp.png')
    else:
        cv2.imwrite('temp.jpg', image_no_stegano)
        img = cv2.imread('temp.jpg')
        os.remove('temp.jpg')

for _ in range(key):
    img = invrotateMatrix(img)

dim = img.shape
w = dim[1]
h = dim[0]


def gilbert2d(width, height):
    if width >= height:
        yield from generate2d(0, 0, width, 0, 0, height)
    else:
        yield from generate2d(0, 0, 0, height, width, 0)


def sgn(x):
    return -1 if x < 0 else (1 if x > 0 else 0)


def generate2d(x, y, ax, ay, bx, by):
    w = abs(ax + ay)
    h = abs(bx + by)

    (dax, day) = (sgn(ax), sgn(ay))
    (dbx, dby) = (sgn(bx), sgn(by))

    if h == 1:
        for i in range(0, w):
            yield (x, y)
            (x, y) = (x + dax, y + day)
        return

    if w == 1:
        for i in range(0, h):
            yield (x, y)
            (x, y) = (x + dbx, y + dby)
        return

    (ax2, ay2) = (ax // 2, ay // 2)
    (bx2, by2) = (bx // 2, by // 2)

    w2 = abs(ax2 + ay2)
    h2 = abs(bx2 + by2)

    if 2 * w > 3 * h:
        if (w2 % 2) and (w > 2):
            (ax2, ay2) = (ax2 + dax, ay2 + day)

        yield from generate2d(x, y, ax2, ay2, bx, by)
        yield from generate2d(x + ax2, y + ay2, ax - ax2, ay - ay2, bx, by)

    else:
        if (h2 % 2) and (h > 2):
            (bx2, by2) = (bx2 + dbx, by2 + dby)

        yield from generate2d(x, y, bx2, by2, ax2, ay2)
        yield from generate2d(x + bx2, y + by2, ax, ay, bx - bx2, by - by2)
        yield from generate2d(x + (ax - dax) + (bx2 - dbx), y + (ay - day) + (by2 - dby),
                              -bx2, -by2, -(ax - ax2), -(ay - ay2))


points = []
for x, y in gilbert2d(width=w, height=h):
    points.append([x, y])

hib_ord = []
for x, y in points:
    hib_ord.append(img[y][x])

text = []
for i in range(len(hib_ord)):
    for j in range(3):
        text.append(chr(hib_ord[i][j]))

txt = "".join(text)

with open(out_txt, 'w', encoding="utf-8") as f:
    f.write(txt)

print('Width: ', w)
print('Height: ', h)

print('Key: ', key)
