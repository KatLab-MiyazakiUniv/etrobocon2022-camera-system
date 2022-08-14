import cv2
import numpy as np

def main():
    arr = np.array([[[1,1,1],[0,0,226]],
                    [[3,3,3],[4,4,4]]])
    arr2 = np.array([0,0,0])
    arr3 = np.array([255,255,255])
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            if np.all(arr[i,j] > arr2) and np.all(arr[i,j] < arr3) :
                print(arr[i,j])

def show_image(image):
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            print(image[i][j], end=" ")
        print()

def black_coordinate(image):
    data = np.array(image)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            # if data[]
            pass
    
def test1():
    path = "course_images/base_circle1.png"
    # 画像データの読み込み
    img = cv2.imread(path)
    print("img.shape", img.shape)
    # BGR色空間からHSV色空間への変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    print("hsv.shape", hsv.shape)

    print("hsv[0]", hsv[0,0])

def test2():
    arr = np.array([[[1,1,1],[0,0,226]],
                    [[3,3,3],[4,4,4]]])
    arr2 = np.array([1,1,1])

    print("arr[0,0] =", arr[0,0])
    print("arr2     =", arr2)
    if arr[0,0,0] == arr2[0] and arr[0,0,1] == arr2[1] and arr[0,0,2] == arr2[2]:
        print("ok")
    else :
        print("no")
    # if arr[0,0,0]


if __name__ == "__main__":
    # main()
    # test1()
    test2()
    print("終了")