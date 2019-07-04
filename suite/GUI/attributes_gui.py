# Import Python packages
import os

# List of interesting pedestrian attributes
ATTRIBUTES = tuple(sorted(("sunglasses", "glasses", "phone_ear", "phone_hand",
                           "headset", "hat", "umbrella", "crutches/cane",
                           "wheelchair", "stroller", "bike", "pet", "hood",
                           "carry_baby", "kid", "young", "adult", "senior",
                           "group")))


def new_dict(subject, main_dict):
    """ This function creates a new dictionary for a subject and initializes
    all values to "no".

    :param subject: str
        Name of the subject.
    :param main_dict: dict
        Dictionary containing all subject dictionaries.
    :return: updated main_dict
    """

    main_dict[subject] = dict()
    for element in ATTRIBUTES:
        main_dict[subject][element] = "no"
    return main_dict


def get_subjects(**params):
    """ This function reads the subjects from an BORIS output file.

    :param params:
        Parameters introduced by the user (BORIS data/output paths).
    :return: list of loaded subjects.
    """

    print(f"[INFO] Working...")
    with open(params["boris_path"], "r") as in_tsv:
        lines = in_tsv.readlines()
        for line in lines:
            # Locate video information
            try:
                line.index("Player #1")
                player_idx = lines.index(line)
            except ValueError:
                pass
            # Locate line before observations
            try:
                line.index("Time\tMedia")
                props_idx = lines.index(line)
            except ValueError:
                pass
        # clip_name = lines[player_idx].split("\t")[1]
        # Store properties names
        props = lines[props_idx].split("\t")
        subj_idx = props.index("Subject")
        # Read entire matrix of observation data
        vals = lines[props_idx+1:lines.__len__()-1]
        vals = list(map(lambda x: x.split("\t"), vals))
        subjects = []
        # Add subject if it hasn't been added before
        for line in vals.__iter__():
            if not line[subj_idx] in subjects:
                subjects.append(line[subj_idx])
        print("Found subjects:", *subjects, "\n")
        return subjects


def set_attributes(subject, attribs, **params):
    """ This function allows the user to set attributes for a chosen subject.

    :param subject: str
        Subject to set attributes for.
    :param attribs: tuple
        List of affirmative subject attributes.
    :param params: dict
        Parameters introduced by the user (BORIS data/output paths).
    :return: done flag
    """

    print(f"[INFO] Working...")
    # Create a new dictionary for the subject
    super_dict = dict()
    super_dict = new_dict(subject, super_dict)
    # Set chosen attributes to "yes"
    for attrib in attribs:
        super_dict[subject][attrib] = "yes"
    # Load attributes data if file already exists
    in_tsv = os.path.split(params["boris_path"])[1]
    if os.path.exists(params["attrib_path"] + "/" +
                      in_tsv.replace(".tsv", "_attributes.tsv")):
        out_tsv = open(params["attrib_path"] + "/" +
                       in_tsv.replace(".tsv", "_attributes.tsv"), "r+")
        pre_data = out_tsv.read()
        out_data = ""
        if subject in pre_data:
            return "done"
    # Create a new attributes file if it doesn't exist
    else:
        out_tsv = open(params["attrib_path"] + "/" +
                       in_tsv.replace(".tsv", "_attributes.tsv"), "w")
        out_data = "Source TSV:\t" + os.path.split(params["boris_path"])[1]\
                   + "\n"
        out_data += "Attributes:\t" + '\t'.join(ATTRIBUTES) + "\n"
    # Write new attributes data to the file
    for element in super_dict.keys():
        out_data += element + "\t" + '\t'.join(super_dict[element].values())
    out_data += "\n"
    out_tsv.write(out_data)
    out_tsv.close()
    return "done"
