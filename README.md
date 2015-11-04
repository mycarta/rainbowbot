# rainbowbot

The idea (thanks to Matt Hall of [Agile Geoscience](http://www.agilegeoscience.com/who/)) is to build a bot that will: 
- download images with maps from the internet (from Google, Twitter, etc.)
- automatically detect the color maps
- flag those with rainbow and other non perceptual colormaps
- optionally convert the colormap to a perceptual version by linearizing the lightness profile

This is my envisioned workflow:

1. download images with maps
2. automatically detect the map portion of the image (it will require removal of text, background, and additional elements like colorbar)
3. reduce the number of colors in the image
4. convert from RGB to HSL and group the reduced colors into 7-8 families, or clusters using H,L pairs 
5. get the mean values for H,L for each cluster
6. sort the mean H, L by H
7. check for monotonicity of L as a perceptual test
8. Optional functionality: convert it to a perceptual version

See my notebook [Evaluate and compare colormaps](https://github.com/seg/tutorials/blob/master/1408_Evaluate_and_compare_colormaps/How_to_evaluate_and_compare_colormaps.ipynb) for a background on perceptual colormaps, and in particular part 4 for an example of the perceptual test.

I started with a Matlab prototype some time ago to test the ideas of sorting  and test of monotonicity, which seemed to work.

Now I am implementing it in Python for this repository.

I plan to test different ideas, or points in the workflow  in different notebooks, which I will upload as completed, which I will combine once I have all the different pieces done.
