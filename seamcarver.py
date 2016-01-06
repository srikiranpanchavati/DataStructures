__author__ = 'Kiran'
from pylab import imread
from pylab import np
from pylab import inf
from pylab import figure
from pylab import subplot
from pylab import title
from pylab import imshow
from pylab import show
from skimage import img_as_float
from skimage import filters
from numpy import delete


def dual_gradient_energy(img):
    """
    calculates the gradient energy of each pixel of an image
    :param img: the image for which the gradient energy is to be calculated
    :return: the gradient energy of each pixel of the image.
    >>> img_test = np.array([[[ 0.77254903,  0.72941178,  0.79215688]]])
    >>> dual_gradient_energy(img_test)
    array([[ 0.]])
    """

    r = img[:, :, 0]
    g = img[:, :, 1]
    b = img[:, :, 2]

    r_h = filters.sobel_h(r)
    g_h = filters.sobel_h(g)
    b_h = filters.sobel_h(b)

    r_v = filters.sobel_v(r)
    g_v = filters.sobel_v(g)
    b_v = filters.sobel_v(b)

    sum_rg_h = np.add(np.square(r_h), np.square(g_h))
    sum_h = np.add(sum_rg_h, np.square(b_h))

    sum_rg_v = np.add(np.square(r_v), np.square(g_v))
    sum_v = np.add(sum_rg_v, np.square(b_v))

    energy = np.add(sum_h, sum_v)
    return energy


def find_seam(img):
    """
    Calculates column index of seam for each row.
    :param img: image for which the seam is to calculated.
    :return: array of seam column.
    >>> img = np.array([[  0.00000000e+00,   5.98615846e-03,   5.90734263e-03],[ 9.22721920e-05, 0.00000000e+00,   5.76701200e-05],[  0.00000000e+00,   1.75509399e-03,   1.73779295e-03],[  9.80392040e-05, 2.30680480e-05,   0.00000000e+00]])
    >>> find_seam(img)
    [0, 0, 2, 1]
    """
    row_length = len(img)
    column_length = len(img[0])
    direction = [[0 for i in range(0, column_length)] for j in range(0, row_length)]
    sum_energy = [[0.0 for i in range(0, column_length)] for j in range(0, row_length)]
    seam_path = []
    min_value = +inf
    index = 0

    for i in range(1, row_length):
        for j in range(1, column_length - 1):
            top_left = float(+inf)
            top_right = float(+inf)
            top_center = img[i - 1][j]

            if j == 1:
                top_right = img[i - 1][j + 1]
            elif j == (column_length - 2):
                top_left = img[i - 1][j - 1]
            else:
                top_right = img[i - 1][j + 1]
                top_left = img[i - 1][j - 1]

            sum_energy[i][j], direction[i][j] = lcs(top_left, top_center, top_right, i, j, img, sum_energy)

    for i in range(1, column_length - 1):
        energy_last_row_min = sum_energy[row_length - 1][i]
        if energy_last_row_min < min_value:
            min_value = energy_last_row_min
            index = i
    seam_path.insert(0, index)
    index = direction[row_length - 1][index]

    for i in range(row_length - 2, -1, -1):
        seam_path.insert(0, index)
        index = direction[i][index]
    return seam_path


def lcs(top_left, top_center, top_right, i, j, img, sum_energy):
    """
    calculates the seam values and path of the seam
    :param top_left: value of the top left element of current element in the ndarray.
    :param top_center: value of the top element of current element in the ndarray.
    :param top_right: value of the top right element of current element in the ndarray.
    :param i: row index
    :param j: column index
    :param img: image for which seam values has to be calculated
    :param sum_energy: weighted sum of the element in ndarray
    :return: returns weighted sum and corresponding column index
    >>> sum_energy = np.array([[0, 0, 0, 0],[1,2, 3, 4],[5, 6, 7, 8]])
    >>> img = np.array([[0, 0, 0, 0],[0.77254903, 0.72941178, 0.79215688, 0.77215688],[0.77254903, 0.72941178, 0.79215688, 0.77215688]])
    >>> top_left = 0.72941178
    >>> top_center = 0.79215688
    >>> top_right = 0.77215688
    >>> i = 2
    >>> j = 2
    >>> lcs(top_left, top_center, top_right, i, j, img, sum_energy)
    (2.7921568799999998, 1)
    """
    sum_e = 0.0
    dir_e = 0
    if i == 1:
        sum_e = img[i][j]
        dir_e = j
    else:
        if min(top_left, top_center, top_right) == top_left:
            sum_e = img[i][j] + sum_energy[i - 1][j - 1]
            dir_e = j - 1
        elif min(top_left, top_center, top_right) == top_center:
            sum_e = img[i][j] + sum_energy[i - 1][j]
            dir_e = j
        elif min(top_left, top_center, top_right) == top_right:
            sum_e = img[i][j] + sum_energy[i - 1][j + 1]
            dir_e = j + 1
    return sum_e, dir_e


