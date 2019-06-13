# AutoROM
AutoROM is a simple tool for importing data from files into TUNG (the ultimate nerd game) as read only memories.

If you have questions or feature suggestions, please visit [the thread](https://logicworld.net/Forum/Post/19) over on the logic world forums.

## Installation
To install AutoROM, simply clone this repository or download and decompress the zip archive to any directory on your machine.

### Releases
For now, contributions and updates will be handled on an ad-hoc basis. Actual "Releases" may come later.

### Requirements
* Python 3.6 or higher
* A working TUNG installation
* Some C# runtime environment (e.g. mono)
* An internet connection (required when the program is first run to download board to json binaries)

### Python dependencies
* numpy `pip3 install numpy`
* tkinter `pip3 install tkinter`
* argparse `pip3 install argparse`

## Usage
AutoROM is a command line utility. These are the available options:

* `-h` Display a help message including all command line options
* `-l` List available ROM board information
* `-r` Target ROM type
* `-i` Input file
* `-o` Output file, defaults to current working directory
* `-c` Clean, deletes all intermediate files

## Adding your own ROM boards
AutoROM is extensible and designed for the (relatively) easy addition of new ROM boards. Understanding of trigonometry, coordinate systems and some experience with python will be helpful.

More information to come.

## Special thanks
* [Stenodyon](https://github.com/Stenodyon) - for creating the BoardToJson tool and making this project possible
