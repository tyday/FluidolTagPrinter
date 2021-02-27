import json, subprocess

character_dictionary = {}
# for ($num = 32; $num -le 126 ; $num++){
for i in range(32,126):
    letter = chr(i)
    command = ['C:/Users/tyrda/AppData/Local/Programs/Python/Python39/python.exe',
        'C:/Users/tyrda/OneDrive/Documents/Fluidol/CNC/F-Engrave-1.73_src/f-engrave.py',
        '-f',
        'C:/Users/tyrda/OneDrive/Documents/Fluidol/CNC/TagFonts/isocp2__.ttf',
        '-t',
        f'{letter}M',
        '-b']
    process = subprocess.run(command, stdout=subprocess.PIPE)
    gcodeStart = False
    result = process.stdout.decode('utf-8').split('\r\n')
    character_dictionary[i] = result[7:-19]
    # for line in result[11:-19]:
    #     print(line)
    print(i, chr(i))
with open('characters.json', 'w', encoding='utf-8') as f:
    data = json.dumps(character_dictionary)
    f.write(data)