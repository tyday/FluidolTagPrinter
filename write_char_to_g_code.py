import json, os, subprocess,sys

CWD = sys.path[0]
OUTPUT_FILE = 'g_code_output.ngc'
OUTPUT_FILE_PATH = os.path.join(CWD, OUTPUT_FILE)
SPACING = 0.0125
CENTERED = True
Z_HEIGHT_ENGAGED = -0.005
Z_HEIGHT_DISENGAGED = 0.25

current_gcode = []

POSITIONS_ENUM = {
    0:'style',
    1:'serial',
    2:'shaft'
}
TAG_TYPES = [
    ("Tag_large", "Large Tag"),
    ("Tag_small", "Small Tag"),
    ("Tag_special", "Special Tag"),
]
TAG_DEFINITIONS = {
    "Tag_large": {
        'name': 'Large Tag',
        'local_origin': {
            'x':0.5,
            'y':0.5,
        },
        'slots': [
            'style',
            'serial',
            'shaft'
        ],
        'style': {
            'y': 0.3346457,
            'x1': 0.7480315,
            'x2': 2.515748
        },
        'serial': {
            'y': 0.1968504,
            'x1': 0.6692913,
            'x2': 1.377953
        },
        'shaft': {
            'y': 0.1968504,
            'x1': 1.889764,
            'x2': 2.519685
        },
        'font': 'isocp2__0p11.json'
    },
    "Tag_small": { 
        'name': 'Small Tag',
        'local_origin': {
            'x':3.75,
            'y':0.5,
        },       
        'slots': [
            'style',
            'serial',
            'shaft'
        ],
        'style': {
            'y': 0.2952756,
            'x1':0.7283465,
            'x2': 2.125984
        },
        'serial': {
            'y': 0.1574803,
            'x1': 0.5905512,
            'x2': 1.259843
        },
        'shaft': {
            'y': 0.1574803,
            'x1': 1.653543,
            'x2': 2.283465
        },
        'font': 'isocp2__0p10.json'
    },
    "Tag_special": {
        'name': 'Special Tag',
        'local_origin': {
            'x':6.75,
            'y':0.5,
        },
        'slots': [
            'serial',
            'shaft'
        ],
        'serial': {
            'y': 0.5211,
            'x1': 0.0572,
            'x2': 1.1038
        },
        'shaft': {
            'y': 0.08267717,
            'x1': 0.0572,
            'x2': 1.1038
        },
        'font': 'isocp2__0p11.json'
    }
}





def handle_cnc_move(code, current_location, current_gcode):
    current_gcode.append(f"{code[0]} X{current_location['x'] } Y{current_location['y']} Z{current_location['z']}")


def handle_G0G1(code, local_origin, current_location, current_gcode):
    # local_origin = origin.copy()
    max_X = 0
    for i in code:
        if i[0] == 'X':
            current_location['x'] = local_origin['x'] + float(i[1:])
            if current_location['x'] > max_X:
                max_X = current_location['x']
        elif i[0] == 'Y':
            current_location['y'] = local_origin['y'] + float(i[1:])
        elif i[0] == 'Z':
            current_location['z'] = float(i[1:])

    
    handle_cnc_move(code, current_location, current_gcode)
    return max_X


def handle_GCODE(code, origin, current_gcode):
    # code = code.split()
    max_width = 0
    current_location = origin.copy()
    for item in code:
        item = item.split()
        if item == []:
            pass
        elif item[0] == 'G0' or item[0] == 'G1':
            # print(item)
            width = handle_G0G1(item, origin, current_location, current_gcode)
            if width > max_width:
                max_width = width
    return max_width

def get_tag_type():
    while True:
        print("\nSelect tag type (or 'q' to quit)")
        for i in range(len(TAG_TYPES)):
            print(f'{i+1}) {TAG_TYPES[i][1]}')
        selection = input()
        if selection.capitalize() == 'Q':
            return None
        elif not selection.isnumeric():
            print("Must select a number")
        elif int(selection) < 1 or int(selection) > len(TAG_TYPES):
            print(f"Number must correspond to tag code")
        else:
            return TAG_TYPES[int(selection)-1][0]
        print()

