# pypixxlib button box demo

A simple demo for the VPixx Technologies's RESPONSEPixx/MRI (4-button response box, [link](http://vpixx.com/products/responsepixx-mri-handheld/)). This is useful if you want to check that everything is working properly with the python wrapper pypixxlib for the button box.

## What it does? 

<p align="center">

<img src="https://github.com/rockNroll87q/pypixxlib_button_box_demo/blob/master/demo_video.gif" width="524" height="295" />  

</p>

The code works creating a separate thread that constantly checks the presence of an input and register temporal information of the event. 

In a regular experiment, in the case you need to control the button box in python, you just need to copy and paste part of the code and control the button pressed event as you prefer.

## How to use it

* Run with `python ./button_box_demo.py` or IDE;
* Play with VPixx button box;
* Press `Esc` o `q` to finish.

## What should I do in my experiment?

In order to use the code in your experiment, I created a short and easy to plugin version in which all the material needed is in a file. Steps are the following. 

Initialise the button box thread at the beginning of your code.

~~~
from button_box_threading import buttonBoxThread
button_thread = buttonBoxThread(1, "bottom box check")
button_thread.start()
~~~
 
Check for the scanner trigger (o button box) when you need to.

~~~
button_state = button_thread.button_state
  while 1:
    if(button_state['state'][-1]==0):
      break
~~~
 
End the thread at the end of the experiment.

~~~
button_thread.stop()
~~~ 

## What you need to run it?

* Python2.x (3.x should work as well) 
* Psychopy ([link](http://www.psychopy.org/))
* pypixxlib (python wrapper, see [vpixx](http://vpixx.com/) website)
