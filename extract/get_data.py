"""library tools for reading and understanding the JSON"""
import json


def get_conversations(filename):
    """read a JSON hangouts file and check the conversations within.

    Args:
        filename (str): path to the file.

    Returns:
        list of str: the names of the conversations, in the same order as
            in the JSON file.
    """
    with open(filename, 'r') as fp:
        data = json.load(fp)
        convos = data['conversation_state']
    all_names = []
    for conv in convos:
        conv = conv['conversation_state']['conversation']
        # does if have a name?
        if 'name' in conv:
            name = conv['name']
        else:
            # get all the people in the conv
            people_names = [person['fallback_name']
                            for person in conv['participant_data']]
            name = ','.join(people_names)
        all_names.append(name)
    return all_names


def load_simplified_conversation_text(filename, conv_number):
    """loads the fairly convoluted json produced by takeouts and
    strips it back to the essentials. Also ignores all events that
    aren't text.

    Args:
        filename (str): path to the JSON file to read.
        conv_number (int): the conversation number. Use `get_conversations`
            to see what number it should be.
    """
    pass
