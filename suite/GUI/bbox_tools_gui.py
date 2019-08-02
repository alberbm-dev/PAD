# Import Python packages
import os
import cv2
import numpy as np
import math
import munkres

# Define openCV BGR colors
GREEN_BGR = (0, 255, 0)
RED_BGR = (0, 0, 180)
BLACK_BGR = (0, 0, 0)

# Available OpenCV trackers
TRACKERS = ["Boosting", "MIL", "KCF", "TLD", "MedianFlow", "GOTURN", "MOSSE",
            "CSRT"]


def draw_bbox(**params):
    """ This function allows the user to draw its own bounding boxes on an
    existing frame.

    :param params: dict
        Parameters introduced by the user (frames path, subject codes)
    :return: done flag
    """

    print(f"[INFO] Working...")
    # Iterate over every frame
    for file_idx in range(0, len(params["frame_path"])):
        # Read image
        img = cv2.imread(params["frame_path"][file_idx])
        # Create a new output data file if it doesn't exist, else just read
        if "bboxes" in os.path.split(params["frame_path"][file_idx])[1]:
            tsv_path = params["frame_path"][file_idx].replace("_bboxes.png",
                                                              "_data.tsv")
            out_path = params["frame_path"][file_idx]
        else:
            tsv_path = params["frame_path"][file_idx].replace(".png",
                                                              "_data.tsv")
            out_path = params["frame_path"][file_idx].replace(".png",
                                                              "_bboxes.png")
        if not os.path.exists(tsv_path):
            with open(tsv_path, "w") as tsv_in:
                out_data = "Source image:\t" + \
                           os.path.split(params["frame_path"][file_idx])[1].\
                               replace("_bboxes", "")
                # out_data += "\n\nName\tX0\tY0\tX1\tY1\tW\tH\tA\tClass"
                out_data += "\nName\tX0\tY0\tX1\tY1\tW\tH\tA"
                tsv_in.write(out_data)
                del out_data
        with open(tsv_path, "r") as tsv_in:
            out_data = tsv_in.read().strip("\n")
            tsv_in.seek(0)
            lines = tsv_in.readlines()
        # Draw ROIs
        rois = cv2.selectROIs("ROI selection " +
                              os.path.split(params["frame_path"][file_idx])[1],
                              img, True, False)
        for bb_idx in range(0, len(rois)):
            x0, y0, w, h = tuple(rois[bb_idx])
            cv2.rectangle(img, (x0, y0), (x0 + w, y0 + h), RED_BGR, 2)
            cv2.putText(img, "subj" + str(bb_idx + len(lines) - 2),
                        (x0, y0 - 5),
                        cv2.FONT_HERSHEY_DUPLEX, 0.4, RED_BGR, 1)
            cv2.imwrite(out_path, img)
            out_data += "\n" + "subj" + str(bb_idx + len(lines) - 2)
            out_data += "\t" + str(x0) + "\t" + str(y0)
            out_data += "\t" + str(x0 + w) + "\t" + str(y0 + h)
            out_data += "\t" + str(w) + "\t" + str(h)
            out_data += "\t" + str(w * h)
        # Write bounding box data to the TSV file
        with open(tsv_path, "w") as tsv_out:
            tsv_out.write(out_data)
            del out_data
        cv2.destroyAllWindows()
    return "done"


def id_bbox(params, bbox_data):
    """ This function allows the user to match bounding boxes to particular
    subjects.

    :param params: dict
        Parameters introduced by the user (frames/data paths).
    :param bbox_data: dict
        Bounding box data for every subject.
    :return: done flag
    """

    print(f"[INFO] Working...")
    # Read image and subjects
    bbox_img = cv2.imread(params["frame_path"])
    # colors = {"person": (0, 0, 255), "traffic_light": (0, 255, 0)}
    subjects = list(bbox_data.keys())
    # Margin between click location and bounding box location
    pad = 10
    with open(params["bbox_path"], "r") as in_bbox:
        lines = in_bbox.readlines()
        data_out = ""
        for line in lines:
            cols = line.replace("\n", "").split("\t")
            try:
                x0 = int(cols[1])
                y0 = int(cols[2])
                x1 = int(cols[3])
                y1 = int(cols[4])
                # Check which bounding box better fits click position
                for subj_idx in range(0, len(subjects)):
                    subject = subjects[subj_idx]
                    if (bbox_data[subject]["X0"] in range(x0-pad, x0+pad)
                            and
                            bbox_data[subject]["Y0"] in range(y0-pad, y0+pad)
                            and
                            bbox_data[subject]["X1"] in range(x1-pad, x1+pad)
                            and
                            bbox_data[subject]["Y1"] in range(y1-pad, y1+pad)):
                        data_out += line.replace(cols[0], subjects[subj_idx])
                        # if subjects[subj_idx] == "Traffic_light":
                        #     color = colors["traffic_light"]
                        # else:
                        #     color = colors["person"]
                        # Write subject name below bounding box.
                        # cv2.rectangle(bbox_img, (x0, y1 + 5),
                        #               (x0 + 65, y1 + 25), BLACK_BGR,
                        #               cv2.FILLED)
                        cv2.putText(bbox_img, subject, (x0, y1+15),
                                    cv2.FONT_HERSHEY_DUPLEX, 0.45, RED_BGR, 1)
                        cv2.imwrite(params["frame_path"].replace(".png", "")
                                    + "_subjects.png", bbox_img)
                        break
            except (ValueError, IndexError):
                data_out += line
    # Update data file
    with open(params["bbox_path"].replace(".tsv", "") + "_edit.tsv",
              "w") as out_bbox:
        out_bbox.write(data_out)
    return "done"