def print_to_slot(tag_type, slot, text, current_gcode):
    origin =  {'x': 0.0, 'y': 0.0, 'z': 0.0}
    origin['x'] = tag_type[slot]['x1']
    origin['y'] = tag_type[slot]['y']
    origin['z'] = Z_HEIGHT_DISENGAGED
    for character in text:
        character = str(ord(character))
        # print(GCODES[character])
        GCODES = {}
        with open(os.path.join(CWD,tag_type['font']), 'r') as f:
            GCODES = json.load(f)
        width = handle_GCODE(GCODES[character], origin, current_gcode)
        origin['x'] = width + SPACING
    # if origin['x'] > tag_type[slot]['x2']:
    #     print("Text has too many characters")
    return tag_type[slot]['x2'] - origin['x']

def move_to_position(tag_type, current_gcode, remaining_space, center=True):
    local_origin = tag_type['local_origin']
    new_gcode = []
    # for j in range(len(current_gcode)):
    for code in current_gcode:
        # code = current_gcode[j]
        current_location = {'x': 0.0, 'y': 0.0, 'z': 0.0}
        for i in code.split(' '):
            if i[0] == 'X':
                current_location['x'] = local_origin['x'] + float(i[1:])
                if center:
                    current_location['x'] += remaining_space/2
                # if current_location['x'] > max_X:
                #     max_X = current_location['x']
            elif i[0] == 'Y':
                current_location['y'] = local_origin['y'] + float(i[1:])
            elif i[0] == 'Z':
                current_location['z'] = float(i[1:])
        new_gcode.append(f"{code.split(' ')[0]} X{current_location['x'] } Y{current_location['y']} Z{current_location['z']}")
    return new_gcode

def get_text(tag_type,slot):
    getting_text = True
    remaining_space = 0
    current_gcode = []
    
    while getting_text:
        current_gcode = []
        text = input(f"Please enter {slot.capitalize()}: ")
        if text.capitalize() == 'Q':
            break
        remaining_space = print_to_slot(tag_type,slot,text,current_gcode)
        if remaining_space < 0:
            print("Text is too long, please enter something shorter.\n")
        else:
            getting_text = False
    return (current_gcode, remaining_space)

if __name__ == '__main__':
    #####################
    # Getting this to work on ms store python debugging
    print(CWD)
    print("sys:", sys.path[0])

    ##############################
    while True:
        tag_type = get_tag_type()
        if tag_type == None:
            break
        tag_type = TAG_DEFINITIONS[tag_type]

        origin = {'x': 0.0, 'y': 0.0, 'z': 0.0}
        while True:
            print(f"\nEditing tag type: {tag_type['name']}.")
            exit_tag =  input("[Enter] to continue or 'q' to return to Tag selection:\n")
            if exit_tag.capitalize() == 'Q':
                break
            total_gcode = ['%','G90 G17 G20'] # G20 indicates using English measurements
            for slot in tag_type['slots']:
                getting_text = True
                remaining_space = 0
                current_gcode, remaining_space = get_text(tag_type, slot)
                    
                # Use remaining text to center the current g_code
                # Add remaining_text/2 to each x in current_gcode
                current_gcode = move_to_position(tag_type, current_gcode, remaining_space, CENTERED)

                # Add current_gcode to total_gcode
                total_gcode += current_gcode
            total_gcode += [f'G1 Z{2* Z_HEIGHT_DISENGAGED}', f'G0 X0.0 Y0.0','%']
            print("GCode saved to", OUTPUT_FILE_PATH)
            with open(OUTPUT_FILE_PATH, 'w') as f:
                for line in total_gcode:
                    f.write(line+'\n')
                    
            command = [r"C:\Program Files (x86)\CNC USB Controller\CNCUSBController.exe",
                       os.path.join(CWD, OUTPUT_FILE_PATH)]
            command = [r"C:\Program Files\Notepad++\notepad++.exe", os.path.join(CWD, OUTPUT_FILE_PATH)]
            subprocess.Popen(command, shell=True)
