# Fact-reader

Selects facts at random from a text file and speaks them out to the user.

## Working
The folder consists of a text file full of facts. The script will ask the user regarding the number of facts they want to know. The user can then type a number between 1-9.
After this, the corresponding number of facts will be randomly selected from the file and will be read out to the user. The text-to-speech implementation was done using Google's
GTTS module.

## Requirements
* [Python3](https://www.python.org/downloads/) 
* [playsound](https://pypi.org/project/playsound/) : `pip3 install playsound`
* [gTTS](https://pypi.org/project/gTTS/) :  `pip3 install gTTS`
* [keyboard](https://pypi.org/project/keyboard/) :  `pip3 install keyboard`
* Internet connectivity (for gTTS)

## Acknowledgements

gTTS Documentation: https://gtts.readthedocs.io/en/latest/

The facts were taken from: https://github.com/anfederico/fact-bot/Facts.txt, https://github.com/assaf/dailyhi/blob/master/facts.txt. 

I thank the authors of these files.
