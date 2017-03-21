import matplotlib.pyplot as plt


def save(xlabel, ylabel, filename):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.savefig('results/' + filename + '.png')
    plt.savefig('results/' + filename + '.pdf')
    plt.figure()
    pass
