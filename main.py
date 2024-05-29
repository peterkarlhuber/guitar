import streamlit as st


NOTES = ["B#/C", "C#/Db", "D", "D#/Eb", "E/Fb", "E#/F", "F#/Gb", "G", "G#/Ab", "A", "A#/Bb", "B/Cb"]


MODE_DICT = {
    "Ionian (Major)": ["1", "2", "3", "4", "5", "6", "7"],
    "Dorian": ["1", "2", "b3", "4", "5", "6", "b7"],
    "Phrygian": ["1", "b2", "b3", "4", "5", "b6", "b7"],
    "Lydian": ["1", "2", "3", "#4", "5", "6", "7"],
    "Mixolydian": ["1", "2", "3", "4", "5", "6", "b7"],
    "Aeolian (Minor)": ["1", "2", "b3", "4", "5", "b6", "b7"],
    "Locrian": ["1", "b2", "b3", "4", "b5", "b6", "b7"],
}


def get_notes(note):
    for idx in range(len(NOTES)):
        if any([note == n_ for n_ in NOTES[idx].split("/")]):
            break
    return [note.split("/")[-1]] + NOTES[idx + 1:] + NOTES[:idx]


def get_tones(notes):
    return [notes[0], notes[2], notes[4], notes[5], notes[7], notes[9], notes[11]]


def get_semitones(notes):
    return [notes[1], notes[3], notes[6], notes[8], notes[10]]


def clear_notes(notes):
    notes_cleaned = []
    for n in notes:
        if "/" in n:
            n_sharp, n_flat = n.split("/")
            if n_sharp[0] in notes_cleaned[-1]:
                notes_cleaned.append(n_flat)
            else:
                notes_cleaned.append(n_sharp)
        else:
            notes_cleaned.append(n)
    return notes_cleaned


def get_scale(mode, tones, semitones):
    scale = []
    for n in MODE_DICT[mode]:
        if n.startswith("b"):
            note = semitones[int(n[1]) - 3 + int(int(n[1]) <= 4)]
        elif n.startswith("#"):
            note = semitones[int(n[1]) - 1 - int(int(n[1]) >= 4)]
        else:
            note = tones[int(n) - 1]
        scale.append(note)
    return scale


def get_major_tonic(tonic, mode):
    for idx, m in enumerate(MODE_DICT.keys()):
        if mode == m:
            break
    scale = get_mode_scale(tonic, mode)
    return scale[-idx]


def get_chords(tonic, seventh=False):
    notes = clear_notes(get_tones(get_notes(tonic)))
    chords = []
    for n, a in zip(notes, ["", "m", "m", "", "", "m", "dim"]):
        chords.append(n + a)
    if seventh:
        add = ["maj7", "7", "7", "maj7", "7", "7", "m7b5"]
        for i in range(len(chords)):
            chords[i] = chords[i].replace("dim", "") + add[i]
    return chords


def get_mode_scale(tonic, mode):
    notes = get_notes(tonic)
    tones = get_tones(notes)
    semitones = get_semitones(notes)
    scale = get_scale(mode, tones, semitones)
    return clear_notes(scale)


def get_mode_chords(tonic, mode, seventh=False):
    chords = get_chords(get_major_tonic(tonic, mode), seventh=seventh)
    for idx, c in enumerate(chords):
        if tonic in c:
            break
    return chords[idx:] + chords[:idx]


def get_info(tonic, mode):
    return {
        "tonic": tonic,
        "mode": mode,
        "scale": get_mode_scale(tonic, mode),
        "chords": get_mode_chords(tonic, mode),
        "7th_chords": get_mode_chords(tonic, mode, seventh=True),
        "major_tonic": get_major_tonic(tonic, mode)
    }


st.title("Major Modes & Scales")
st.divider()

col1, col2, col3 = st.columns(3, gap="large")
tonic = col1.selectbox("Tonic", ["C", "D", "E", "F", "G", "A", "B"])
accidental = col2.selectbox("Accidental", ["", "#", "b"])
mode = col3.selectbox("Mode", MODE_DICT.keys())
st.divider()

info = get_info(tonic+accidental, mode)

st.markdown("**Tonic:**")
st.markdown(info["tonic"])

st.markdown("**Mode:**")
st.markdown(info["mode"])

st.markdown("**Major Tonic:**")
st.markdown(info["major_tonic"])

st.markdown("**Scale:**")
st.markdown(" - ".join(info["scale"]))

st.markdown("**Chords:**")
st.markdown(" - ".join(info["chords"]))

st.markdown("**Dominant Chords:**")
st.markdown(" - ".join(info["7th_chords"]))

st.divider()
st.link_button("Guitar Chords", "https://www.guitartricks.com/chords")
