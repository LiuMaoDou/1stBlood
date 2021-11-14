import matplotlib.pyplot as plt
def plt_fig(title, xlabel,ylabel,xlst,ylst,legend='default'):
    plt.plot(xlst,ylst,label=legend)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()
    plt.close()
