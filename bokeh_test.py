import numpy as np

from bokeh.plotting import figure, show, output_file

N = 10000

x = np.random.normal(0, 4*np.pi, N)
y = np.sin(x) #+ np.random.normal(0, 0.2, N)# + np.random.normal(0, 2, N)


p = figure(webgl=False)
p.scatter(x,y, alpha=0.1)

output_file("webgl_false.html", title="scatter 10k points (with WebGL)")

show(p)