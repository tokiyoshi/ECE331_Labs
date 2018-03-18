import pandas as pd
import numpy as np
from pathlib import Path

import matplotlib.pyplot as plt


def import_data(directory):
    data_file = our_file.parent.joinpath(directory)

    df = pd.read_excel(data_file)

    data_array_dict = {}
    for name in df.columns:
        data_array_dict[name] = df[name]

    return df


def plot_data(x, y, title, x_label, y_label, save_name, type=None):
    plt.style.use('bmh')

    fig_x = 10
    fig_y = 6

    fig, ax = plt.subplots(figsize=(fig_x, fig_y))

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    if type is None:
        line = ax.plot(x, y)
    elif type == "semi-log":
        line = ax.semilogy(x, y)
    elif type == "log":
        line = ax.loglog(x, y)

    plt.ylabel(y_label, fontsize=14)
    plt.xlabel(x_label, fontsize=14)
    plt.title(title)

    plt.tight_layout()
    plt.savefig(str(save_file.joinpath('%s.png' % save_name)), format='png')
    #plt.show()
    return plt, ax, line[0]


our_file = Path.cwd()
save_file = our_file.parent.joinpath('plots')

save_file.mkdir(exist_ok=True)

downwards_data = import_data('raw_data/downwards.xlsx')
upwards_data = import_data('raw_data/upwards.xlsx')

# First make the Gummel Plot
x_data = downwards_data['V_BE-mV']
y_data = downwards_data['I_C-mA']/1000

down_plot, down_ax, down_line = plot_data(x_data, y_data,
                                  "Gummel Plot for Downwards npn Transistor", "$V_{BE}$ (mV)", "$I_{C}$ (A)",
                                    "Downwards_Gummel_plot", type="semi-log")
ignore_index = -4
x_fit = x_data[:ignore_index]
y_fit = y_data[:ignore_index]

fitting_coefficents = np.polyfit(x_fit, np.log(y_fit), 1)
fitter = np.poly1d(fitting_coefficents)

print('Downwards with fitting coefficents of %s, %s' % (fitting_coefficents[0], fitting_coefficents[1]))

print('The I_CS = %s A' % (np.exp(fitter(0))))

xp = np.linspace(0, max(x_data)+50)

down_ax.plot(xp, np.exp(fitter(xp)), '--', color=down_line.get_color(), alpha=0.5)

down_plot.savefig(str(save_file.joinpath('downward_fitted.png')), format='png')
#down_plot.show()

# Second make the Gain Plot
y_data = downwards_data['gain']
x_data = downwards_data['I_C-mA']/1000

gain_plot, gain_ax, down_line = plot_data(x_data, y_data,
                                  'Gain plot Downwards npn Transistor', '$I_{C}$ (A)', r"$\beta$",
                                    "Downwards_gain", type="log")

down_line.label = "Downwards"

# Upwards

y_data = upwards_data['gain']
x_data = upwards_data['I_C-mA']/1000

up_line = gain_ax.loglog(x_data, y_data)[0]

up_line.label = "Upwards"

legend = gain_ax.legend(loc='upper right', shadow=True, fancybox=True)
# The frame is matplotlib.patches.Rectangle instance surrounding the legend.
frame = legend.get_frame()

for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width

gain_plot.savefig(str(save_file.joinpath('gain_both.png')), format='png')
gain_plot.show()
