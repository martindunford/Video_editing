#! /usr/local/bin/python3

# http://zulko.github.io/blog/2014/09/20/vector-animations-with-python/
import numpy as np
import gizeh as gz
import moviepy.editor as mpy

def main():

    W,H = 800, 600
    D = 2 # duration in seconds
    r = 30 # size of the letters / pentagons

    gradient= gz.ColorGradient("linear",((0,(0,.5,1)),(1,(0,1,1))),
                               xy1=(0,-r), xy2=(0,r))

    text_to_display = "Martin Dunford'"
    def make_frame(t):
        polygon = gz.regular_polygon(r, 5, stroke_width=3, fill=gradient,xy=[0,t*30])
        surface = gz.Surface(W,H, bg_color=(1,100,1))
        for i, letter in enumerate(text_to_display):
            angle = max(0,min(1,2*t/D-1.0*i/5))*2*np.pi
            txt = gz.text(letter, "Amiri", 3*r/2, fontweight='bold',xy=[0,t*30])
            group = (gz.Group([polygon, txt])
                     .rotate(angle)
                     .translate((W*(i+1)/len(text_to_display),H/2)))
            group.draw(surface)
        return surface.get_npimage()

    clip = mpy.VideoClip(make_frame, duration=5)
    clip.write_gif("gizeh.gif",fps=20, opt="OptimizePlus")

if __name__ == '__main__':
    main()