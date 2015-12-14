# rainbowbot

The idea (thanks to Matt Hall of [Agile Geoscience](http://www.agilegeoscience.com/who/)) is to build a bot that will: 
- download images with maps from the internet (from Google, Twitter, etc.)
- automatically detect the color maps
- flag those with rainbow and other non perceptual colormaps
- optionally convert the colormap to a more perceptual version by linearizing the lightness gradient

This is my envisioned workflow (ideally all automatic, no user input required, and no hard-coded parameters):

1. download images with maps
2. detect the map portion of the image (it will require removal of text, background, and additional elements like colorbar)
3. reduce the number of colors in the image
4. convert from RGB to HSL and group the reduced colors into 7-8 families, or clusters using H,L pairs 
5. get the mean values for H,L for each cluster
6. sort the mean H, L by H
7. check for monotonicity of L as a perceptual test
8. optional functionality: convert it to a perceptual version

See my notebook [Evaluate and compare colormaps](https://github.com/seg/tutorials/blob/master/1408_Evaluate_and_compare_colormaps/How_to_evaluate_and_compare_colormaps.ipynb) for a background on perceptual colormaps, and in particular part 4 for an example of the perceptual test.

I started with a quick and dirty Matlab prototype some time ago to try my ideas on sorting and to try the test of monotonicity, which seemed to work:
an image of geophysical data with non perceptual colormap 

![Jet](https://github.com/mycarta/rainbowbot/blob/master/images4README/rainbow_blues_tight.png)

one with perceptual colormap (in the sense of ordered, strictly monotonic lightness)

![LinearL](https://github.com/mycarta/rainbowbot/blob/master/images4README/LinearL_tight.png)

and the result of sorting H and L by H

![sort](https://github.com/mycarta/rainbowbot/blob/master/images4README/H_vs_L_sorted_by_H.PNG)

The logic for the test, in Matlab, was:
> test = (all(diff(L)<0)) | (all(diff(L)<0))

which will translate into:
> all(x<y for x, y in pairwise(L))

Now I am implementing the whole workflow in Python. I plan to test different ideas, or points in the workflow  in different notebooks, which I will upload as completed, which I will combine once I have all the different pieces done
