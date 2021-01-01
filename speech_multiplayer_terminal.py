import speech_recognition as sr
import keyboard
import pyaudio
import wave
import pyttsx3


# Say loud

def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


# Record audio


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100


def record():

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Listening...")

    frames = []

    while keyboard.is_pressed('space') != True:
        data = stream.read(CHUNK)
        frames.append(data)
    print("Stopped Listening..")

    sample_width = p.get_sample_size(FORMAT)

    stream.stop_stream()
    stream.close()
    p.terminate()

    return sample_width, frames


def record_to_file(file_path):
    wf = wave.open(file_path, 'wb')
    wf.setnchannels(CHANNELS)
    sample_width, frames = record()
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


# Speech recognition
def speechRecog():
    r = sr.Recognizer()
    with sr.WavFile("word.wav") as source:
        # Listening from audio file
        audio = r.listen(source)

    # text from audio using google speech recognition system
    try:
        text = r.recognize_google(audio)
        # print("Google Speech Recognition Output : "+text)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio !!!")
    except:
        print(
            "could not request result from google speech recognition service; {0}".format(e))
    # createFrame(text)


'''
def speechRecogAudio():
    # r=sr.Recognizer()
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say Something...")
        audio = r.listen(source)

    # text from audio using google speech recognition system
    try:
        text = r.recognize_google(audio)
        print("Google Speech Recognition Output : "+text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio !!!")
    except:
        print(
            "could not request result from google speech recognition service; {0}".format(e))
    # createFrame(text)
'''

# Input players information


def playerInfo():
    print("Enter no of players : ", end="")
    say("Enter no of players")
    n = int(input())
    x = 1
    name = []
    while(x <= n):
        print("Enter player-"+str(x)+" name : ", end="")
        say("Enter name of player "+str(x))
        name.append(input())
        x += 1
    return n, name

# Instructions


def instruction():
    print("INSTRUCTIONS :")
    say("INSTRUCTIONS")
    print("Please speak word(s) into the microphone")
    say("Please speak words into the microphone")
    print('Press space bar to say next word')
    say('Press space bar to say next word')

# Game Module


def game(n, name):
    wolist = []  # list for previously played player
    wplist = []  # list for current played player

    # Game start for player 1
    print("TURN FOR PLAYER "+name[0]+" :")
    say("TURN FOR PLAYER "+name[0])
    record_to_file('word.wav')
    text = speechRecog()
    # text = input()
    wplist.append(text.lower())
    wolist = wplist
    wplist = []
    # print("WORD SAID NOW & TO BE SAID : ", end="")
    # print(wolist)

    # Game for next turns
    i = 0
    j = 1
    won = False
    lost = []
    while True:
        print("TURN FOR PLAYER "+name[j]+" :")
        say("TURN FOR PLAYER "+name[j])
        eliminate = False

        while True:

            # Check for the words said by previous player
            if(i < len(wolist)):
                print("Say the next word")
                say("Say the next word")
                record_to_file('word.wav')
                text = speechRecog()
                # text = input()
                # Check if current player is saying same as previous player
                if(wolist[i] == text.lower()):
                    wplist.append(text.lower())
                    i = i+1
                else:
                    i = 0
                    print("You said wrong word !!!!")
                    say("You said wrong word")
                    print(name[j]+" LOST !!!")
                    say(name[j]+" LOST")
                    eliminate = True
                    lost.append(j)
                    if(len(lost) == n-1):
                        won = True
                    break
            # If all words are said by current player those was said by previous player
            # Then we have to record another new word
            else:
                record_to_file('word.wav')
                text = speechRecog()
                # text = input()
                # Check if current player's newly said word is already said by another player
                if(text.lower() in wplist):
                    print("Your new word already exists !!!!")
                    say("Your new word already exists")
                    print(name[j]+" LOST !!!")
                    say(name[j]+" LOST")
                    eliminate = True
                    lost.append(j)
                    if(len(lost) == n-1):
                        won = True
                # If newly said word is not said previously then success
                else:
                    wplist.append(text.lower())
                i = 0
                break
        # print("WORDS SAID CURRENTLY : ", end="")
        # print(wplist)
        if(eliminate == False):
            wolist = wplist
        wplist = []
        # print("WORD TO BE SAID NOW : ", end="")
        # print(wolist)

        j = (j+1) % n
        while(j in lost):
            j = (j+1) % n
        if(won == True):
            break
    print('#' * 80)
    print(name[j]+" WON THE GAME!")
    say(name[j]+" WON THE GAME")
    print('#' * 80)

# Main function


if __name__ == "__main__":
    # Input players information
    print('#' * 80)
    n, name = playerInfo()
    print(name)

    # Instructions
    print('#' * 80)
    instruction()

    # Game
    print('#' * 80)
    game(n, name)