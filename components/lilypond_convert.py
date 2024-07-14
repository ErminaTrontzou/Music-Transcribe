class LilyPondConverter:
    def __init__(self, notes_info):
        self.notes_info = notes_info
        self.note_to_lilypond_pitch = self.generate_note_to_lilypond_pitch()
    
    def generate_note_to_lilypond_pitch(self):
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        suffixes = [",,,", ",,", ",", "", "'", "''", "'''", "''''"]
        note_to_lilypond_pitch = {}

        for octave in range(1, 8):  # generating for octaves 1 to 7
            for note in notes:
                lilypond_suffix = suffixes[octave - 1]
                if '#' in note:
                    lp_note = note.lower().replace('#', 'is') + lilypond_suffix
                else:
                    lp_note = note.lower() + lilypond_suffix
                note_to_lilypond_pitch[f"{note}{octave}"] = lp_note

        note_to_lilypond_pitch['pause'] = 'r'
        return note_to_lilypond_pitch
    
    def duration_to_lilypond(self, duration):
        if duration == 1.0:
            return '4'  # quarter note
        elif duration == 0.5:
            return '8'  # eighth note
        elif duration == 0.25:
            return '16' # sixteenth note
        elif duration == 2.0:
            return '2'  # half note
        elif duration == 4.0:
            return '1'  # whole note
        else:
            if duration < 0.375:
                return '16'
            elif duration < 0.75:
                return '8'
            elif duration < 1.5:
                return '4'
            elif duration < 3:
                return '2'
            else:
                return '1'
    
    def convert(self):
        lilypond_notes = []
        for note_info in self.notes_info:
            note = note_info['note']
            duration = note_info['duration']
            lp_note = self.note_to_lilypond_pitch.get(note, '')
            lp_duration = self.duration_to_lilypond(duration)
            if lp_note and lp_duration:
                lilypond_notes.append(f"{lp_note}{lp_duration}")
        
        lilypond_string = " ".join(lilypond_notes)
        return lilypond_string

    def write_to_file(self, file_name):
        lilypond_string = self.convert()
        with open(file_name, 'w') as file:
            file.write("\\version \"2.20.0\"\n")
            file.write("{\n")
            file.write(lilypond_string)
            file.write("\n}\n")
        print(f"LilyPond file written to {file_name}")