def remove_bbox(**params):
    """ This functions allows the user to erase existing bounding boxes from
    several frames.

    :param params: dict
        Parameters introduced by the user (frames/data paths, subject codes)
    :return: done flag
    """

    print(f"[INFO] Working...")
    # Iterate over every data file
    for file_idx in range(0, len(params["bbox_path"])):
        # Overwrite data file skipping selected subjects
        with open(params["bbox_path"][file_idx], "r") as in_tsv:
            lines = in_tsv.readlines()
        with open(params["bbox_path"][file_idx], "w") as out_tsv:
            for line in lines:
                if not line.split("\t")[0] in params["subjects"]:
                    out_tsv.write(line)
        del lines
        # Load corresponding image, read bounding box data and draw them
        bbox_img = cv2.imread(params["frame_path"][file_idx])
        with open(params["bbox_path"][file_idx], "r") as in_bbox:
            lines = in_bbox.readlines()
            for line in lines:
                cols = line.replace("\n", "").split("\t")
                try:
                    subject = str(cols[0])
                    x0 = int(cols[1])
                    y0 = int(cols[2])
                    x1 = int(cols[3])
                    y1 = int(cols[4])
                    # if cols[7] == "traffic_light":
                    #     color = (0, 255, 0)
                    # elif cols[7] == "person":
                    #     color = (0, 0, 255)
                    cv2.rectangle(bbox_img, (x0, y0), (x1, y1), RED_BGR, 2)
                    cv2.putText(bbox_img, subject, (x0, y0-5),
                                cv2.FONT_HERSHEY_DUPLEX, 0.4, RED_BGR, 1)
                except (ValueError, IndexError):
                    pass
        cv2.imwrite(params["bbox_path"][file_idx].replace("_data.tsv", "") +
                    "_bboxes.png", bbox_img)
    return "done"


def remove_bbox_v2(params, bbox_data):
    print(f"[INFO] Working...")
    # List of subjects to be eliminated
    gones = list(bbox_data.keys())
    # Margin between click location and bounding box location
    pad = 10
    subj_out = list()
    # Read original bounding box data
    with open(params["bbox_path"], "r") as in_bbox:
        lines = in_bbox.readlines()
        for line in lines:
            cols = line.replace("\n", "").split("\t")
            try:
                subj = cols[0]
                x0 = int(cols[1])
                y0 = int(cols[2])
                x1 = int(cols[3])
                y1 = int(cols[4])
                # Check which bounding box better fits click position
                for gone_idx in range(0, len(gones)):
                    gone = gones[gone_idx]
                    if (bbox_data[gone]["X0"] in range(x0 - pad,
                                                       x0 + pad) and
                            bbox_data[gone]["Y0"] in range(y0 - pad,
                                                           y0 + pad) and
                            bbox_data[gone]["X1"] in range(x1 - pad,
                                                           x1 + pad) and
                            bbox_data[gone]["Y1"] in range(y1 - pad,
                                                           y1 + pad)):
                        subj_out.append(subj)
                        break
            except (ValueError, IndexError):
                pass
    # Update data file
    with open(params["bbox_path"], "w") as out_bbox:
        for line in lines:
            if not line.split("\t")[0] in subj_out:
                out_bbox.write(line)
    del lines
    # Load corresponding image, read bounding box data and draw them
    bbox_img = cv2.imread(params["frame_path"])
    with open(params["bbox_path"], "r") as in_bbox:
        lines = in_bbox.readlines()
        for line in lines:
            cols = line.replace("\n", "").split("\t")
            try:
                subject = str(cols[0])
                x0 = int(cols[1])
                y0 = int(cols[2])
                x1 = int(cols[3])
                y1 = int(cols[4])
                # if cols[7] == "traffic_light":
                #     color = (0, 255, 0)
                # elif cols[7] == "person":
                #     color = (0, 0, 255)
                cv2.rectangle(bbox_img, (x0, y0), (x1, y1), RED_BGR, 2)
                cv2.putText(bbox_img, subject, (x0, y0 - 5),
                            cv2.FONT_HERSHEY_DUPLEX, 0.4, RED_BGR, 1)
            except (ValueError, IndexError):
                pass
    cv2.imwrite(
        params["bbox_path"].replace("_data.tsv", "") + "_bboxes.png",
        bbox_img)

    return "done"


