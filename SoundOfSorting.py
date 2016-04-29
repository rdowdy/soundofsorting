gArray = [12, 5, 32, 65, 34, 78, 4, 86, 3, 6, 54, 94, 45, 19, 82, 1]
gArray2 = [12, 5, 32, 65, 34, 78, 4, 86, 3, 6, 54, 94, 2, 93, 57, 52, 4, 10, 14, 543, 16, 19, 14, 79]
gNotes = []

mask = 0xff

#################################
# Scale Defintions
#
# each degree of the scale
# is defined by its distance
# from the root in semitones
##################################
majorKey = {
    1 : 0,
    2 : 2,
    3 : 4,
    4 : 5,
    5 : 7,
    6 : 9,
    7 : 11,
    8 : 12
}

# C, D, E, G, A
majorPentatonic = {
    1 : 0,
    2 : 2,
    3 : 4,
    4 : 7,
    5 : 9
}

#############################
## Bubble Sort
#############################
def bubbleSort(a):
    n = len(a)
    gNotes = []

    for i in range(0, n):
        for j in range(0, n-1):
            if a[j] > a[j+1]:
                temp = a[j]
                a[j] = a[j+1]
                a[j+1] = temp
                addNote(j)
                addNote(j+1)
            # end if
        # end for
    # end for
    return a
#############################

#############################
## Merge Sort
#############################
def mergeSort(a, ga):
    n = len(a)

    if n == 1:
        addNote(ga.index(a[0]))
        return a
    # end if 

    l1 = a[0:n/2]
    l2 = a[n/2:n]

    l1 = mergeSort(l1, ga)
    l2 = mergeSort(l2, ga)

    return merge(l1, l2, ga)

##############
# merge helper
##############

def merge(a, b, ga):
    c = []

    while(len(a) > 0 and len(b) > 0):
        if(a[0] > b[0]):
            addNote(ga.index(a[0]))
            addNote(ga.index(b[0]))

            c.append(b[0])
            b = b[1:]
        else:
            addNote(ga.index(a[0]))
            addNote(ga.index(b[0]))

            c.append(a[0])
            a = a[1:]
        # end if
    # end while

    while(len(a) > 0):
        #addNote(ga.index(a[0]))

        c.append(a[0])
        a = a[1:]
    # end while 

    while (len(b) > 0):
        #addNote(ga.index(b[0]))

        c.append(b[0])
        b = b[1:]
    # end while
    return c
#############################

#############################
## Music/MIDI
#############################
def addNote(val):
    gNotes.append((val % 8) + 1)

# takes a number mod 8
# converts it to a note
# as such:
# 1: root note of key
# ...
# 8: root note of key (one octave higher)
#
# for the first iteration, as a proof of concept
# I'll assume the key of C
# with C4 (0x3C) as the root note
def numToNoteHex(num):
    hexVal = majorKey[num] + 0x3C
    return hexVal

##############
# Creates a MIDI file 
# given an array of notes
# assumed 1 track
#
# fileName will be the name
# used for the .mid file
#
# ticksPerQuarterNote is the number
# of ticks per quarter note, aka
# the tempo. Ticks is an arbitrary
# unit, but I think it is somehow
# correlated to the OS clock
#
# notes is an array of musical notes
# corresponding to the degree of the 
# scale being used (1 is root)
##############
def createMIDIfile(fileName, ticksPerQuarterNote, notes):
    if fileName[-4:] != '.mid':
        fileName += '.mid'
    ##############################
    ## Create MIDI Header
    ##############################
    midiHeader = []
    # first 4 bytes are
    # hex for 'MThd'
    # required for all MIDI files
    midiHeader += bytearray([0x4d, 0x54, 0x68, 0x64])
    # the next 4 bytes
    # contain the size of 
    # the remaining header
    # which is always 6 bytearray
    midiHeader += bytearray([0x00, 0x00, 0x00, 0x06])
    # the next 2 bytes
    # contain the format
    midiHeader += bytearray([0x00, 0x01])
    # the next 2 bytes
    # contain the number of tracks
    # in MIDI
    midiHeader += bytearray([0x00, 0x01])
    # the next 2 bytes
    # will be the speed of the music
    ticks = [0x00] * 2
    ticks[0] = (ticksPerQuarterNote >> 8) & mask
    ticks[1] = ((ticksPerQuarterNote << 8) >> 8) & mask

    midiHeader += bytearray(ticks)

    ##############################
    ## Track Header, Track Data, and Track Out
    ##############################

    trackHeader = []
    trackData = []
    # track header
    trackHeader += bytearray([0x4d, 0x54, 0x72, 0x6b])

    # for proof of concept
    # im just gonna do
    # quarter note length notes
    for note in notes:
        # time units
        trackData += bytearray([0x20])
        # Note On 0x90
        trackData += bytearray([0x90])
        # Pitch
        trackData += bytearray([numToNoteHex(note)])
        # Volume
        trackData += bytearray([0x60])

        # hold the note for quarter note length
        trackData += bytearray([0x7f])
        trackData += bytearray([numToNoteHex(note)])
        trackData += bytearray([0x00])
    #end for

    # track out
    trackData += bytearray([0x00, 0x0ff, 0x2f, 0x00])

    # put the track size into the header
    trackSize = len(trackData)
    trackSizeBytes = [0x00] * 4

    trackSizeBytes[0] = (trackSize >> 24) & mask
    trackSizeBytes[1] = ((trackSize << 8) >> 24) & mask
    trackSizeBytes[2] = ((trackSize << 16) >> 24) & mask
    trackSizeBytes[3] = ((trackSize << 24) >> 24) & mask

    trackHeader += bytearray(trackSizeBytes)

    MIDI = midiHeader + trackHeader + trackData

    ##############################
    ## Write the MIDI file
    ##############################

    f = open(fileName, 'wb')
    f.write(bytearray(MIDI))
    f.close()

    return fileName


print "=========================================="
print "===== BUBBLE SORT"
print "=========================================="
print bubbleSort(gArray2)
print "Number of notes:", len(gNotes)
print "MIDI file name:", createMIDIfile("Bubble_Sort.mid", 1024, gNotes)
print "=========================================="

gNotes = []
print "=========================================="
print "===== MERGE SORT"
print "=========================================="
print mergeSort(gArray2, gArray2)
print "Number of notes: ", len(gNotes)
print "MIDI file name:", createMIDIfile("Merge_Sort.mid", 1024, gNotes)
print "=========================================="