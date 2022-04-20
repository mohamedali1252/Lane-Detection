from thresholding import cv2, np

def perspective_transform():
    src = np.float32([(550, 460),  # top-left
                      (150, 720),  # bottom-left
                      (1200, 720),  # bottom-right
                      (770, 460)])  # top-right
    dst = np.float32([(100, 0),
                      (100, 720),
                      (1100, 720),
                      (1100, 0)])
    M = cv2.getPerspectiveTransform(src, dst)
    Minv = cv2.getPerspectiveTransform(dst, src)
    return M, Minv


def warp_perspective(img, imgsize, M):
    return cv2.warpPerspective(img, M, imgsize, cv2.INTER_LINEAR)