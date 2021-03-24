import itertools
import random
from PIL import Image, ImageDraw
import streamlit as st


def generate_image(note_dict):
    ''' note dict is of hte form: {note:color} '''

    note_list_white = ['E3', 'F3', 'G3','A4', 'B4', 'C4', 'D4', "E4", 'F4', 'G4', 'A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5' ]

    #bkd is the "Black key dictionary"
    #coordinates of a box are the values of the dict for each note. ((upper left), (bottom right))
    bkd = {'Ab4':((223, 90), (255, 142)),
           'Bb4':((268, 90), (300, 142)), 
            'Db4':((360, 90), (391, 142)), 
           'Eb4':((405, 90), (436, 142)),
           'Gb4':((495, 90), (526, 142)),
           'Ab5':((540, 90), (572, 142)),
           'Bb5':((586, 90), (616, 142)),
           'Db5':((677, 90), (709, 142)),
           'Eb5':((723, 90), (754, 142)),
           'Gb5':((812, 90), (844, 142)),
           'G#5':((858, 90), (889, 142)),
           'Gb3':((178, 90), (210, 142)),}

    #say that some flat notes are the same as other sharp notes
    bkd['G#3'] = bkd['Ab4']
    bkd['F#3'] = bkd['Gb3']

    bkd['A#4'] = bkd['Bb4']
    bkd['C#4'] = bkd['Db4']
    bkd['D#4'] = bkd['Eb4']
    bkd['F#4'] = bkd['Gb4']
    bkd['G#4'] = bkd['Ab5']
    bkd['A#5'] = bkd['Bb5']
    bkd['C#5'] = bkd['Db5']
    bkd['D#5'] = bkd['Eb5']
    bkd['F#5'] = bkd['Gb5']

    bkd['Ab6'] = bkd['G#5']

    note_position_d = {}

    #white keys are regularly spaced, so we can just iterate over the keys and add to the x values to define the note coordinate boxes
    y1_white = 172
    y2_white = 222

    new_x1 = 58
    new_x2 = 104

    #get the position for each note
    for note in note_list_white:
        new_x1 += 45.4
        new_x2 +=  45.4
        note_position_d[note] = ((new_x1, y1_white), (new_x2, y2_white))

    #merge the white key dict and black key dict
    all_note_positions = {**note_position_d, **bkd}

    source_img = Image.open("keyboard.png")
    draw = ImageDraw.Draw(source_img)
    for note,color in note_dict.items():
        print (note, color)
        position = all_note_positions[note]
        draw.rectangle(position, fill=color)

    return source_img

def get_passing_notes(scale):
    '''given a scale, return the passing notes'''

    #convert scale ot only use flats
    zc = [key_equivaleny_d[i] if i in key_equivaleny_d else i for i in scale]
    print (zc, '***')
    start = whole_sequence.index(zc[0])
    end = whole_sequence.index(zc[-1]) + 1
    truncated_sequence = whole_sequence[start:end]
    passing_notes = [i  for i in truncated_sequence if i not in zc]
    return passing_notes

st.title('Random chord progression generator')
seq_len = st.number_input('sequence length (1-6)', min_value=2, max_value=6, value=4)

random_choice = st.selectbox('Select Manual or Random major root note', ['Manual', 'Random'], index=1)

if random_choice == 'Manual':
    input_note = st.radio(label='Root Note',options=['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab'])

st.markdown('###')

