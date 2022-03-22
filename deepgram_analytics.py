import asyncio
from deepgram import Deepgram
from dotenv import load_dotenv
from typing import Dict
import os

load_dotenv()

PATH_TO_FILE = 'premier_broken-phone.mp3'

async def compute_speaking_time(transcript_data: Dict) -> None:
   if 'results' in transcript_data:
       transcript = transcript_data['results']['channels'][0]['alternatives'][0]['words']

       total_speaker_time = {}
       speaker_words = []
       current_speaker = -1

       for speaker in transcript:
           speaker_number = speaker["speaker"]

           if speaker_number is not current_speaker:
               current_speaker = speaker_number
               speaker_words.append([speaker_number, [], 0]) # 0 is the total amount of time per phrase for each speaker

               try:
                   total_speaker_time[speaker_number][1] += 1
               except KeyError:
                   total_speaker_time[speaker_number] = [0,1]

     
           get_word = speaker["word"]
           speaker_words[-1][1].append(get_word)

           total_speaker_time[speaker_number][0] += speaker["end"] - speaker["start"] # [0] gets the total time
           speaker_words[-1][2] += speaker["end"] - speaker["start"]

       for speaker, words, time_amount in speaker_words:
           print(f"Speaker {speaker}: {' '.join(words)}")
           print(f"Speaker {speaker}: {time_amount}")

       for speaker, (total_time, amount) in total_speaker_time.items(): # (unpacks)key goes into total_time, value goes into amount
           print(f"Speaker {speaker} avg time per phrase: {total_time/amount} ")
           print(f"Total time of conversation: {total_time}")

   return transcript


async def main():
   deepgram = Deepgram(os.getenv("DEEPGRAM_API_KEY"))

   with open(PATH_TO_FILE, 'rb') as audio:
       source = {'buffer': audio, 'mimetype': 'audio/mp3'}
       transcription = await deepgram.transcription.prerecorded(source, {'punctuate': True, 'diarize': True})

       speakers = await compute_speaking_time(transcription)
  

asyncio.run(main())
