import pandas as pd
import numpy as np
from pathlib import Path

import matplotlib.pyplot as plt

our_file = Path.cwd()
save_file = our_file.parent.joinpath('plots')
data_file = our_file.parent.joinpath('raw_data\ECE331 Lab3 Data421V1.csv')

save_file.mkdir(exist_ok=True)

df = pd.read_csv(data_file)

# We know there is a first run. So find it's length, and thats the length of each run
repeats_per_run = np.count_nonzero(df.VAR2 == 1)

data_array_dict = {}
for name in df.columns:
    data_array_dict[name] = np.reshape(df[name], (-1, repeats_per_run))

# Now lets graph each I_DS vs V_DS for each V_GS

I_DS = data_array_dict['VDS Current']
V_DS = data_array_dict['VDS Voltage']
V_GS = data_array_dict['VGS Voltage']

num_of_runs = np.shape(I_DS)[0]

plt.style.use('bmh')

for run_type in ['nothing', 'tight_fit', 'wide_fit', 'intercept']:
    if run_type == 'tight_fit' or run_type == 'wide_fit':
        fig_x = 10
        fig_y = 6
    elif run_type == 'nothing' or run_type == 'intercept':
        fig_x = 10
        fig_y = 10

    fig, ax = plt.subplots(figsize=(fig_x, fig_y))
    lower_lim = 0
    V_DSsat = []
    I_DSsat = []
    V_T = 1.1
    for run_num in reversed(range(num_of_runs)):  # Reversed to get legend in thr right order
        I_DS_run = I_DS[run_num, :] * 1000
        V_DS_run = V_DS[run_num, :]
        p = ax.plot(V_DS_run, I_DS_run, label='$V_{GS}$ = %1.2f V' % np.median(V_GS[run_num, :]))

        if run_type == 'intercept':
            val_to_find = np.median(V_GS[run_num, :]) - V_T
            idx = (np.abs(V_DS_run - val_to_find)).argmin()
            V_DSsat.append(V_DS_run[idx])
            I_DSsat.append(I_DS_run[idx])

        if run_type == 'tight_fit' or run_type == 'wide_fit':
            I_DS_fit = I_DS[run_num, 50:] * 1000
            V_DS_fit = V_DS[run_num, 50:]
            fitting_coefficents = np.polyfit(V_DS_fit, I_DS_fit, 1)
            print('Run number %s with fitting coefficents of %s, %s' % (run_num, fitting_coefficents[0], fitting_coefficents[1]))
            print('Early Voltage = %2.2f' % (fitting_coefficents[1]/fitting_coefficents[0]))
            fitter = np.poly1d(fitting_coefficents)

            if run_type == 'tight_fit':
                lower_lim = -10
            elif run_type == 'wide_fit':
                lower_lim = -300
            xp = np.linspace(lower_lim, 10)

            ax.plot(xp, fitter(xp), '--', color=p[0].get_color(), alpha=0.5,
                    label='Fit of %1.0f V' % np.median(V_GS[run_num, :]))

    if run_type == 'intercept':
        line, = ax.plot(V_DSsat, I_DSsat, 'k.--', markersize=12,  label='$V_{DS}$ = $V_{GS} - V_T$')
        line.set_color((0, 0, 0, 0.4))
        line.set_markerfacecolor((0, 0, 0, .75))

    plt.ylabel('$I_{D}$ (mA)', fontsize=14)
    plt.xlabel('$V_{DS}$ (V)',  fontsize=14)
    plt.title('MOSFET comparison of $I_{DS}$ and $V_{DS}$ for varied $V_{GS}$')

    # Now add the legend with some customizations.
    if run_type == 'tight_fit' or run_type == 'wide_fit':
        handles, labels = ax.get_legend_handles_labels()
        order = [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]
        legend = ax.legend([handles[idx] for idx in order], [labels[idx] for idx in order],
                           loc='upper left', shadow=True, fancybox=True, ncol=2)
    elif run_type == 'nothing' or run_type == 'intercept':
        legend = ax.legend(loc='upper right', shadow=True, fancybox=True)

    # The frame is matplotlib.patches.Rectangle instance surrounding the legend.
    frame = legend.get_frame()

    for label in legend.get_lines():
        label.set_linewidth(1.5)  # the legend line width

    ax.set_xlim(lower_lim, 10)

    plt.tight_layout()
    plt.savefig(str(save_file.joinpath('characteristic_%s.png' % run_type)), format='png')
    plt.show()

V_DS_threshold = V_DS[:, 80]
I_DS_threshold = I_DS[:, 80] * 1000
V_GS_threshold = V_GS[:, 80]

fig, ax = plt.subplots(figsize=(10, 10))

plt.ylabel('$I_{DS}$ (mA)', fontsize=14)
plt.xlabel('$V_{GS}$ (V)', fontsize=14)
plt.title('MOSFET comparison of $I_{DS}$ and $V_{GS}$ for varied $V_{DS}$ =  %1.2f V' % np.mean(V_DS_threshold))

ax.set_xlim(0, 6)

ax.plot(V_GS_threshold, I_DS_threshold, 'o-')
plt.tight_layout()
plt.savefig(str(save_file.joinpath('characteristic_threshold.png')), format='png')
plt.show()

