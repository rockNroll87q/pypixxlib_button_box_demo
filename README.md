# pypixxlib_button_box_demo

A simple demo for the VPixx Technologies's RESPONSEPixx/MRI (4-button response box, [link](http://vpixx.com/products/responsepixx-mri-handheld/)). This is useful if you want to check that everything is working properly with the python wrapper pypixxlib for the button box.

### What it does? 

<p align="center">

<img src="https://github.com/rockNroll87q/pypixxlib_button_box_demo/blob/master/demo_video.gif" width="524" height="295" />  

</p>

The code works creating a separate thread that constantly checks the presence of an input and register temporal information of the event. 

In a regular experiment, in the case you need to control the button box in python, you just need to copy and paste part of the code and control the button pressed event as you prefer.

See the [video](https://github.com/rockNroll87q/) for a demo.

### How to use it

* Run with `python ./button_box_demo.py` or IDE;
* Play with VPixx button box;
* Press `Esc` o `q` to finish.

### What you need to run it?

* Python2.x (3.x should work as well) 
* Psychopy ([link](http://www.psychopy.org/))
* pypixxlib (python wrapper, see [vpixx](http://vpixx.com/) website)
