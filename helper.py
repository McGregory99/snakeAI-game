import matplotlib.pyplot as plt
from IPython import display
import os

plt.ion() # Activa el modo interactivo

def plot(scores, mean_scores, num_games):
    display.display(plt.gcf())
    plt.clf()  # Clear Figure
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    filepath=os.path.join("img", str(num_games)+'.png')
    plt.savefig(filepath)
