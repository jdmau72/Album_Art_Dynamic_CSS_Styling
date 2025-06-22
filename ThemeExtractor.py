import sys

#
#  Use k-means clustering to find the most-common colors in an image
#
import cv2
import numpy as np
from sklearn.cluster import KMeans

# These four functions sourced (and modified slightly) from Tim Poulsen: https://www.timpoulsen.com/2018/finding-the-dominant-colors-of-an-image.html
def make_histogram(cluster):
    """
    Count the number of pixels in each cluster
    :param: KMeans cluster
    :return: numpy histogram
    """
    numLabels = np.arange(0, len(np.unique(cluster.labels_)) + 1)
    hist, _ = np.histogram(cluster.labels_, bins=numLabels)
    hist = hist.astype('float32')
    hist /= hist.sum()
    return hist

def make_bar(height, width, color):
    """
    Create an image of a given color
    :param: height of the image
    :param: width of the image
    :param: BGR pixel values of the color
    :return: tuple of bar, rgb values, and hsv values
    """
    bar = np.zeros((height, width, 3), np.uint8)
    bar[:] = color
    red, green, blue = int(color[2]), int(color[1]), int(color[0])
    hsv_bar = cv2.cvtColor(bar, cv2.COLOR_BGR2HSV)
    hue, sat, val = hsv_bar[0][0]
    return bar, (red, green, blue), (hue, sat, val)

def sort_hsvs(hsv_list):
    """
    Sort the list of HSV values
    :param hsv_list: List of HSV tuples
    :return: List of indexes, sorted by hue, then saturation, then value
    """
    #changing to sort by saturation first
    # bars_with_indexes = []
    # for index, hsv_val in enumerate(hsv_list):
    #     bars_with_indexes.append((index, hsv_val[0], hsv_val[1], hsv_val[2]))
    # bars_with_indexes.sort(key=lambda elem: (elem[1], elem[2], elem[3]))
    # return [item[0] for item in bars_with_indexes]

    bars_with_indexes = []
    for index, hsv_val in enumerate(hsv_list):
        bars_with_indexes.append((index, hsv_val[0], hsv_val[1], hsv_val[2]))
    bars_with_indexes.sort(key=lambda elem: (elem[2], elem[1], elem[3]))
    return [item[0] for item in bars_with_indexes]

def findDominantColors(imgPath, n_colors):
    img = cv2.imread(imgPath)

    #blur the image
    img = cv2.bilateralFilter(img,9,75,75)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # img = cv2.GaussianBlur(img, (5,5),0)


    height, width, _ = np.shape(img)

    # reshape the image to be a simple list of RGB pixels
    image = img.reshape((height * width, 3))

    # we'll pick the 5 most common colors
    clusters = KMeans(n_clusters=n_colors, )
    clusters.fit(image)

    # count the dominant colors and put them in "buckets"
    histogram = make_histogram(clusters)
    # then sort them, most-common first
    combined = zip(histogram, clusters.cluster_centers_)
    combined = sorted(combined, key=lambda x: x[0], reverse=True)

    # finally, we'll output a graphic showing the colors in order
    bars = []
    hsv_values = []
    for index, rows in enumerate(combined):
        bar, rgb, hsv = make_bar(100, 100, rows[1])
        # print(f'Bar {index + 1}')
        # print(f'  RGB values: {rgb}')
        # print(f'  HSV values: {hsv}')
        hsv_values.append(hsv)
        bars.append(bar)

    # sort the bars[] list so that we can show the colored boxes sorted
    # by their HSV values -- sort by hue, then saturation
    sorted_bar_indexes = sort_hsvs(hsv_values)
    sorted_bars = [bars[idx] for idx in sorted_bar_indexes]
    # print(sorted_bars.index(0))

    # cv2.imshow('Img', img)
    # cv2.imshow('Sorted by HSV values', np.hstack(sorted_bars))
    # cv2.imshow(f'{n_colors} Most Common Colors', np.hstack(bars))
    # cv2.waitKey(0)

    # gets the two most major colors, then flips them (since OpenCV used gbr, but we want rgb)
    primaryColor = sorted_bars.pop()[0][0]
    secondaryColor = sorted_bars.pop(0)[0][0]

    # have to reverse into RGB format, and convert to ints
    colorA = [int(primaryColor[2]), int(primaryColor[1]), int(primaryColor[0])]
    colorB = [int(secondaryColor[2]), int(secondaryColor[1]), int(secondaryColor[0])]

    return (colorA, colorB)


# colorA, colorB = findDominantColors("static/img/front.jpg", 7)
# # # findDominantColors("joni1.jpg", 7)
# # # findDominantColors("joni2.jpg", 7)
# # # colorA, colorB = (findDominantColors("front.png", 7))
# print(colorA)
# print(colorB)
#
# sys.stdout.flush()