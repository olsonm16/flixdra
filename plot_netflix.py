import plotly.plotly as py
from plotly.graph_objs import Bar

def plot_history(history, name):
	py.sign_in('mitchhydras','wi2qaykd8l')
	days = []
	times = []

	for date in history.keys():
		days.append(str(date).split(" ")[0])
		times.append(history[date].get_mins())

	trace0 = Bar(x=days,
	    y=times
	)

	data = [trace0]

	unique_url = py.plot(data, filename = name + "netflix-history")