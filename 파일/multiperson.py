import cv2
import time
import math
import numpy as np
import argparse
import datetime
import serial
import threading
import pyrebase
from flask import *
import os

# print('serial ' + serial.__version__)

#파이어베이스 정보
config = {
    "apiKey": "AIzaSyAOksU2ogxblR2vUVczwffzmv-x15v2OJI",
    "authDomain": "casptone-a2cbe.firebaseapp.com",
    "databaseURL": "https://casptone-a2cbe-default-rtdb.firebaseio.com",
    "projectId": "casptone-a2cbe",
    "storageBucket": "casptone-a2cbe.appspot.com",
    "messagingSenderId": "247150714233",
    "appId": "1:247150714233:web:31b6a3fdcc9d5138c5e3a8",
    "serviceAccount": "C:\\Users\\User\\test\\serviceAccountKey.json"
}

#파이어베이스 연결
firebase = pyrebase.initialize_app(config)

storage = firebase.storage()

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('video.html') #html파일 이름 multiperson 이나 video


def gen():
    #PORT = 'COM7'
    #BaudRate = 9600

    #ARD = serial.Serial(PORT, BaudRate)

    parser = argparse.ArgumentParser(description='Run keypoint detection')
    parser.add_argument("--device", default="gpu", help="Device to inference on")
    args = parser.parse_args()

    protoFile = "C:\\project\\models\\coco\\pose_deploy_linevec.prototxt"
    weightsFile = "C:\\project\\models\\coco\\pose_iter_440000.caffemodel"
    nPoints = 18
    # COCO Output Format
    keypointsMapping = ['Nose', 'Neck', 'R-Sho', 'R-Elb', 'R-Wr', 'L-Sho', 'L-Elb', 'L-Wr', 'R-Hip', 'R-Knee', 'R-Ank',
                        'L-Hip', 'L-Knee', 'L-Ank', 'R-Eye', 'L-Eye', 'R-Ear', 'L-Ear']

    POSE_PAIRS = [[1, 2], [1, 5], [2, 3], [3, 4], [5, 6], [6, 7],
                  [1, 8], [8, 9], [9, 10], [1, 11], [11, 12], [12, 13],
                  [1, 0], [0, 14], [14, 16], [0, 15], [15, 17],
                  [2, 17], [5, 16]]

    mapIdx = [[31, 32], [39, 40], [33, 34], [35, 36], [41, 42], [43, 44],
              [19, 20], [21, 22], [23, 24], [25, 26], [27, 28], [29, 30],
              [47, 48], [49, 50], [53, 54], [51, 52], [55, 56],
              [37, 38], [45, 46]]

    colors = [[0, 100, 255], [0, 100, 255], [0, 255, 255], [0, 100, 255], [0, 255, 255], [0, 100, 255],
              [0, 255, 0], [255, 200, 100], [255, 0, 255], [0, 255, 0], [255, 200, 100], [255, 0, 255],
              [0, 0, 255], [255, 0, 0], [200, 200, 0], [255, 0, 0], [200, 200, 0], [0, 0, 0]]

    inWidth = 168
    inHeight = 168

    pre_Y = 0
    present_Y = 0

    threshold = 0.1
    input_source = 0
    cap = cv2.VideoCapture(input_source)
    hasFrame, frame = cap.read()
    vid_writer = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10,
                                 (frame.shape[1], frame.shape[0]))
    net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

    if args.device == "cpu":
        net.setPreferableBackend(cv2.dnn.DNN_TARGET_CPU)
        print("Using CPU device")
    elif args.device == "gpu":
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        print("Using GPU device")

    while cv2.waitKey(1) < 0:
        count = 0
        t = time.time()
        swtich_degree = False
        hasFrame, frame = cap.read()
        frameCopy = np.copy(frame)
        if not hasFrame:
            cv2.waitKey()
            break

        frameWidth = frame.shape[1]
        frameHeight = frame.shape[0]

        inpBlob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (inWidth, inHeight),
                                        (0, 0, 0), swapRB=False, crop=False)
        net.setInput(inpBlob)
        output = net.forward()  # make a prediction
        H = output.shape[2]
        W = output.shape[3]

        detected_keypoints = []
        keypoints_list = np.zeros((0, 3))
        keypoint_id = 0
        threshold = 0.1

        post_y = 0
        rHipY = 0
        lHipY = 0
        neck = 0
        flag_for = True

        for part in range(nPoints):
            probMap = output[0, part, :, :]
            probMap = cv2.resize(probMap, (frame.shape[1], frame.shape[0]))

            # getKeypoints
            mapSmooth = cv2.GaussianBlur(probMap, (3, 3), 0, 0)
            mapMask = np.uint8(mapSmooth > threshold)
            keypoints = []
            contours, _ = cv2.findContours(mapMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                blobMask = np.zeros(mapMask.shape)
                blobMask = cv2.fillConvexPoly(blobMask, cnt, 1)
                maskedProbMap = mapSmooth * blobMask
                _, maxVal, _, maxLoc = cv2.minMaxLoc(maskedProbMap)
                keypoints.append(maxLoc + (probMap[maxLoc[1], maxLoc[0]],))
            # getKeyPoints

            print("Keypoints - {} : {}".format(keypointsMapping[part], keypoints))
            if keypointsMapping[part] == "Neck":
                mapSmooth = cv2.GaussianBlur(probMap, (3, 3), 0, 0)
                mapMask = np.uint8(mapSmooth > threshold)
                keypoints = []
                contours, _ = cv2.findContours(mapMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                for cnt in contours:
                    blobMask = np.zeros(mapMask.shape)
                    blobMask = cv2.fillConvexPoly(blobMask, cnt, 1)
                    maskedProbMap = mapSmooth * blobMask
                    _, maxVal, _, maxLoc = cv2.minMaxLoc(maskedProbMap)
                    keypoints.append(maxLoc + (probMap[maxLoc[1], maxLoc[0]],))
                    neck = maxLoc[1]
            elif keypointsMapping[part] == "R-Hip":
                mapSmooth = cv2.GaussianBlur(probMap, (3, 3), 0, 0)
                mapMask = np.uint8(mapSmooth > threshold)
                keypoints = []
                contours, _ = cv2.findContours(mapMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                for cnt in contours:
                    blobMask = np.zeros(mapMask.shape)
                    blobMask = cv2.fillConvexPoly(blobMask, cnt, 1)
                    maskedProbMap = mapSmooth * blobMask
                    _, maxVal, _, maxLoc = cv2.minMaxLoc(maskedProbMap)
                    keypoints.append(maxLoc + (probMap[maxLoc[1], maxLoc[0]],))
                    rHipY = maxLoc[1]
            elif keypointsMapping[part] == "L-Hip":
                mapSmooth = cv2.GaussianBlur(probMap, (3, 3), 0, 0)
                mapMask = np.uint8(mapSmooth > threshold)
                keypoints = []
                contours, _ = cv2.findContours(mapMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                for cnt in contours:
                    blobMask = np.zeros(mapMask.shape)
                    blobMask = cv2.fillConvexPoly(blobMask, cnt, 1)
                    maskedProbMap = mapSmooth * blobMask
                    _, maxVal, _, maxLoc = cv2.minMaxLoc(maskedProbMap)
                    keypoints.append(maxLoc + (probMap[maxLoc[1], maxLoc[0]],))
                    lHipY = maxLoc[1]
            # print(neck, rHipY, lHipY)
            if neck != 0 and rHipY != 0 and lHipY != 0:
                post_y = neck + rHipY + lHipY

            keypoints_with_id = []
            minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)

            for i in range(len(keypoints)):
                keypoints_with_id.append(keypoints[i] + (keypoint_id,))
                keypoints_list = np.vstack([keypoints_list, keypoints[i]])
                keypoint_id += 1
                # Add the point to the list if the probability is greater than the threshold
            detected_keypoints.append(keypoints_with_id)
        present_Y = post_y
        frameClone = frame.copy()

        for i in range(nPoints):
            for j in range(len(detected_keypoints[i])):
                cv2.circle(frameClone, detected_keypoints[i][j][0:2], 5, colors[i], -1, cv2.LINE_AA)

        # getValidPairs
        valid_pairs = []
        invalid_pairs = []
        n_interp_samples = 10
        paf_score_th = 0.1
        conf_th = 0.7

        for k in range(len(mapIdx)):
            # A->B constitute a limb
            pafA = output[0, mapIdx[k][0], :, :]
            pafB = output[0, mapIdx[k][1], :, :]
            pafA = cv2.resize(pafA, (frameWidth, frameHeight))
            pafB = cv2.resize(pafB, (frameWidth, frameHeight))

            candA = detected_keypoints[POSE_PAIRS[k][0]]
            candB = detected_keypoints[POSE_PAIRS[k][1]]
            nA = len(candA)
            nB = len(candB)

            if (nA != 0 and nB != 0):
                valid_pair = np.zeros((0, 3))
                for i in range(nA):
                    max_j = -1
                    maxScore = -1
                    found = 0
                    for j in range(nB):
                        # Find d_ij
                        d_ij = np.subtract(candB[j][:2], candA[i][:2])
                        norm = np.linalg.norm(d_ij)
                        if norm:
                            d_ij = d_ij / norm
                        else:
                            continue
                        # Find p(u)
                        interp_coord = list(zip(np.linspace(candA[i][0], candB[j][0], num=n_interp_samples),
                                                np.linspace(candA[i][1], candB[j][1], num=n_interp_samples)))
                        # Find L(p(u))
                        paf_interp = []
                        for k in range(len(interp_coord)):
                            paf_interp.append([pafA[int(round(interp_coord[k][1])), int(round(interp_coord[k][0]))],
                                               pafB[int(round(interp_coord[k][1])), int(round(interp_coord[k][0]))]])
                        # Find E
                        paf_scores = np.dot(paf_interp, d_ij)
                        avg_paf_score = sum(paf_scores) / len(paf_scores)

                        # Check if the connection is valid
                        # If the fraction of interpolated vectors aligned with PAF is higher then threshold -> Valid Pair
                        if (len(np.where(paf_scores > paf_score_th)[0]) / n_interp_samples) > conf_th:
                            if avg_paf_score > maxScore:
                                max_j = j
                                maxScore = avg_paf_score
                                found = 1
                    # Append the connection to the list
                    if found:
                        valid_pair = np.append(valid_pair, [[candA[i][3], candB[max_j][3], maxScore]], axis=0)

                # Append the detected connections to the global list
                valid_pairs.append(valid_pair)
            else:  # If no keypoints are detected
                print("No Connection : k = {}".format(k))
                invalid_pairs.append(k)
                valid_pairs.append([])
        # getValidPairs

        # getPersonwiseKeypoints
        personwiseKeypoints = -1 * np.ones((0, 19))

        for k in range(len(mapIdx)):
            if k not in invalid_pairs:
                partAs = valid_pairs[k][:, 0]
                partBs = valid_pairs[k][:, 1]
                indexA, indexB = np.array(POSE_PAIRS[k])

                for i in range(len(valid_pairs[k])):
                    found = 0
                    person_idx = -1
                    for j in range(len(personwiseKeypoints)):
                        if personwiseKeypoints[j][indexA] == partAs[i]:
                            person_idx = j
                            found = 1
                            break

                    if found:
                        personwiseKeypoints[person_idx][indexB] = partBs[i]
                        personwiseKeypoints[person_idx][-1] += keypoints_list[partBs[i].astype(int), 2] + \
                                                               valid_pairs[k][i][2]

                    # if find no partA in the subset, create a new subset
                    elif not found and k < 17:
                        row = -1 * np.ones(19)
                        row[indexA] = partAs[i]
                        row[indexB] = partBs[i]
                        # add the keypoint_scores for the two keypoints and the paf_score
                        row[-1] = sum(keypoints_list[valid_pairs[k][i, :2].astype(int), 2]) + valid_pairs[k][i][2]
                        personwiseKeypoints = np.vstack([personwiseKeypoints, row])
        # getPersonwiseKeypoints

        for i in range(17):
            for n in range(len(personwiseKeypoints)):
                index = personwiseKeypoints[n][np.array(POSE_PAIRS[i])]
                if -1 in index:
                    continue
                B = np.int32(keypoints_list[index.astype(int), 0])
                A = np.int32(keypoints_list[index.astype(int), 1])
                cv2.line(frameClone, (B[0], A[0]), (B[1], A[1]), colors[i], 3, cv2.LINE_AA)
                # 기울기 계산
                if colors[i] == [0, 255, 0]:
                    # calculate_degree
                    dx = B[0] - B[0]
                    dy = A[1] - A[1]
                    rad = math.atan2(abs(dy), abs(dx))

                    deg = rad * 180 / math.pi

                    if deg < 45:
                        string = "bend"
                        cv2.putText(frame, string, (0, 25), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 255))
                        print(f"[degree] {deg} ({string})")
                        op = 'a'
                        #ARD.write(op.encode())
                    elif deg > 45:
                        op = 'b'
                        #ARD.write(op.encode())
                    # calculate_degree

        if pre_Y - present_Y > 500:  # 숫자가 커질수록 민감도 높아짐
            print("fall!!!!!!!!!!!!!!!!!!!!!!!!!!")
            filename = datetime.datetime.now().strftime("%H-%M-%S")
            foldername = datetime.datetime.now().strftime("%F")
            cv2.imwrite("C:\\capture\\ " + str(filename) + ".png", frame)  # 데스크탑에 저장 >> 파이어 베이스 업로드로 변경하면됨
            storage.child(str(foldername) + "/" + str(filename) + ".png" + ".png").put("C:\\capture\\ " + str(filename) + ".png")
            
        pre_Y = present_Y
        present_Y = 0

        cv2.putText(frame, "time taken = {:.2f} sec".format(time.time() - t), (50, 50), cv2.FONT_HERSHEY_COMPLEX, .8,
                    (255, 50, 0), 2, lineType=cv2.LINE_AA)
        imgencode = cv2.imencode('.jpg', frameClone)[1]
        stringData = imgencode.tostring()
        yield (b'--frame\r\n'
               b'Content-Type: text/plain\r\n\r\n' + stringData + b'\r\n')

        vid_writer.write(frameClone)

    cv2.waitKey(0)
    del (cap)


@app.route('/calculation')
def calculation():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
