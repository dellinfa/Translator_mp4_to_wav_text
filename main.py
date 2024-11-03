import speech_recognition as sr
from pydub import AudioSegment
# def transcribe_audio(file_path):
#     # Inizializza il riconoscitore
#     recognizer = sr.Recognizer()
#
#     # Carica il file audio
#     with sr.AudioFile(file_path) as source:
#         audio_data = recognizer.record(source)
#
#     # Trascrivi l'audio in testo
#     try:
#         text = recognizer.recognize_google(audio_data, language='it-IT')
#         return text
#     except sr.UnknownValueError:
#         return "Google Speech Recognition non è riuscito a capire l'audio"
#     except sr.RequestError as e:
#         return f"Errore nella richiesta al servizio Google Speech Recognition; {e}"
#
#
#
#
# def split_audio(file_path, segment_length_ms):
#     audio = AudioSegment.from_wav(file_path)
#     segments = [audio[i:i + segment_length_ms] for i in range(0, len(audio), segment_length_ms)]
#     return segments
#
# # Esempio di utilizzo
# file_path = "path_to_large_audio_file.wav"
# segments = split_audio(file_path, 60000)  # Segmenti di 60 secondi
# for i, segment in enumerate(segments):
#     segment.export(f"segment_{i}.wav", format="wav")
#
#
# transcription = transcribe_audio(file_path)
# print(transcription)


from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import speech_recognition as sr

def split_audio(file_path, segment_length_ms):
    audio = AudioSegment.from_wav(file_path)
    segments = [audio[i:i + segment_length_ms] for i in range(0, len(audio), segment_length_ms)]
    return segments

def transcribe_audio_segment(segment_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(segment_path) as source:
        audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data, language='it-IT')
        return text
    except sr.UnknownValueError:
        return "Google Speech Recognition non è riuscito a capire l'audio"
    except sr.RequestError as e:
        return f"Errore nella richiesta al servizio Google Speech Recognition; {e}"

def transcribe_large_audio(file_path, segment_length_ms=120000):
    print('Segmento l audio')
    segments = split_audio(file_path, segment_length_ms)
    print('entro nel for per trascrivere ogni singolo segmento')
    transcription = ""
    for i, segment in enumerate(segments):
        print('Segmento {} trascritto'.format(i))
        segment_path = f"segment_{i}.wav"
        segment.export(segment_path, format="wav")
        transcription += transcribe_audio_segment(segment_path) + " "
    return transcription

def convert_mp4_to_wav(mp4_file_path, wav_file_path):
    # Carica il file video
    video = VideoFileClip(mp4_file_path)
    # Estrai l'audio e salvalo come file WAV
    video.audio.write_audiofile(wav_file_path)


# Esempio di utilizzo
mp4_file_path = "lezione 20 31 ottobre.mp4"
wav_file_path = "output_audio {}.wav".format(mp4_file_path)
convert_mp4_to_wav(mp4_file_path, wav_file_path)
transcription = transcribe_large_audio(wav_file_path)

with open("transcription {}.txt".format(mp4_file_path), "w", encoding="utf-8") as f:
    f.write(transcription)

print(transcription)
