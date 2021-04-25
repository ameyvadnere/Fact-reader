#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Created on: 25/4/21 15:16:30 (IST)
@author: Ameya Vadnere
@version: 1.0.0

Documentation:
    The following script reads randomly selected facts from a text file and speaks them out to the user. It uses
    Google's gTTS module to convert text to speech. The user can input the no. of facts they want to know and 
    they will be able to listen to that many number of facts.
'''

import random                           # For randomly generating facts
from gtts import gTTS                   # Google's Text-to-Speech Library
import os                               # For removal of files
import sys                              # For system operations
from playsound import playsound         # Playing audio files
import keyboard                         # Detecting keyboard inputs

class FactReader:
    FILEPATH = 'facts.txt'                  # The path of the fact file
    language = 'en'                         # Spoken language. Check out https://gtts.readthedocs.io/en/latest/module.html#languages-gtts-lang
    accent_domain = 'ca'                    # Spoken accent. Check out https://gtts.readthedocs.io/en/latest/module.html#languages-gtts-lang
    greeting_1 = 'Hello! How many facts do you want to know today?'     
    greeting_2 = 'Have a nice day!'
    file_not_found_error_sentence = 'The designated file could not be found!'
    empty_file_error_sentence = 'The file is empty!'


    @classmethod
    def get_num_facts(cls) -> int:
        '''
        Takes the number of facts the user wants 
        to listen as input and returns it.

            Parameters:
                None

            Returns:
                int(pressed_key) (int): No. (of facts) input by the user
        '''

        cls.speak(cls.greeting_1)                                   # Say a greeting message.
        while True:
            try:
                pressed_key = keyboard.read_key()
                if ord(pressed_key) in range(ord('1'), ord('9')+1): # If a key from 1-9 is pressed
                    return int(pressed_key)
            except:                                                 # Exit if any other key is pressed.
                cls.speak(cls.greeting_2)                           # Say another greeting message before exiting.
                sys.exit(1)                         


    @classmethod
    def get_line_count(cls, FILEPATH: str) -> int:
        '''
        Takes the path of the file as input and
        returns the number of lines in the file.

            Parameters:
                FILEPATH (str): Path of the file
            
            Returns:
                line_count (int): The no. of lines in the file
        '''

        try:
            with open(FILEPATH, encoding='utf-8') as f:
                line_count = 0
                for line in f:
                    line_count += 1
                
            if line_count == 0:                                     # If file is empty, speak out the error message, then exit.
                cls.speak(cls.empty_file_error_sentence)
                sys.exit(1)

            return line_count
                
        except FileNotFoundError:                                   # If file is not found, speak out the error message, then exit
            cls.speak(cls.file_not_found_error_sentence)
            sys.exit(1)
    

    @classmethod
    def get_facts(cls, FILEPATH: str, num_facts: int) -> list:
        '''
        Takes the file path and the no. of facts, then randomly generates num_facts 
        no. of integers, which are used to extract facts randomly from the file.

            Parameters:
                FILEPATH (str): Path of the file
                num_facts (int): No. of facts to be generated
            
            Returns:
                facts (list): List of randomly generated facts
        '''

        line_count = cls.get_line_count(FILEPATH)                               # Get line count
        rn_list = sorted(random.sample(range(0, line_count-1), num_facts))      # Randomly generate num_facts no. of integers
        facts = []
        count = 0                                                               # count maintains no. of facts added to the list facts.

        # Iterate through the file line-by-line, if the current 'i' matches a randomly generated integer, put the corresponding
        # line into the list facts. Note that iteration over the entire file is done in order to save memory. We could also load the
        # entire file into a list and select the lines corresponding to the random integers. This would not require iteration over the
        # entire file, but would require loading entire file into memory.

        with open(FILEPATH, encoding='utf-8') as fp:                             
            for i, line in enumerate(fp):                                        
                if i in rn_list:                                                
                    if line:                                                     
                        facts.append(line)                                       
                        rn_list.pop(0)                                                       
                        count += 1                                              
                    else:                                                       # A line might be empty. If so, generate another random integer.
                        rn_list.insert(0, random.randint(i+1, line_count-1))
                if count == num_facts:                                          # If num_facts no. of facts is obtained, break.
                    break

        return facts
        

    @staticmethod
    def speak(sentence, delete=True, slow=False, lang=language, tld=accent_domain):
        '''
        Takes a sentence, generates an audio file by calling the gTTS API,
        saves the audio file, then plays it.

            Parameters:
                sentence (str): String of words to be spoken
                delete (bool): Whether to delete the generated audio file after playing it.
                slow (bool): Slow speech
                lang (str): Language of speech
                tld (str): Accent of speech

            Returns:
                None

            For more information, visit https://gtts.readthedocs.io/en/latest/index.html
            For languages and accents, check out https://gtts.readthedocs.io/en/latest/module.html#languages-gtts-lang
        '''
        try:
            tts = gTTS(sentence, slow=slow, lang=lang, tld=tld)
            tts.save('sentence.mp3')
            playsound('sentence.mp3')
            if delete:
                os.remove('sentence.mp3')
        except:                                     # No Internet Connection error
            playsound('no_internet_error.mp3')
            sys.exit(1)
            

    @classmethod
    def speak_facts(cls, FILEPATH=FILEPATH):
        '''
        Takes the file path, gets the no. of facts, extracts facts at random from the file,
        then speaks out each fact. Ends with a greeting.

            Parameters:
                FILEPATH (str): Path of the file

            Returns:
                None
        '''

        num_facts = cls.get_num_facts()
        facts = cls.get_facts(FILEPATH, num_facts)
        for i in range(num_facts):
            cls.speak(facts[i])
        cls.speak(cls.greeting_2)

FactReader.speak_facts()