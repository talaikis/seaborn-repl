from os import getenv
from os.path import join, dirname, abspath
from datetime import datetime, timedelta
from json import dump, load
from ast import literal_eval

from seaborn import heatmap, despine
import matplotlib.pyplot as plt
from matplotlib import cm
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from pandas import read_json, to_datetime, concat
import seaborn as sns
sns.set_style('darkgrid')
sns.set_palette(sns.color_palette('RdBu', n_colors=5))
BLUE1, = sns.color_palette('muted', 1)

BASE_DATA = join(dirname(abspath(__file__)))
fig_size = (9, 6)

def cumulate_returns(x):
    return x.cumsum()[-1]

def plot_monthly_heatmap(returns, name):
    try:
        returns = returns.groupby([lambda x: x.year, lambda x: x.month]).apply(cumulate_returns)
        returns = returns.to_frame().unstack()
        returns = returns.fillna(0.0)
        returns = returns.round(3)
        returns.rename(columns={ 1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr',
            5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug',
            9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'},
            inplace=True)
        plt.figure(figsize=fig_size)
        ax = plt.gca()
        ax.set_title('Monthly returns, %', fontweight='bold')
        heatmap(returns, xticklabels=[i[1] for i in list(returns.columns)], annot=True, fmt='0.3f', annot_kws={'size': 8}, alpha=1.0, center=0.0, cbar=False, cmap=cm.RdYlGn, ax=ax, robust=True)
        plt.savefig(join(BASE_DATA, '{}-monthly-returns.png'.format(name)), bbox_inches='tight')
        plt.close()
    except Exception as e:
        print('plot_monthly_heatmap', e)

if __name__ == '__main__':
    df = read_json(join(BASE_DATA, 'ret.json'), orient='index')
    plot_monthly_heatmap(df['returns'], 'test')