if st.button('Generate'):
    st.header("Chord progression")

    #get the whole sequence of  keys used 
    whole_sequence = ['E3', 'F3', 'Gb3', 'G3', 'Ab4', 'A4', 'Bb4', 'B4', 'C4', 'Db4', 'D4', 'Eb4','E4', 'F4', 'Gb4', 'G4', 'Ab5', 'A5', 'Bb5', 'B5', 'C5', 'Db5', 'D5','Eb5', 'E5', 'F5', 'Gb5', 'G5', 'Ab6']

    #all root notes
    root_notes = ['A4', 'Bb4', 'B4', 'C4', 'Db4', 'D4', 'Eb4', 'E3', 'F3', 'Gb3', 'G3', 'Ab4']
    major_minor_dict = {1:'I', 2:'ii', 3:'iii', 4:'IV', 5:'V', 6:'vi'}

    #convert between sharp notes and their equivalent flat notes
    key_equivaleny_d = {'G#3':'Ab4',
                        'F#3':'Gb3',
                        'A#4':'Bb4',
                        'C#4':'Db4',
                        'D#4':'Eb4',
                        'F#4':'Gb4',
                        'G#4':'Ab5',
                        'A#5':'Bb5',
                        'C#5':'Db5',
                        'D#5':'Eb5',
                        'F#5':'Gb5',
                        'Ab6':'G#5'}

    #scales of the root notes (keys are same as in root_notes list
    scales = {'A4':['A4', 'B4', 'C#4', 'D4', 'E4', 'F#4', 'G#4'],
              'Bb4':['Bb4', 'C4', 'D4', 'Eb4', 'F4', 'G4', 'A5'],
              'B4':['B4', 'C#4', 'D#4', 'E4', 'F#4', 'G#4', 'A#5'],
              'C4':['C4', 'D4', 'E4', 'F4', 'G4', 'A5', 'B5'],
              'Db4':['Db4', 'Eb4', 'F4', 'Gb4', 'Ab5', 'Bb5', 'C5'],
              'D4':['D4', 'E4', 'F#4', 'G4', 'A5', 'B5', 'C#5'],
              'Eb4':['Eb4', 'F4', 'G4', 'Ab5', 'Bb5', 'C5', 'D5'],
              'E3':['E3', 'F#3', 'G#3', 'A4', 'B4', 'C#4', 'D#4'],
              'F3':['F3', 'G3', 'A4', 'Bb4', 'C4', 'D4', 'E4'],
              'Gb3':['Gb3', 'Ab4', 'Bb4', 'B4', 'Db4', 'Eb4', 'F4'],
              'G3':['G3', 'A4', 'B4', 'C4', 'D4', 'E4', 'F#4'],
              'Ab4':['Ab4', 'Bb4', 'C4', 'Db4', 'Eb4', 'F4', 'G4']}

    #for each root note, store its "tension" and "release" notes in its scale
    scales_tension_release = {i:{'tension':[], 'release':[]} for i,j in scales.items()}

    for note in root_notes:
        #add release notes
        note_scale = scales[note]
        pentatonic = note_scale[:-1] #remove the 7th
        del pentatonic[3] #remove the 4th
        scales_tension_release[note]['release'] = pentatonic

        #add tension notes
        passing_notes = get_passing_notes(note_scale)
        scales_tension_release[note]['tension'] = passing_notes

    #generate random zero-indexed chord progression list, e.g. [0, 3, 2, 1] 
    chord_progression = [random.choice(range(0,6)) for i in range(0,seq_len)]
#    chord_progression = range(0,6)

    if random_choice == 'Random':
        input_note = random.choice(root_notes)

    else:
        #match up the user's selection with the root note list to get an input_note with the octave at the end
        #note_sels and root_notes are in the same order, but note_sels doesn't have the octave number
        note_sels = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']
        index_pos = note_sels.index(input_note)
        input_note = root_notes[index_pos]
        print ("**********", input_note)
#    input_note = "A4"
#    input_note = 'Ab4'

    print ('randomly chosen note:', input_note, chord_progression)
    triad_major_minor = '(' + ', '.join([major_minor_dict[i+1] for i in chord_progression]) + ')'
    print (triad_major_minor)
    st.write('Root Note:' , input_note[:-1], )
    st.write('Random Chord Progression:', ', '.join([str(i+1) for i in chord_progression]), triad_major_minor)

    #generate the two octave scale, give the input note
    note_scale = scales[input_note]
    upper_scale = [i[:-1]+str(int(i[-1])+1) for i in note_scale]
    print (note_scale)
    print (upper_scale)
    two_octave_scale = note_scale + upper_scale
    print (two_octave_scale)

    #create triads_dict, which holds all 6 of the input note's triads
    #it is of the form {triad_number : [note1, note2, note3] }
    #note that it is zero-indexed
    triads_dict = {i:two_octave_scale[i::2][:3] for i in range(0, 6)}
    print ("triads:")
    for num, triad in triads_dict.items():
        print (num, triad)

    print ("")
    print ("chord progression", chord_progression)

    #for each random zero-index chord, make a note_dict and generate/show the image
    #note_dict is just { note : color } where the given note will be painted with the specified color
    for i, chord in enumerate(chord_progression):
        print (triads_dict[chord])
        note_dict = {note:'orange' for note in triads_dict[chord]}
        img = generate_image(note_dict)
        img = img.resize((img.size[0], 125))
        st.image(img)

    st.header("Melody palette")
    st.markdown("- ![tension p](https://via.placeholder.com/15/FF0000/000000?text=+) `tension (passing notes)`", unsafe_allow_html=True)
    st.markdown("- ![release](https://via.placeholder.com/15/0000FF/000000?text=+) `release (major pentatonic scale)`", unsafe_allow_html=True)

    #generate a note_dict to to show the melody palette
    note_dict = {}
    for label,notes in scales_tension_release[input_note].items():
        print (label,notes)
        if label == 'tension':
            for note in notes:
                note_dict[note] = 'red'
        else:
            for note in notes:
                note_dict[note] = 'blue'

    img = generate_image(note_dict)
    img = img.resize((img.size[0], 125))
    st.image(img)
    st.markdown('###')
    st.markdown('[![image link](https://www.buymeacoffee.com/assets/img/bmc-meta-new/new/favicon-32x32.png?version=2021.03.24.06.20.31)](https://www.buymeacoffee.com/rmurray20)')

    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)




