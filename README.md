# ScriptEditor
CS121 Script Editor Project

Shakespeare’s plays are long, so performers often cut them down before producing them. 
They do so by going through the play line-by-line, crossing outlines (or parts of lines) 
that can be cut without changing the nature of the play in unintended ways such as the complete 
removal of a character or the loss of a thematic element. This can be a problem as there is currently 
no easy way to check if this happens. Additionally, Shakespeare’s plays have a lot of structure: acts, 
scenes, speeches,lines, characters, etc. Performers often take advantage of this structure to 
help them navigate the play and to better understand and produce it (e.g., by creating a list of 
characters that have scenes together, figuring out how many lines a character has, etc). This app 
makes it easy to cut a play, while still making it possible to navigate to certain parts of the play and to analyze the play.

## Installation

1. Clone the repository from GitHub
2. Navigate to the ScriptEditor directory `cd ScriptEditor`
3. Get the correct Ruby gems `bundle install`
4. Navigate to the plays folder `cd app/views/plays`
5. Run the parser `python parser.py`
6. Run the migration using rails db:migrate.
7. Set up the server `rails s`
8. Navigate to localhost:3000 to see the site

## Usage

* The python parser relies on data.xml, so to view a different play, change the specified play in parser.py to any xml file in the app/assets folder.
* To import a new play, download the XML from the Folger Digital Library and put it into the app/assets folder.
* To jump to a section of the play, click on a scene or act on the floating navigation bar on the right. If you don't want the navigation bar, you can click on the Navigation tab.
* To strike through a line of the play, click on that line. If it does not work, rerun to localhost:3000 and try again.
* Sometimes the back button makes everything break.

* To toggle between Edit mode on or off, click the "Edit" button in the top navigation bar. 


## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## History

May 5, 2017 Version 0.7 released

## Credits

This is an iteration of a project for Harvey Mudd College's CS121 (Software Development) class taught by Professor Yekaterina Kharitonova. 
This was done by Samantha Andow, Julia McCarthy, Julio Medina, and Sarah Sedky. Project advisor was Professor Ben Wiedermann.

## Future features
* Add a way to get back to the play from the characters tab, since the back button does not always work.
* The javascript relies on the formatting of the URL, so make it independent of the URL.
* Make the edit button meaningful.

## License

MIT License

Copyright (c) 2017 (JS)^2

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
