from thresholding import cv2, np

def hist(img):
    bottom_half = img[img.shape[0] // 2:, :]
    return np.sum(bottom_half, axis=0)
    
class LaneLines:
    def __init__(self):
        self.left_fit = None
        self.right_fit = None
        self.binary = None
        self.nonzero = None
        self.nonzerox = None
        self.nonzeroy = None
        self.clear_visibility = True
        self.dir = []
        self.nwindows = 9
        self.margin = 100
        self.minpix = 50

    def forward(self, img):
        self.extract_features(img)
        return self.fit_poly(img)

    def pixels_in_window(self, center, margin, height):
        topleft = (center[0] - margin, center[1] - height // 2)
        bottomright = (center[0] + margin, center[1] + height // 2)

        condx = (topleft[0] <= self.nonzerox) & (self.nonzerox <= bottomright[0])
        condy = (topleft[1] <= self.nonzeroy) & (self.nonzeroy <= bottomright[1])
        return self.nonzerox[condx & condy], self.nonzeroy[condx & condy]

    def extract_features(self, img):
        self.img = img
        self.window_height = np.int32(img.shape[0] // self.nwindows)
        self.nonzero = img.nonzero()
        self.nonzerox = np.array(self.nonzero[1])
        self.nonzeroy = np.array(self.nonzero[0])

    def find_lane_pixels(self, img):
        assert (len(img.shape) == 2)
        out_img = np.dstack((img, img, img))
        histogram = hist(img)
        midpoint = histogram.shape[0] // 2
        leftx_base = np.argmax(histogram[:midpoint])
        rightx_base = np.argmax(histogram[midpoint:]) + midpoint
        leftx_current = leftx_base
        rightx_current = rightx_base
        y_current = img.shape[0] + self.window_height // 2
        leftx, lefty, rightx, righty = [], [], [], []
        for _ in range(self.nwindows):
            y_current -= self.window_height
            center_left = (leftx_current, y_current)
            center_right = (rightx_current, y_current)

            good_left_x, good_left_y = self.pixels_in_window(center_left, self.margin, self.window_height)
            good_right_x, good_right_y = self.pixels_in_window(center_right, self.margin, self.window_height)

            leftx.extend(good_left_x)
            lefty.extend(good_left_y)
            rightx.extend(good_right_x)
            righty.extend(good_right_y)

            if len(good_left_x) > self.minpix:
                leftx_current = np.int32(np.mean(good_left_x))
            if len(good_right_x) > self.minpix:
                rightx_current = np.int32(np.mean(good_right_x))

        return leftx, lefty, rightx, righty, out_img

    def fit_poly(self, img):
        leftx, lefty, rightx, righty, out_img = self.find_lane_pixels(img)

        if len(lefty) > 1500:
            self.left_fit = np.polyfit(lefty, leftx, 2)
        if len(righty) > 1500:
            self.right_fit = np.polyfit(righty, rightx, 2)

        maxy = img.shape[0] - 1
        miny = img.shape[0] // 3
        if len(lefty):
            miny = min(miny, np.min(lefty))

        if len(righty):
            miny = min(miny, np.min(righty))

        ploty = np.linspace(miny, maxy, img.shape[0])
        left_fitx = self.left_fit[0] * ploty ** 2 + self.left_fit[1] * ploty + self.left_fit[2]
        right_fitx = self.right_fit[0] * ploty ** 2 + self.right_fit[1] * ploty + self.right_fit[2]
        out_img1= np.copy(out_img)
        for i, y in enumerate(ploty):
            l = int(left_fitx[i])
            r = int(right_fitx[i])
            y = int(y)
            cv2.line(out_img, (l, y), (r, y), (0, 255, 0))
            cv2.line(out_img, (r, y), (r, y), (255, 0, 0),10)
            cv2.line(out_img, (l, y), (l, y), (255, 0, 0),10)
            cv2.line(out_img1, (r, y), (r, y), (255, 0, 0),5)
            cv2.line(out_img1, (l, y), (l, y), (255, 0, 0),5)

        lR, rR, pos = self.measure_curvature()

        return out_img, out_img1

        def plot(self, out_img):
        lR, rR, pos = self.measure_curvature()
        W = 400
        H = 300
        widget = np.copy(out_img[:H, :W])
        widget //= 2
        widget[0, :] = [0, 0, 255]
        widget[-1, :] = [0, 0, 255]
        widget[:, 0] = [0, 0, 255]
        widget[:, -1] = [0, 0, 255]
        out_img[:H, :W] = widget
        curvature_msg = "Curvature = {:.0f} m".format(min(lR, rR))
        cv2.putText(out_img, curvature_msg, org=(10, 100), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                        color=(255, 255, 255), thickness=2)

        cv2.putText(
            out_img,
            "Vehicle is {:.2f} m away from center".format(pos),
            org=(10, 200),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.66,
            color=(255, 255, 255),
            thickness=2)

        return out_img

    def measure_curvature(self):
        ym = 30 / 720
        xm = 3.7 / 700

        left_fit = self.left_fit.copy()
        right_fit = self.right_fit.copy()
        y_eval = 700 * ym
        left_curveR = ((1 + (2 * left_fit[0] * y_eval + left_fit[1]) ** 2) ** 1.5) / np.absolute(2 * left_fit[0])
        right_curveR = ((1 + (2 * right_fit[0] * y_eval + right_fit[1]) ** 2) ** 1.5) / np.absolute(2 * right_fit[0])

        xl = np.dot(self.left_fit, [700 ** 2, 700, 1])
        xr = np.dot(self.right_fit, [700 ** 2, 700, 1])
        pos = (1280 // 2 - (xl + xr) // 2) * xm
        return left_curveR, right_curveR, pos

    

