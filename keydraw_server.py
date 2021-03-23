import itertools
import random
from PIL import Image, ImageDraw
import streamlit as st


def generate_image(triad, chord_num):

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

#    for i, (note, position) in enumerate(all_note_positions.items()):
#        if i%2 == 0:
#            draw.rectangle(position, fill="orange")

    source_img = Image.open("keyboard.png")
    draw = ImageDraw.Draw(source_img)
    for i,note in enumerate(triad):
        print (note)
        position = all_note_positions[note]
        draw.rectangle(position, fill="orange")

    return source_img
#    outname = 'output_' + str(chord_num)
#    source_img.save(outname, "png")


st.title('Random chord progression generator')
seq_len = st.number_input('sequence length (1-6)', min_value=2, max_value=6, value=4)

#random_choice = st.radio(label='Manual or Random Root Note', options=['Manual', 'Random'], value='Random')
random_choice = st.selectbox('Manual or Random Root Note', ['Manual', 'Random'], index=1)

if random_choice == 'Manual':
    input_note = st.radio(label='Root Note',options=['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab'])

if st.button('Generate'):
    notes = ['A4', 'Bb4', 'B4', 'C4', 'Db4', 'D4', 'Eb4', 'E3', 'F3', 'Gb3', 'G3', 'Ab4']

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

    #major, minor triads

    chord_progression = [random.choice(range(0,7)) for i in range(0,seq_len)]
#    chord_progression = range(0,7)

    if random_choice == 'Random':
        input_note = random.choice(notes)

    else:
        note_sels = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']
        index_pos = note_sels.index(input_note)
        input_note = notes[index_pos]
        print ("**********", input_note)
#    input_note = "A4"
#    input_note = 'Ab4'

    print ('randomly chosen note:', input_note, chord_progression)
    st.write('Randomly Chosen Root Note:' , input_note[:-1], )
    st.write('Randomly Chosen Chord Progression:', ', '.join([str(i+1) for i in chord_progression]))



    note_scale = scales[input_note]
    upper_scale = [i[:-1]+str(int(i[-1])+1) for i in note_scale]
    print (note_scale)
    print (upper_scale)



    two_octave_scale = note_scale + upper_scale
    print (two_octave_scale)


    triads_dict = {i:two_octave_scale[i::2][:3] for i in range(0, 7)}
    print ("triads:")
    for num, triad in triads_dict.items():
        print (num, triad)

    print ("")
    print ("chord progression", chord_progression)

    for i, chord in enumerate(chord_progression):
        print (triads_dict[chord])
        img = generate_image(triads_dict[chord], i)
        img = img.resize((img.size[0], 125))

        st.image(img)

#    for num, triad in triads_dict.items():
#        st.write('triad #' + str(num+1) + ', '.join(triad))
