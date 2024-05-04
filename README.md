# Overtitle

Opera-Access provides a practical solution for the delivery of surtitles—also known as supertitles, SurCaps, or OpTrans—in theaters and operas. 

Using the well-established Python and Tkinter technologies, the software enables the surtitle driver to send text fragments to the audience in real-time via SSE. This eliminates the need for a dedicated app, allowing audience members to access these surtitles through a browser on their devices via local WiFi. 

The system offers customization options such as text format settings and language preferences, making performances more accessible to individuals with visual or auditory disabilities and to non-native speakers. While the technology may not be new, the application of this tool to enhance the theater-going experience is a notable improvement for the partnering theaters and opera houses.

# Table of Contents
- [Requirements](#Requirements)
- [Installation](#Installation)
- [Testing](#Testing)
- [Usage](#Usage)
- [Contributing](#Contributing)
- [License](#License)

# Requirements
Python: 3.9.13 - 3.9.17


# Installation

1. Clone the project from git:

```
git clone https://github.com/odonald/Opera-Access.git
```


2. Change directory in to project root:

```
cd Opera-Access
```
3. Create your virtual environment:

```
python -m venv venv
```
4. Activate your virtual environment:
```
source venv/bin/activate
```

5. Install requirements:
```
pip install -r requirements.txt
```

6. Run the Application:

```python
python run.py
```

# Testing
To run all tests, make sure you are within the virtual environment by repeating steps 2, 3 & 4 from the [Installation](##Installation) instructions.

You currently have two options:

## 1. Run without end-to-end test (recommended):
The testing suite currently includes a very "flaky" [pyautogui](https://pyautogui.readthedocs.io/en/latest/)
 end-to-end test, chances are high it will not work, unless you are running it on macOS using dark mode system settings.
#### !At this point it is highly recommended to run tests excluding the end-to-end test!
To run the suite without the end-to-end test:
```python
ptw -- -m "not e2e"
```

## 2. Run all tests including the end-to-end test (not recommended):

1. From the application root first activate the hot developer reload function of the application:
```python
python dev_hot_reload.py
```
*(Note: This will automatically close and reopen the application after every saved code change.)*

2. Then to run the suite without the end-to-end test, execute:
```python
ptw
```
*Note: Pytestwatch monitors your IDE and performs a round of tests after every saved code change.*



# Usage
1. The Application will start a local server at http://{YOURNETWORKIP}:7832 (shown in the program).

2. If required, you can change the port from 7832 to a different setting via "File" --> "Change Port".

3. Load a .txt file into the program using the "Import Text" button. (The program will automatically split the text file line by line).´

4. Repeat step 3 to add translations of the desired text. (Text files and their translations need to have the same length in lines).

5. Switch the display language to your preferred language (this will only be visible to the navigator). 

5. Use the "Open Website" Button and navigate through the text using the "previous" and "next" buttons to preview the user device output page.

6. Share the link with the users - Use the QR code or share the Link from your browser window in step 5.

#### Important:
1. The user devices have to be logged in to the same network the host device is broadcasting on. 
2. The program needs to be restarted if introduced to a new network - It will not automatically switch networks while still open. 



# Contributing

Go ahead and contribute :) 


# License

[MIT](https://choosealicense.com/licenses/mit/)
