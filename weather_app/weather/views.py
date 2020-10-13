from django.shortcuts import render
import requests
from requests import Response
# from rest_framework.response import Response
from rest_framework import status
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

from weather_app.settings import WEATHER_URL, APP_ID


def fetch_temp_readings(request):

    context = {}
    query_params = request.GET
    exit_func = False
    if 'city' not in query_params:
       exit_func = True
    if 'period' not in query_params:
       exit_func = True
    params = {
		'url': WEATHER_URL,
		'params': {
			'q': query_params.get('city', ''),
			'units': 'metric',
			'mode': 'json',
			'APPID': APP_ID
		}
	}
    if exit_func is not True:
        response = requests.get(**params)
        if response.status_code == 200:
           period = query_params.get('period').strip("\'")
           img_hash = extract_graph_data(response.json(), period)
           context['img_hash'] = str(img_hash)
        else:
           context['status_code'] = response.status_code
    else:
        context['message'] = 'missing required query params(i.e. city and/or period)'
    if query_params.get('view_type', 'api') == 'web':
        return render(request, 'index.html', context)
    return render(request, 'index.html', context)


def extract_graph_data(weather_data_dict, period):

    data_names = ['dt_txt', 'temp_min', 'temp_max', 'humidity']
    plot_data = []
    for data_dict in weather_data_dict.get('list'):
        _data = dict(
            map(
                lambda name:
                    (name, data_dict.get(name) if name == 'dt_txt' else data_dict.get('main')[name]),
                    data_names
            )
        )
        if period.strip('"') not in _data.get('dt_txt'):
           continue
        plot_data.append(_data)

    img_hash = prep_plot_data(plot_data, data_names)
    return img_hash

def prep_plot_data(extracted_weather_data, names):

    plot_data = {}
    for name in names:
        values = list(map(lambda data: data.get(name), extracted_weather_data))
        plot_data[name] = values
    img_hash = generate_bar_graph(plot_data, names)
    return img_hash


def autolabel(rects, ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


def generate_bar_graph(plot_data, names):

    plot = {}
    x = np.arange(len(plot_data.get('dt_txt')))
    width = 0.35

    fig, ax = plt.subplots()
    for name_index in range(len(names)):
        _name = names[name_index]
        if _name == 'dt_txt':
            continue
        key = 'rect_{}'.format(name_index)
        if name_index == 1:
            x_add = 0.35
        elif name_index == 2:
            x_add = 0
        else:
            x_add = 0.35
        plot[key] = ax.bar(x - x_add if name_index == 1 else x + x_add, plot_data.get(_name), width, label='{}'.format(_name))

    ax.set_ylabel('Readings')
    ax.set_title('Weather(Min, Max, Humidity)')
    ax.set_xticks(x)
    # ax.set_xticklabels(plot_data.get('dt_txt'))
    # ax.set_xticklabels(plot_data.get('dt_txt'), rotation='vertical')
    ax.legend()
    map(lambda rect: autolabel(rect, ax), plot.values())
    fig.tight_layout()
    b64_string = io.BytesIO()
    plt.savefig(b64_string, format='png')
    b64_string.seek(0)
    img_hash = base64.b64encode(b64_string.read())
    return img_hash.decode('utf-8')
