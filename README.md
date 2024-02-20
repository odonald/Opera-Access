# Overtitle

Enabling theater and opera visitors to receive more inclusive surtitles directly to their handheld devices by being able to choose from multiple language support and customizable color settings for vision- and hearing-impaired visitors.

## Requirements
Python: 3.9.13 - 3.9.17


## Installation

Clone the project from git:

```
git clone git@github.com:odonald/Access-Opera.git
```


Change directory in to project root:

```
cd Access-Opera
```
Create your virtual environment:

```
python -m venv env
```
Activate your virtual environment:
```
source env/bin/activate
```

Install requirements:
```
pip install -r requirements.txt
```

Run the Application:

```python
python main.py
```
## Usage
1. The Application will start a local server at http://{YOURNETWORKIP}:7832 (shown in the program).

2. If required, you can change the port from 7832 to a different setting via "File" --> "Change Port".

3. Load a .txt file into the program using the "Import Text" button. (The program will automatically split the text file line by line).´

4. Repeat step 3 to add translations of the desired text. (Text files and their translations need to have the same length in lines).

5. Switch the display language to your preferred language (this will only be visible to the navigator). 

5. Use the "Open Website" Button and navigate through the text using the "previous" and "next" buttons to preview the user device output page.

6. Share the link with the users - Use the QR code or share the Link from your browser window in step 5.

Important:
1. The user devices have to be logged in to the same network the host device is broadcasting on. 
2. The program needs to be restarted if introduced to a new network - It will not automatically switch networks while still open. 



## Contributing

Go ahead and contribute :) 

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
