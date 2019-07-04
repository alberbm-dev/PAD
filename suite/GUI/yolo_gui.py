# Import Python packages
import numpy as np
import time
import cv2
import os

# Define openCV BGR colors
GREEN_BGR = (0, 255, 0)
RED_BGR = (0, 0, 180)


def run_yolo3(**params):
    # Load COCO classes
    labels_path = os.path.sep.join([params["yolo_path"], "coco.names"])
    labels = open(labels_path).read().strip().split("\n")

    # Initialize a list of colors to represent each possible class label
    # np.random.seed(42)
    # colors = np.random.randint(0, 255, size=(len(labels), 3), dtype="uint8")
    # colors[0] = (0, 0, 255)
    # colors[9] = (0, 255, 0)

    # Get paths to YOLO weights and model configuration
    weights_path = os.path.sep.join([params["yolo_path"], "yolov3.weights"])
    config_path = os.path.sep.join([params["yolo_path"], "yolov3.cfg"])

    # Load YOLO object
    print(f"[INFO] Loading YOLO from disk...")
    net = cv2.dnn.readNetFromDarknet(config_path, weights_path)

    frame_list = list()
    for frame_idx in range(0, len(params["frame_path"])):
        frame_list.append(os.path.split(params["frame_path"][frame_idx])[1])
        # Load image and get dimensions
        image = cv2.imread(params["frame_path"][frame_idx])
        (H, W) = image.shape[:2]

        # Determine only the *output* layer names needed
        layer_names = net.getLayerNames()
        layer_names = [layer_names[i[0] - 1] for i
                       in net.getUnconnectedOutLayers()]

        # Construct blob from input frame
        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True,
                                     crop=False)
        net.setInput(blob)
        start = time.time()
        # Perform a forward pass on YOLO
        layer_outputs = net.forward(layer_names)
        end = time.time()

        # Show timing information
        print("[INFO] YOLO took {:.4f} seconds".format(end - start))

        boxes = []
        confidences = []
        class_ids = []

        # Loop over each of the layer outputs
        for output in layer_outputs:
            # Loop over each of the detections
            for detection in output:
                # Extract  class ID and confidence
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                # Filter out weak predictions under confidence threshold
                if confidence > params["confidence"]:
                    # Scale the coordinates back relative to the original size
                    box = detection[0:4] * np.array([W, H, W, H])
                    (center_X, center_Y, width, height) = box.astype("int")

                    # Derive top-left coordinates
                    x = int(center_X - (width / 2))
                    y = int(center_Y - (height / 2))

                    # Update coordinates, confidences and class IDs
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        # Remove overlapping applying non-maxima supression
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, params["confidence"],
                                params["threshold"])

        # Ensure at least one detection exists
        if len(idxs) > 0:
            # Loop over the kept indexes after NMS
            subj_idx = 0
            for i in idxs.flatten():
                # Only show people and traffic lights boxes
                if class_ids[i] == 0 or class_ids[i] == 9:
                    # Extract the bounding box coordinates
                    (x, y) = (boxes[i][0], boxes[i][1])
                    (w, h) = (boxes[i][2], boxes[i][3])

                    # Draw a bounding box rectangle and label on the image
                    # color = [int(c) for c in colors[class_ids[i]]]
                    cv2.rectangle(image, (x, y), (x + w, y + h), RED_BGR, 2)
                    # text = "{}: {:.3f}".format(labels[class_ids[i]],
                    #                            confidences[i])
                    text = "{}".format("subj" + str(subj_idx))
                    cv2.putText(image, text, (x, y - 5),
                                cv2.FONT_HERSHEY_DUPLEX, 0.4, RED_BGR, 1)

                    # Write bounding box data to a file
                    if os.path.exists(params["bbox_path"] + "/" +
                                      frame_list[frame_idx].replace(".png", "")
                                      + "_data.tsv"):
                        out_tsv = open(params["bbox_path"] + "/" +
                                       frame_list[frame_idx].replace(".png",
                                                                     "") +
                                       "_data.tsv", "r+")
                        pre_data = out_tsv.read()
                        out_data = ""

                    else:
                        out_tsv = open(params["bbox_path"] + "/" +
                                       frame_list[frame_idx].replace(".png",
                                                                     "") +
                                       "_data.tsv", "w")
                        out_data = "Source image:\t" + frame_list[frame_idx]
                        # out_data +="\n\nName\tX0\tY0\tX1\tY1\tW\tH\tA\tClass"
                        out_data += "\nName\tX0\tY0\tX1\tY1\tW\tH\tA"

                    out_data += "\n" + "subj"+str(subj_idx)
                    out_data += "\t" + str(x) + "\t" + str(y)
                    out_data += "\t" + str(x+w) + "\t" + str(y+h)
                    out_data += "\t" + str(w) + "\t" + str(h)
                    out_data += "\t" + str(w * h)
                    # out_data += "\t" + str(w*h) + "\t" + labels[class_ids[i]]
                    out_tsv.write(out_data)
                    out_tsv.close()
                    subj_idx += 1

        # Write data to the frame
        cv2.imwrite(params["bbox_path"] + "/" +
                    frame_list[frame_idx].replace(".png", "") + "_bboxes.png",
                    image)
    return "done"
