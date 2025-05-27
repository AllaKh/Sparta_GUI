
import sys

# mar='_'
def  cycle_marker(mar='_'):
#this function cycles the markers for display
    all_marker_string=',ov^<>1234sp*hH+xDd|_'
    if mar==all_marker_string[-1]:
        mar=all_marker_string[0]
    else:
        mar_ind=all_marker_string.find(mar)
        mar=all_marker_string[mar_ind+1]
    return mar

if __name__ == "__main__":
    for ind in range(25):
        mar=cycle_marker(mar)
        print(mar)
    pass

# https://matplotlib.org/2.1.2/api/_as_gen/matplotlib.pyplot.plot.html
# '-'	solid line style
# '--'	dashed line style
# '-.'	dash-dot line style
# ':'	dotted line style
# '.'	point marker
# ','	pixel marker
# 'o'	circle marker
# 'v'	triangle_down marker
# '^'	triangle_up marker
# '<'	triangle_left marker
# '>'	triangle_right marker
# '1'	tri_down marker
# '2'	tri_up marker
# '3'	tri_left marker
# '4'	tri_right marker
# 's'	square marker
# 'p'	pentagon marker
# '*'	star marker
# 'h'	hexagon1 marker
# 'H'	hexagon2 marker
# '+'	plus marker
# 'x'	x marker
# 'D'	diamond marker
# 'd'	thin_diamond marker
# '|'	vline marker
# '_'	hline marker

