import sys
import warnings
import importlib
import subprocess

warnings.filterwarnings("ignore")

def check_and_install(module_name):
    try:
        importlib.import_module(module_name)
    except ImportError:
        print(f"{module_name} is not installed. Installing...")
        subprocess.check_call(["pip", "install", module_name])
        print(f"{module_name} has been successfully installed.")

# Modules to check and install
modules_to_check = ["matplotlib", "pandas"]

for module_name in modules_to_check:
    check_and_install(module_name)

import pandas as pd
import matplotlib.pyplot as plt


def main():
    print("Genereting plots...")

    if len(sys.argv) < 2:
        print()
        print("Error -> ","Usage: python script.py <string>")
        return
    string_argument = sys.argv[1]


    df = pd.read_csv(string_argument, delimiter=" ",usecols=[0,1,4,8,12],names=["MsuH","m_ini","M_ass","b-y","age_parent"],skiprows=1)
    df = df.sort_values(by=["age_parent"])


    ######################
    # First plot
    ######################
    n_col = 10
    l = len(df)

    ap_min, ap_max = df["age_parent"].min(),df["age_parent"].max()    
    step = int(l/n_col)
    ap_step = (ap_max-ap_min)/n_col

    x,y,c = df[["b-y"]], df[["M_ass"]], df[["age_parent"]].to_numpy()
    viridis = plt.get_cmap('viridis', n_col,)

    for i in range(n_col):
        label = "{:.2f} Gyr - {:.2f} Gyr".format(ap_step*i, ap_step*(i+1))
        _=plt.scatter(x[i*step:(i+1)*step],y[i*step:(i+1)*step],c=viridis.colors[i],marker=".",label=label,s=7)
        
    plt.xlim(-0.2,1.2)
    _=plt.legend(fontsize=8)
    plt.ylabel(r"M_ass")
    plt.xlabel(r"b-y")
    plt.gca().invert_yaxis()
    plt.savefig('Images/Scatter.png')
    plt.clf()



    ######################
    # A variation on the first plot
    ######################
    plt.gca().invert_yaxis()
    plt.ylabel(r"M_ass")
    plt.xlabel(r"b-y")
    plt.scatter(x,y,c=c,s=4)
    cbar = plt.colorbar()
    cbar.set_label("Gyr")
    plt.savefig('Images/Scatter_optional.png')
    plt.clf()



    ######################
    # Second plot
    ######################
    n = [1,5]
    h = []
    n_bins = 17

    h.append(df[df["age_parent"]<n[0]]["MsuH"])
    for i in range(len(n)-1):
        h.append(df[(df["age_parent"]>n[i]) & (df["age_parent"]<n[i+1])]["MsuH"])
    h.append(df[df["age_parent"]>n[-1]]["MsuH"])

    plt.xlabel(r"MsuH")
    plt.ylabel(r"Frequency")
    kwargs = dict(histtype='stepfilled', alpha=0.4, bins=n_bins, ec="k")

    plt.hist(h[0],density=True, **kwargs, label="age_parent < {:.1f} Gyr".format(n[0]))
    for i in range(1,len(n)):
        plt.hist(h[i],density=True, **kwargs, label="{:.1f} Gyr < age_parent < {:.1f} Gyr".format(n[i-1],n[i]))
    plt.hist(h[-1],density=True, **kwargs, label="age_parant > {:.1f} Gyr".format(n[-1]))

    plt.legend()
    plt.savefig('Images/Histogram1.png')
    plt.clf()



    ######################
    # Third plot
    ######################
    h = []
    n_bins = 15

    h.append(df[df["age_parent"]<n[0]]["m_ini"])
    for i in range(len(n)-1):
        h.append(df[(df["age_parent"]>n[i]) & (df["age_parent"]<n[i+1])]["m_ini"])
    h.append(df[df["age_parent"]>n[-1]]["m_ini"])

    plt.xlabel(r"m_ini")
    plt.ylabel(r"Frequency")
    kwargs = dict(histtype='stepfilled', alpha=0.4, bins=n_bins, ec="k")

    plt.hist(h[0],density=True, **kwargs, label="age_parent < {:.1f} Gyr".format(n[0]))
    for i in range(1,len(n)):
        plt.hist(h[i],density=True, **kwargs, label="{:.1f} Gyr < age_parent < {:.1f} Gyr".format(n[i-1],n[i]))
    plt.hist(h[-1],density=True, **kwargs, label="age_parant > {:.1f} Gyr".format(n[-1]))

    plt.legend()
    plt.savefig('Images/Histogram2.png')


    print("Plots saved in /Images/")


if __name__ == "__main__":
    main()