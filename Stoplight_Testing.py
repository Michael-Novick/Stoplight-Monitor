import cv2
import numpy as np
import imutils


class Stoplight:
    def __init__(self, vertices):
        self.vertices = vertices
        self.height = vertices[3, 0] - vertices[0, 0]
        self.width = vertices[3, 1] - vertices[2, 1]

    def find_stoplight_center(self):
        stoplight_center = np.mean(self.vertices[:, 1])
        return stoplight_center

    def redefine_position(self):  # Todo
        # write code (optical flow?) to redefine stoplight location
        vertices = None
        self.vertices = vertices
        return None


cap = cv2.VideoCapture('MOV_0002.AVI')
# can also identify computer port with incoming camera stream
height, width = cap.get(cv2.CAP_PROP_FRAME_HEIGHT), cap.get(cv2.CAP_PROP_FRAME_WIDTH)
screen_center = width / 2
left_bound = 0.5 * screen_center
right_bound = 1.5 * screen_center
stoplights = []
snip_height = height / 2
while cap.isOpened():  # does the video ever close?
    # read video frame & show on screen
    ret, frame = cap.read()  # ret should be true or 1, frame should be a 3D array?
    frame = frame[0:int(snip_height), int(left_bound):int(right_bound)]
    frame = imutils.resize(frame, width=800)
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # thresh = 200
    # frame = cv2.threshold(frame, thresh, 255, cv2.THRESH_BINARY)[1]
    # cv2.imshow("Black/White", frame)

    # blur image to help with edge detection
    # blurred = cv2.GaussianBlur(frame, (5, 5), 0)
    blurred = frame
    # cv2.imshow("Blurred", blurred)
    #
    lower_bound_red = (0, 0, 155)
    upper_bound_red = (150, 150, 255)
    red = cv2.inRange(blurred, lower_bound_red, upper_bound_red)

    lower_bound_green = (0, 100, 0)
    upper_bound_green = (20, 150, 20)
    green = cv2.inRange(blurred, lower_bound_green, upper_bound_green)
    filtered = red + green
    filtered = cv2.medianBlur(filtered, 5)
    filtered = cv2.Canny(filtered, 1, 254)
    cv2.imshow("Filtered", filtered)

    circles = cv2.HoughCircles(filtered, cv2.HOUGH_GRADIENT, 1, minDist=10, minRadius=2)
    # for circle in circles:
    #     cvRound(circles[i][0]), cvRound(circles[i][1]))
    #     radius = cvRound(circles[i][2])
    #     circle(img, center, 3, Scalar(0, 255, 0), -1, 8, 0)
    #     circle(img, center, radius, Scalar(0, 0, 255), 3, 8, 0)
    #
    # imshow("circles", img);


    output = frame.copy()

    image = frame
        # loop over the (x, y) coordinates and radius of the circles
    if circles is not None:
        circle = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circle:
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
            cv2.circle(output, (x, y), r, (0, 255, 0), 4)
            # cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

        # show the output image
        print(circles)
    cv2.imshow("output", output)

    #
    # input('press key to continue: ')
    # # identify edges & show on screen
    # edged = cv2.Canny(blurred, 30, 150)
    # cv2.imshow("Edged", edged)

    # perform full Hough Transform to identify lane lines
    # lines = cv2.HoughLines(edged, 1, np.pi / 180, 25)
    #
    # # define arrays for left and right lanes
    # rho_left = []
    # theta_left = []
    # rho_right = []
    # theta_right = []
    #
    # # ensure cv2.HoughLines found at least one line
    # if lines is not None:
    #
    #     # loop through all of the lines found by cv2.HoughLines
    #     for i in range(0, len(lines)):
    #
    #         # evaluate each row of cv2.HoughLines output 'lines'
    #         for rho, theta in lines[i]:
    #
    #             # collect left lanes
    #             # if theta < np.pi/2 and theta > np.pi/4:
    #             rho_left.append(rho)
    #             theta_left.append(theta)
    #
    #             # plot all lane lines for DEMO PURPOSES ONLY
    #             a = np.cos(theta); b = np.sin(theta)
    #             x0 = a * rho; y0 = b * rho
    #             x1 = int(x0 + 400 * (-b)); y1 = int(y0 + 400 * (a))
    #             x2 = int(x0 - 600 * (-b)); y2 = int(y0 - 600 * (a))
    #
    #             cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 1)
    #
    #             # collect right lanes
    #             # if theta > np.pi/2 and theta < 3*np.pi/4:
    #             rho_right.append(rho)
    #             theta_right.append(theta)
    #
    #             # plot all lane lines for DEMO PURPOSES ONLY
    #             a = np.cos(theta); b = np.sin(theta)
    #             x0 = a * rho; y0 = b * rho
    #             x1 = int(x0 + 400 * (-b)); y1 = int(y0 + 400 * (a))
    #             x2 = int(x0 - 600 * (-b)); y2 = int(y0 - 600 * (a))
    #             cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 1)
    #
    #
    # vertices = None  # identify vertices with processing and feature detection
    # for corners in vertices:
    #     if True:  # return to this function
    #         stoplights.append(Stoplight(corners))

    # press the q key to break out of video
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
