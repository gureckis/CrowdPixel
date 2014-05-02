CrowdPixel
==========

a psiturk-compatible project for making crowdsourced visual art.
you provide and image, crowdpixel will split the image into
tiles, and present each tile to a worker on mechanical turk
who is asked to draw a representation of the tile.  the crowd
provides a rich detailed piece of art in the spirit of painter
chuck close.

Requirements
------------
Besides the standard dependencies of **psiTurk**, this project
depends on the python `image_slicer` library.  You can install
this library by typing `sudo pip install image_slicer`.

How to use
----------

Breifly, assuming you have psiturk installed, working, have the AWS credentials and an
account on psiturk.org.

**Get the repo**  

1. `git clone git@github.com:gureckis/CrowdPixel.git`  

**Make it yours**  

1. `cd CrowdPixel` - change to the project folder  
1. edit `config.txt` to your liking (particular setting `host` to 0.0.0.0 if you plan to run on the public internet, also fill in the `contact_email_on_error`, your university/organization name, etc...) 
1. replace `static/images/university.png` with a logo reflecting your university/organization
1. edit the `templates/ad.html` file to reflect your university/organization and the amount you plan to pay for each drawing
1. edit the `templates/consent.html` if you want to use it (you may be able to skip if just playing around... just change  `templates/ad.html` so that the `/exp` route is chose when you click begin instead of `/consent`)  
1. choose a high resolution JPG/GIF/PNG image you'd like people to render
1. run `python setup.py <filename> <numtiles>` where `<filename>` is the name of your image and `<numtiles>` is the number of tiles
you want to create (don't include the `<>` characters).  This will create a `numtiles` images in `static/images/tiles/` folder and set the number of conditions in your `config.txt` so that each worker will view a different tile during the experiment.
See the [image slicer docs](https://image-slicer.readthedocs.org/en/latest/) for more info.

**Test your code**  

1. `psiturk` - launch psiturk  
1. `[psiTurk server:off mode:sdbx #HITs:0]$ server on` - start server  
1. `[psiTurk server:on mode:sdbx #HITs:0]$ debug` - test it locally  (will pop open a browser stepping you through)
1. `[psiTurk server:on mode:sdbx #HITs:0]$ create hit` - to create the hit on the AMT sandbox
1. Test the experiment by finding your listing on the Amazon sanbox

**Run live**  

1. If all is going well and looks how you expect, `[psiTurk server:on mode:sdbx #HITs:0]$ mode` - to switch to "live" mode  
1. `[psiTurk server:on mode:live #HITs:0]$ create hit` - to create the hit on the live server  
1. `[psiTurk server:on mode:live #HITs:0]$ hit list active` - to monitor the progress
1. `[psiTurk server:on mode:live #HITs:0]$ worker approve --hit <yourhitid>` - to approve and pay everyone who has finished


In other words, it works basically identically to the default “stroop” example that ships with **psiTurk**.
See the main [psiturk docs](http://psiturk.readthedocs.org/en/latest/) if you don't feel you know
what you are doing.

**The Gallery**  

This project provides a custom URL (via custom.py) that lets you view the results of the “experiment”.  To access this 
you just point your browser at your local server with /gallery as the url.  For example, “http://mylaptop.myuniversity.edu:22362/gallery” It’ll prompt you for a username and password 
which are set by the `login_username` and `login_pw` fields of the `config.txt` file.