def track_bbox(**params):
    """ This function performs tracking of subjects across a set of frames,
    using Hungarian Algorithm.

    :param params: dict
        Parameters introduced by the user (bounding box data).
    :return: done flag
    """

    print(f"[INFO] Working...")
    coords = dict()
    # Load data from two frames at a time, first one contains real names
    for tsv_idx in range(0, len(params["bbox_path"])-1):
        with open(params["bbox_path"][tsv_idx], "r") as tsv_k0,\
                open(params["bbox_path"][tsv_idx+1], "r") as tsv_k1:
            data_k0 = tsv_k0.readlines()
            data_k1 = tsv_k1.readlines()
            coords["k0"] = dict()
            coords["k1"] = dict()
            for line_idx in range(2, len(data_k0)):
                cols = data_k0[line_idx].replace("\n", "").split("\t")
                coords["k0"][cols[0]] = cols[1:len(cols)]
            for line_idx in range(2, len(data_k1)):
                cols = data_k1[line_idx].replace("\n", "").split("\t")
                coords["k1"][cols[0]] = cols[1:len(cols)]
        out_k1 = ''.join(data_k1)
        k0_keys = list(coords["k0"].keys())
        k1_keys = list(coords["k1"].keys())
        bbox_img = cv2.imread(params["bbox_path"][tsv_idx + 1].
                              replace("_data.tsv", "_bboxes.png"))
        ImW = bbox_img.shape[1]
        ImH = bbox_img.shape[0]
        # Distance between bounding boxes centers
        offset = np.empty([len(k0_keys), len(k1_keys)])
        # Ratio between bounding boxes areas
        ratio = np.empty([len(k0_keys), len(k1_keys)])
        # categ = np.empty([len(k0_keys), len(k1_keys)])
        # Compute center offset and area ratio
        for subj_k0 in range(0, len(coords["k0"].keys())):
            for subj_k1 in range(0, len(coords["k1"].keys())):
                xc_0 = (int(coords["k0"][k0_keys[subj_k0]][0]) +
                        int(coords["k0"][k0_keys[subj_k0]][2])) / 2
                yc_0 = (int(coords["k0"][k0_keys[subj_k0]][1]) +
                        int(coords["k0"][k0_keys[subj_k0]][3])) / 2
                c_0 = np.array((xc_0, yc_0))
                area_0 = int(coords["k0"][k0_keys[subj_k0]][6])
                xc_1 = (int(coords["k1"][k1_keys[subj_k1]][0]) +
                        int(coords["k1"][k1_keys[subj_k1]][2])) / 2
                yc_1 = (int(coords["k1"][k1_keys[subj_k1]][1]) +
                        int(coords["k1"][k1_keys[subj_k1]][3])) / 2
                c_1 = np.array((xc_1, yc_1))
                area_1 = int(coords["k1"][k1_keys[subj_k1]][6])
                # offset[subj_k0][subj_k1] = np.linalg.norm(c_0 - c_1)
                offset[subj_k0][subj_k1] = np.linalg.norm(c_0 - c_1) \
                    / math.sqrt(ImW**2 + ImH**2)
                # ratio[subj_k0][subj_k1] = abs((A_0 - A_1)/A_0)
                # ratio[subj_k0][subj_k1] = abs(area_0-area_1)/(area_0+area_1)
                ratio[subj_k0][subj_k1] = abs(area_0 - area_1) / (ImW * ImH)
                # categ = [0 if coords["k0"][k0_keys[subj_k0]][7] ==
                #          coords["k1"][k1_keys[subj_k1]][7] else 1]
        # cost = 0.4*offset + 0.2*ratio + 0.4*int(categ[0])
        # Cost is 60% offset, 40% ratio
        cost = 60*offset + 40*ratio
        # Munkres requires list, not numpy matrix
        cost = cost.tolist()
        # Create munkres matrix and compute optimal cost combination
        m = munkres.Munkres()
        indexes = m.compute(cost)

        # Read frame without subjects, write real names according to tracking
        # bbox_img = cv2.imread(params["bbox_path"][tsv_idx + 1]
        #                       .replace("_data.tsv", "_bboxes.png"))
        for row, column in indexes:
            # value = cost[row][column]
            # print(f'({row}, {column}) -> {value}')
            out_k1 = out_k1.replace(k1_keys[column], k0_keys[row])
            text = k0_keys[row]
            x = int(coords["k1"][k1_keys[column]][0])
            y = int(coords["k1"][k1_keys[column]][3])
            size = cv2.getTextSize(text, cv2.FONT_HERSHEY_DUPLEX, 0.55, 1)
            # cv2.rectangle(bbox_img, (x, y + 5), (x + size[0][0], y + 5),
            #               BLACK_BGR, cv2.FILLED)
            cv2.putText(bbox_img, text, (x, y + 20), cv2.FONT_HERSHEY_DUPLEX,
                        0.55, RED_BGR, 1)
            cv2.imwrite(params["bbox_path"][tsv_idx + 1].replace(
                "_data.tsv", "_bboxes_subjects.png"), bbox_img)
        # Update data file
        with open(params["bbox_path"][tsv_idx+1], "w") as tsv_out:
            tsv_out.write(out_k1)
        del m
        del cost
        del data_k1
        del data_k0
        del coords["k0"]
        del coords["k1"]
    return "done"


