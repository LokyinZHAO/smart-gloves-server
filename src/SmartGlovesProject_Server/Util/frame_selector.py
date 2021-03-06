import numpy as np
from sklearn.preprocessing import minmax_scale


def select_frame(fourier_trans_matrix: np.ndarray, selection):
    frame = []
    for i in selection:
        frame.append(fourier_trans_matrix[i])
    frame = np.array(frame)
    frame_scale = minmax_scale(frame, feature_range=(0, 1), axis=1)
    return frame_scale


def select_frame_5(fourier_trans_matrix: np.ndarray):
    f_5 = select_frame(fourier_trans_matrix, selection=(118, 315, 512, 709, 906))
    for i in range(len(f_5)):
        for j in range(len(f_5[0])):
            f_5[i][j] *= 4
            f_5[i][j] = int(f_5[i][j])
            if f_5[i][j] == 4:
                f_5[i][j] = 3
    return f_5


def select_frame_8(fourier_trans_matrix: np.ndarray):
    return select_frame(fourier_trans_matrix, selection=(51, 182, 313, 444, 575, 706, 837, 968))