def plot_seam(img, seam_path):
    """
    plots the seam path for an image.
    :param img: the image for which seam has to be plotted
    :param seam_path: the seam column array for the image.
    :return: image with plotted seam path.
    >>> img = np.array([[[ 0.77254903, 0.72941178, 0.79215688], [0.7354903, 0.7141178, 0.7215688]],[[0.77254903, 0.72941178, 0.79215688], [0.7354903, 0.7141178, 0.7215688]]])
    >>> seam_path = np.array([0, 1])
    >>> plot_seam(img, seam_path)
    array([[[ 1.        ,  0.        ,  0.        ],
            [ 0.7354903 ,  0.7141178 ,  0.7215688 ]],
    <BLANKLINE>
           [[ 0.77254903,  0.72941178,  0.79215688],
            [ 1.        ,  0.        ,  0.        ]]])
    """
    plot_color = [1, 0, 0]
    row_length = len(img)
    for i in range(0, row_length):
        img[i][seam_path[i]] = plot_color
    return img


def remove_seam(img, seam_path):
    """
    Removal of the seam carve to compress the image.
    :param img: Image for which seam carve has to be removed.
    :param seam_path: the seam column array.
    :return: returns compressed image after seam carve has been removed.
    >>> img = np.array([[[ 0.77254903, 0.72941178, 0.79215688], [0.7354903, 0.7141178, 0.7215688]],[[0.77254903, 0.72941178, 0.79215688], [0.7354903, 0.7141178, 0.7215688]]])
    >>> seam_path = np.array([0, 1])
    >>> remove_seam(img, seam_path)
    array([[[ 0.77254903,  0.72941178,  0.79215688]],
    <BLANKLINE>
           [[ 0.77254903,  0.72941178,  0.79215688]]])
    """

    for i in range(0, len(seam_path)):
        plot_index = seam_path[i]
        img[i, plot_index:len(img[0]) - 2, :] = img[i, plot_index + 1:len(img[0]) - 1, :]
    return delete(img, len(img[0]) - 1, 1)


def seam_carve(iterations, img_seam, img_transformed):
    """
    :param iterations: Number of times seam carving has to be performed.
    :param img_seam: Image on which seam path can be visualised.
    :param img_transformed: compressed image after seam carving
    :return: returns images with seam path and compressed image.
    >>> img_seam = np.array([[[ 0.77254903, 0.72941178, 0.79215688], [0.7354903, 0.7141178, 0.7215688]],[[0.77254903, 0.72941178, 0.79215688], [0.7354903, 0.7141178, 0.7215688]]])
    >>> img_transformed = np.array([[[ 0.77254903, 0.72941178, 0.79215688], [0.7354903, 0.7141178, 0.7215688]],[[0.77254903, 0.72941178, 0.79215688], [0.7354903, 0.7141178, 0.7215688]]])
    >>> seam_carve(1, img_seam, img_transformed)
    (array([[[ 1.       ,  0.       ,  0.       ],
            [ 0.7354903,  0.7141178,  0.7215688]],
    <BLANKLINE>
           [[ 1.       ,  0.       ,  0.       ],
            [ 0.7354903,  0.7141178,  0.7215688]]]), array([[[ 0.77254903,  0.72941178,  0.79215688]],
    <BLANKLINE>
           [[ 0.77254903,  0.72941178,  0.79215688]]]))
    """
    for i in range(0, iterations):
        energy = dual_gradient_energy(img_transformed)
        seam_path = find_seam(energy)

        img_seam = plot_seam(img_seam, seam_path)
        img_transformed = remove_seam(img_transformed, seam_path)
    return img_seam, img_transformed


def main():
    img = img_as_float(imread('HJoceanSmall.png'))
    img_seam_v = img_as_float(imread('HJoceanSmall.png'))
    img_transformed_v = img_as_float(imread('HJoceanSmall.png'))
    iterations = 20
    img_seam_v, img_transformed_v = seam_carve(iterations, img_seam_v, img_transformed_v)

    figure()

    subplot(221)
    imshow(img)
    title("1. Original")

    subplot(222)
    imshow(img_seam_v)
    title("2. Seam carved vertical")

    # Transposed Image

    img_seam_hv = img_transformed_v.transpose(1, 0, 2)
    img_transformed_hv = img_transformed_v.transpose(1, 0, 2)
    iterations = 20

    img_seam_hv, img_transformed_hv = seam_carve(iterations, img_seam_hv, img_transformed_hv)

    subplot(223)
    imshow(img_seam_hv.transpose(1, 0, 2))
    title("3. Seam carved horizontal")

    subplot(224)
    imshow(img_transformed_hv.transpose(1, 0, 2))
    title("4. Transformed Image")

    show()

if __name__ == '__main__':
    main()
    import doctest
    doctest.testmod()