def track_bbox_v2(**params):
    """ This function performs tracking of subjects across a set of frames,
        using OpenCV built-in trackers.

    :param params: dict
        Parameters introduced by the user (frames, tracker, subject).
    :return: done/error flag
    """

    print(f"[INFO] Working...")
    # Create tracker object corresponding to choice
    if params["tracker"] == "Boosting":
        tracker = cv2.TrackerBoosting_create()
    elif params["tracker"] == "MIL":
        tracker = cv2.TrackerMIL_create()
    elif params["tracker"] == "KCF":
        tracker = cv2.TrackerKCF_create()
    elif params["tracker"] == "TLD":
        tracker = cv2.TrackerTLD_create()
    elif params["tracker"] == "MedianFlow":
        tracker = cv2.TrackerMedianFlow_create()
    elif params["tracker"] == "GOTURN":
        tracker = cv2.TrackerGOTURN_create()
    elif params["tracker"] == "MOSSE":
        tracker = cv2.TrackerMOSSE_create()
    elif params["tracker"] == "CSRT":
        tracker = cv2.TrackerCSRT_create()
    # Iterate over all the frame on the list
    for frame_idx in range(0, len(params["frame_path"])):
        # Read frame
        img = cv2.imread(params["frame_path"][frame_idx])
        if "tracking" in os.path.split(params["frame_path"][frame_idx])[1]:
            tsv_path = params["frame_path"][frame_idx]. \
                replace("_tracking.png", "_data.tsv")
            out_path = params["frame_path"][frame_idx]
        else:
            tsv_path = params["frame_path"][frame_idx]. \
                replace(".png", "_data.tsv")
            out_path = params["frame_path"][frame_idx]. \
                replace(".png", "_tracking.png")
        # First frame: draw bounding box and initialize tracker
        if frame_idx == 0:
            bbox = cv2.selectROI("Select ROI " + os.path.
                                 split(params["frame_path"][frame_idx])[1], img)
            ok = tracker.init(img, bbox)
        # Rest of frames: update tracker with the current frame
        else:
            ok, bbox = tracker.update(img)
        # Succesful tracking: save data
        if ok:
            # Draw bounding box on the frame, including identifier
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(img, p1, p2, RED_BGR, 2)
            cv2.putText(img, params["subject"], (p1[0], p2[1] + 20),
                        cv2.FONT_HERSHEY_DUPLEX, 0.55, RED_BGR, 1)
            cv2.imwrite(out_path, img)
            # Save bounding box data to TSV file
            if not os.path.exists(tsv_path):
                with open(tsv_path, "w") as tsv_in:
                    out_data = "Source image:\t" + os.path.\
                        split(params["frame_path"][frame_idx])[1].\
                        replace("_bboxes", "")
                    out_data += "\nName\tX0\tY0\tX1\tY1\tW\tH\tA"
                    tsv_in.write(out_data)
                    del out_data
            with open(tsv_path, "r") as tsv_in:
                out_data = tsv_in.read().strip("\n")
                tsv_in.seek(0)
                out_data += "\n" + params["subject"]
                out_data += "\t" + str(int(bbox[0])) + "\t" + str(int(bbox[1]))
                out_data += "\t" + str(int(bbox[0] + bbox[2])) + \
                            "\t" + str(int(bbox[1] + bbox[3]))
                out_data += "\t" + str(int(bbox[2])) + "\t" + str(int(bbox[3]))
                out_data += "\t" + str(int(bbox[2]) * int(bbox[3]))
            with open(tsv_path, "w") as tsv_out:
                tsv_out.write(out_data)
                del out_data
            cv2.destroyAllWindows()
        # Unsuccesful tracking: raise error flag
        else:
            return "error"
    return "done"
