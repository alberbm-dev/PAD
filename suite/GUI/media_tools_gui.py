# Import Python packages
import os
import cv2
import numpy as np


def any2avi(**params):
    """ This function converts an MP4 (or other format) video into an AVI file.

    :param params: dict
        Parameters introduced by the user (input/output paths).
    :return: done flag.
    """

    print(f"[INFO] Working...")
    any_list = list()
    # Iterate over every input file
    for any_idx in range(0, len(params["any_path"])):
        # Extract input file name and get AVI name
        any_list.append(os.path.split(params["any_path"][any_idx])[1])
        any_vid = cv2.VideoCapture(params["any_path"][any_idx])
        avi_name = any_list[any_idx].split(".", 1)[0] + ".avi"
        # Create a new AVI video object
        avi_vid = cv2.VideoWriter(params["avi_path"] + "/" + avi_name,
                                  cv2.VideoWriter_fourcc(*'XVID'),
                                  int(any_vid.get(cv2.CAP_PROP_FPS)),
                                  (int(any_vid.get(cv2.CAP_PROP_FRAME_WIDTH)),
                                   int(any_vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
                                   ))
        # As long as there are frames left, read one and save it to the AVI
        ret = True
        while ret:
            ret, frame = any_vid.read()
            if not ret:
                break
            avi_vid.write(frame)
        avi_vid.release()
        del avi_vid
        any_vid.release()
        del any_vid
    return "done"


def fancynaming_clip2frames(video, frame_idx):
    """ This function creates cool names for output files, following
    the format (frame_{number}.png)

    :param video: opencv video object
        Video to extract name from.
    :param frame_idx: int
        Index of the frame in the video.
    :return: file name for the frame.
    """

    # Pad code with zeros
    num_zeros = np.zeros(len(str(int(video.get(cv2.CAP_PROP_FRAME_COUNT)))) + 1
                         - len(str(frame_idx)))
    num_zeros = np.int32(num_zeros)
    # Build name string
    fancy_name = "frame_" + "0" * len(num_zeros) + str(frame_idx) + ".png"
    return fancy_name


def clip2frames(**params):
    """ This function extracts the frames from a video.

    :param params: dict
         Parameters introduced by the user (input/output paths).
    :return: done flag
    """

    print(f"[INFO] Working...")
    vid_name = list()
    # Iterate over all the chosen videos
    for vid_idx in range(0, len(params["clip_path"])):
        # Get the name of the video, without path nor extension
        vid_name.append(os.path.split(params["clip_path"][vid_idx])[1])
        vid_name[vid_idx] = vid_name[vid_idx].split(".")[0]
        # Check if output directory already exists, create it if it doesn't
        try:
            os.makedirs(params["frame_path"] + "/" + vid_name[vid_idx])
        except FileExistsError:
            pass
        vid = cv2.VideoCapture(params["clip_path"][vid_idx])
        frame_idx = int(vid.get(cv2.CAP_PROP_POS_FRAMES)) + 1
        ret = True
        # As long as there are frames left, read a frame and store it
        while ret:
            ret, frame = vid.read()
            if not ret:
                break
            frame_name = fancynaming_clip2frames(vid, frame_idx)
            cv2.imwrite(params["frame_path"] + "/" + vid_name[vid_idx] + "/" +
                        frame_name, frame)
            frame_idx += 1
        vid.release()
        del vid
    return "done"


def clip2vid(**params):
    """ This function merges several video clips into one single file.

    :param params: dict
        Parameters introduced by the user (input/output paths).
    :return: done flag
    """

    print(f"[INFO] Working...")
    # Iterate over all the input files
    for clip_idx in range(len(params["clip_path"])):
        clip = cv2.VideoCapture(params["clip_path"][clip_idx])
        # Create the video file when the first clip is read
        if clip_idx == 0:
            vid = cv2.VideoWriter(params["vid_path"],
                                  cv2.VideoWriter_fourcc(*'XVID'),
                                  int(clip.get(cv2.CAP_PROP_FPS)),
                                  (int(clip.get(cv2.CAP_PROP_FRAME_WIDTH)),
                                   int(clip.get(cv2.CAP_PROP_FRAME_HEIGHT))))
        # As long as there are frames left, read one and write it to the video
        ret = True
        while ret:
            ret, frame = clip.read()
            vid.write(frame)
        clip.release()
        del clip
    vid.release()
    return "done"


def frames2clip(**params):
    """ This function builds a video file from its individual frames.

    :param params: dict
        Parameters introduced by the user (input/output paths, fps).
    :return: done flag
    """

    print(f"[INFO] Working...")
    # Read a frame and create video object with according parameters
    img = cv2.imread(params["frame_path"][0])
    clip = cv2.VideoWriter(params["clip_path"],
                           cv2.VideoWriter_fourcc(*'XVID'),
                           params["fps"], (img.shape[1], img.shape[0]))
    # For every frame, read it and write it to the video file
    for frame_idx in range(0, len(params["frame_path"])):
        img = cv2.imread(params["frame_path"][frame_idx])
        clip.write(img)
    clip.release()
    return "done"


def fancynaming_hevc2avi(filename, total):
    """ This function creates cool names for output files, following
    the format (video_{number}.avi)

    :param filename: str
        Video file name.
    :param total: int
        Total number of videos.
    :return: file name for the video.
    """

    # Find video code (number after timestamp)
    idx1 = filename.rfind("--")
    idx2 = filename.rfind("--", 0, idx1)
    code = filename[idx2+2:idx1]
    # Pad code with zeros
    num_zeros = np.int32(np.zeros(len(str(total)) + 1 - len(code)))
    fancy_name = "video_" + "0"*len(num_zeros) + code + ".avi"
    return fancy_name


def hevc2avi(**params):
    """ This function converts an HEVC video into an AVI video.

    :param params: dict
        Parameters introduced by the user (input/output paths).
    :return: done flag.
    """

    print(f"[INFO] Working...")
    hevc_list = list()
    # Iterate over every HEVC file
    for hevc_idx in range(0, len(params["hevc_path"])):
        # Extract HEVC name and get AVI name
        hevc_list.append(os.path.split(params["hevc_path"][hevc_idx])[1])
        hevc_vid = cv2.VideoCapture(params["hevc_path"][hevc_idx])
        avi_name = fancynaming_hevc2avi(hevc_list[hevc_idx], len(hevc_list))
        # Create a new AVI video object
        avi_vid = cv2.VideoWriter(params["avi_path"] + "/" + avi_name,
                                  cv2.VideoWriter_fourcc(*'XVID'),
                                  int(hevc_vid.get(cv2.CAP_PROP_FPS)),
                                  (int(hevc_vid.get(cv2.CAP_PROP_FRAME_WIDTH)),
                                   int(hevc_vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
                                   ))
        # As long as there are frames left, read one and save it to the AVI
        ret = True
        while ret:
            ret, frame = hevc_vid.read()
            if not ret:
                break
            avi_vid.write(frame)
        avi_vid.release()
        del avi_vid
        hevc_vid.release()
        del hevc_vid
    return "done"


def vid2clip(**params):
    """ This function cuts a video file into a clip.

    :param params: dict
        Parameters introduced by the user (input/output paths,
         start/stop times).
    :return: done flag
    """

    print(f"[INFO] Working...")
    vid = cv2.VideoCapture(params["vid_path"])
    # Advance the video to the chosen start time
    vid.set(cv2.CAP_PROP_POS_MSEC, params["start_time"])
    # Create a clip video object according to input video properties
    clip = cv2.VideoWriter(params["clip_path"],
                           cv2.VideoWriter_fourcc(*'XVID'),
                           int(vid.get(cv2.CAP_PROP_FPS)),
                           (int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)),
                            int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    # As long as stop time has not been reached, or no more clips left,
    # read a frame and write it to the clip file
    ret = True
    first_frame = vid.get(cv2.CAP_PROP_POS_FRAMES)
    while vid.get(cv2.CAP_PROP_POS_MSEC) <= params["stop_time"] and ret:
        ret, frame = vid.read()
        clip.write(frame)
    clip.release()
    last_frame = vid.get(cv2.CAP_PROP_POS_FRAMES)
    clip_frames = last_frame - first_frame + 1
    vid.release()

    # Save the conversion information to a TSV file
    with open(params["clip_path"].split(".")[0] + "_data.tsv", "w") as f:
        out_data = "Original video:\t" + os.path.split(params["vid_path"])[1] \
                   + "\n"
        out_data += "Clip name:\t" + os.path.split(params["clip_path"])[1] + \
                    "\n"
        out_data += "Start time:\t" + str(int(params["start_time"])) + " ms\n"
        out_data += "Start frame:\t" + str(int(first_frame)) + "\n"
        out_data += "Stop time:\t" + str(int(params["stop_time"])) + " ms\n"
        out_data += "Stop frame:\t" + str(int(last_frame)) + "\n"
        out_data += "Total clip frames:\t" + str(clip_frames) + "\n"
        f.write(out_data)
    return "done"
