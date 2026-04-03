import asyncio

from dotenv import load_dotenv
import speech_recognition as sr

from openai.helpers import LocalAudioPlayer
from openai import OpenAI, AsyncOpenAI

load_dotenv()

client = OpenAI()
asyncio_client = AsyncOpenAI()

async def tts(speech: str):
    async with asyncio_client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        instructions="Speak in a cheerful and positive tone.",
        input=speech,
        response_format="pcm"
    ) as response:
        await LocalAudioPlayer().play(response)
def main():
    r = sr.Recognizer()  #?--> Speech to text

    with sr.Microphone() as source:  #?mic acess
        r.adjust_for_ambient_noise(source)  #? remove backgroud noise
        r.pause_threshold = 2  

        SYSTEM_PROPT = """
                You are an expert voice agent. you are given the transcript of what user has said using voice.
                You need to output as if you are an voice agent. you need to understand the user query and respond accordingly. you can also ask follow up questions if you need more information from the user.
            """
        messages = [{
                        "role": "system",
                        "content": SYSTEM_PROPT
                    },]
        while True:

            print("Speack something")
            audio = r.listen(source)
            

            print("processing audio")
            stt = r.recognize_google(audio)

            print("You said", stt)

            messages.append({
                "role": "user",
                "content": stt
            })
            response =client.chat.completions.create(
                model="gpt-4.1-nano",
                messages=messages
            )
            print("Agent response", response.choices[0].message.content)
            asyncio.run(tts(speech=response.choices[0].message.content))

main()