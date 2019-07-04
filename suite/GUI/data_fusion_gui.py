# Import Python packages
import cv2

# Define openCV BGR colors
RED_BGR = (0, 0, 180)
BLACK_BGR = (0, 0, 0)


def data_fusion(**params):
    """ This function includes the behavioral data from BORIS in a video.

    :param params: dict
        Parameters introduced by the user (BORIS path, input/output clip paths)
    :return: done flag
    """

    print(f'[INFO] Working...')
    # Read BORIS file and find properties and values
    with open(params["boris_path"], "r") as boris_tsv:
        lines = boris_tsv.readlines()
        for line in lines:
            try:
                line.index("Time\tMedia")
                props_idx = lines.index(line)
            except ValueError:
                pass
        props = lines[props_idx].split("\t")
        subj_idx = props.index("Subject")
        behav_idx = props.index("Behavior")
        try:
            mod1_idx = props.index("Modifier 1")
        except ValueError:
            pass
        try:
            mod2_idx = props.index("Modifier 2")
        except ValueError:
            pass
        stat_idx = props.index("Status\n")
        time_idx = props.index("Time")
        # Save behavior data to a 2D array
        vals = lines[props_idx+1:lines.__len__()]
        vals = ",".join(vals).replace("\n", "").split(",")
        vals = list(map(lambda x: x.split("\t"), vals))
        # Create a dictionary for storing subjects, behaviors, mods, timestamps
        behaviors = dict()
        # Iterate over every line of the behavior matrix
        for line in vals.__iter__():
            # If the subject is new, create its own dictionary
            if not line[subj_idx] in behaviors.keys():
                behaviors[line[subj_idx]] = dict()
            # If the behavior is new for the subject, create dictionary
            if not line[behav_idx] in behaviors[line[subj_idx]].keys():
                behaviors[line[subj_idx]][line[behav_idx]] = dict()
                try:
                    behaviors[line[subj_idx]][line[behav_idx]]["Mod1"] = \
                        [line[mod1_idx]]
                except (NameError, UnboundLocalError):
                    pass
                try:
                    behaviors[line[subj_idx]][line[behav_idx]]["Mod2"] = \
                        [line[mod2_idx]]
                except (NameError, UnboundLocalError):
                    pass
                behaviors[line[subj_idx]][line[behav_idx]]["START"] = []
                behaviors[line[subj_idx]][line[behav_idx]]["STOP"] = []
                behaviors[line[subj_idx]][line[behav_idx]][line[stat_idx]] = \
                    [line[time_idx]]
            # For already exisitng behaviors just register modifiers and times
            else:
                try:
                #     if not line[mod1_idx] in \
                #            behaviors[line[subj_idx]][line[behav_idx]]["Mod1"]:
                    behaviors[line[subj_idx]][line[behav_idx]]["Mod1"]. \
                        append(line[mod1_idx])
                except (KeyError, NameError, UnboundLocalError):
                    pass
                try:
                #     if not line[mod2_idx] in \
                #            behaviors[line[subj_idx]][line[behav_idx]]["Mod2"]:
                        behaviors[line[subj_idx]][line[behav_idx]]["Mod2"]. \
                            append(line[mod2_idx])
                except (KeyError, NameError, UnboundLocalError):
                    pass
                behaviors[line[subj_idx]][line[behav_idx]][line[stat_idx]].\
                    append(line[time_idx])

    # Create input and output video objects, same parameters
    vid_in = cv2.VideoCapture(params["clip_path"])
    vid_out = cv2.VideoWriter(params["fusion_path"],
                              cv2.VideoWriter_fourcc(*'XVID'),
                              int(vid_in.get(cv2.CAP_PROP_FPS)),
                              (int(vid_in.get(cv2.CAP_PROP_FRAME_WIDTH)),
                               int(vid_in.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    # As long as there are frames left, read one and write information
    ret = True
    while ret:
        ret, frame = vid_in.read()
        pos_ms = vid_in.get(cv2.CAP_PROP_POS_MSEC)
        pos_s = pos_ms/1000
        line = 0
        # Iterate over every subject and behavior
        for subj in behaviors.keys():
            for behav in behaviors[subj].keys():
                # Some behaviors are repeated, so more iterations
                for rep in range(0, len(behaviors[subj][behav]["START"])):
                    # Check if the behavior is active or not
                    if float(behaviors[subj][behav]["START"][rep]) <= pos_s \
                            <= float(behaviors[subj][behav]["STOP"][rep]):
                        line += 1
                        # Build text with subject, behavior (and mods, if any)
                        text = subj + "-" + behav
                        try:
                            if behaviors[subj][behav]["Mod1"][2*rep]:
                                mod1 = behaviors[subj][behav]["Mod1"][2*rep]
                                text = text + "-" + mod1
                        except (IndexError, KeyError):
                            pass
                        try:
                            if behaviors[subj][behav]["Mod2"][2*rep]:
                                mod2 = behaviors[subj][behav]["Mod2"][2*rep]
                                text = text + "-" + mod2
                        except (IndexError, KeyError):
                            pass
                        # Calculate string size and build rectangle to fit it
                        size = cv2.getTextSize(text, cv2.FONT_HERSHEY_DUPLEX,
                                               0.7, 1)
                        cv2.rectangle(frame, (10, 8+25*(line-1)),
                                      (10+size[0][0]+10, 8+25*line), (0, 0, 0),
                                      cv2.FILLED)
                        cv2.putText(frame, text, (10, 25+25*(line-1)),
                                    cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 0, 180),
                                    1)
        # Add edited frame to output video
        vid_out.write(frame)
    return "done"
