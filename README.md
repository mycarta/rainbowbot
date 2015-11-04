# rainbowbot

The idea is to build a bot that will: 
- download images with maps from the internet (from Google, Twitter, etc.)
- automatically detect the color maps
- flag those with rainbow and other non perceptual colormaps
- optionally convert the colormap to a perceptual version by linearizing the lightness profile

This is the workflow I am thinking of

1) download images with maps
2) automatically detect the map portion of the image (involves removal of text, background, and additional elements like colorbar). I am thinking of using 


reduce the number of colors in the image in scikit-image
2) use scikit-learn k-means or dbscan to group the reduced colors into 7-8 clusters using HSL H, L (and perhaps S)
3) get mean values for H, L for each cluster
4) sort the mean H, L by H
5) check for monotonicity of L as a perceptual test
6) Optional functionality would be to convert it to a perceptual version.
See this notebook for a background on perceptual colormaps https://github.com/seg/tutorials/blob/master/1408_Evaluate_and_compare_colormaps/How_to_evaluate_and_compare_colormaps.ipynb
I made a Matlab prototype some time ago and the idea seems to work.
Now I am implementing it in Python - I have a bunch of notebooks where I am testing different things in the above list separately.
