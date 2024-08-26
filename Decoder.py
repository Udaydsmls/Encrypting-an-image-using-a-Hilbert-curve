import cv2
import numpy as np

w = int(input('Width of the Image:'))
h = int(input('Height of the Image:'))

key = int(input('Enter the Key: '))

path = input('Path for the txt file: ')

out_img = input('Save output file as: ')


def invaltrotateMatrix(mat):
    if not len(mat):
        return

    top = 0
    bottom = len(mat) - 1

    left = 0
    right = len(mat[0]) - 1

    nmat = np.array([[[0, 0, 0] for _ in range(right + 1)] for _ in range(bottom + 1)])

    while left < right and top < bottom:

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

    return nmat


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

with open(path, "r", encoding="utf-8") as myfile:
    data = myfile.read()

order = []

for i in data:
    order.append(ord(i))

order = np.array(order)

pix = order.reshape(-1, 3)

img = [[0 for i in range(w)] for j in range(h)]

for i in range(len(points)):
    x, y = points[i]
    img[y][x] = pix[i]

image = np.array(img)

for _ in range(key):
    image = invaltrotateMatrix(image)

cv2.imwrite(out_img, image)
