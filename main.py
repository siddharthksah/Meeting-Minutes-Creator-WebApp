# @author Siddharth
# @website www.siddharthsah.com

# importing the necessary packages

import streamlit as st
import pyaudio
import wave
from summarizer import Summarizer

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

favicon = './favicon.png'
st.set_page_config(page_title='Meeting Minutes Generator', page_icon = favicon, initial_sidebar_state = 'auto')
# favicon being an object of the same kind as the one you should provide st.image() with (ie. a PIL array for example) or a string (url or local file path)

hide_footer_style = """
    <style>
    .reportview-container .main footer {visibility: hidden;}    
    """
st.markdown(hide_footer_style, unsafe_allow_html=True)

st.write("""
## Meeting Minutes Generator
""")

def record(duration):
    filename = "recorded.wav"
    chunk = 1024
    FORMAT = pyaudio.paInt16
    channels = 1
    sample_rate = 44100
    record_seconds = duration
    p = pyaudio.PyAudio()
    # open stream object as input & output
    stream = p.open(format=FORMAT,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    output=True,
                    frames_per_buffer=chunk)
    frames = []
    print("Recording...")
    for i in range(int(44100 / chunk * record_seconds)):
        data = stream.read(chunk)
        frames.append(data)
    print("Finished recording.")
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(filename, "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(sample_rate)
    wf.writeframes(b"".join(frames))
    wf.close()
    audio = "recorded.wav"


def transcribe():
    import speech_recognition as sr

    # Initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()

    # Reading Audio file as source
    # listening the audio file and store in audio_text variable

    with sr.AudioFile('recorded.wav') as source:
        audio_text = r.listen(source)

        # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
        try:

            # using google speech recognition
            text = r.recognize_google(audio_text)
            print('Converting audio transcripts into text ...')
            print(text)
            st.write(text)

        except:
            print('Sorry.. run again...')



st.sidebar.title("Duration")
duration = st.sidebar.slider("Recording duration in seconds", 0.0, 100.0, 5.0)

#duration = 5

#duration = st.number_input('Insert a number')



if st.button("Start Recording"):

    with st.spinner("Recording started..."):
        #st.markdown("![Alt Text](https://icons8.com/vue-static/landings/animated-icons/icons/sound/sound_200.gif)")
        record(duration)
        # audio_file = open('recorded.wav', 'rb')
        # audio_bytes = audio_file.read()
        # st.audio(audio_bytes, format='audio/ogg')


    st.write('Audio Clip Saved!')
    st.write('Transcribing the speech to text now')
    st.write('Please wait...')
    transcription = transcribe()
    print(transcription)

    st.write('Creating summary now...')
    model = Summarizer()
    st.write(model(str(transcription)))






st.write('\n')
st.write('\n')
st.write('\n')

st.write("""
#### Made with :heart: by Siddharth """)
# st.markdown(
#     """<a href="https://www.siddharthsah.com/">siddharthsah.com</a>""", unsafe_allow_html=True,
# )
link = '[siddharthsah.com](http://www.siddharthsah.com/)'
st.markdown(link, unsafe_allow_html=True)