
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

sns.set()
sns.set_style('white')
sns.set_context('talk')


def draw_arrow(ax, x0, y0, x1, y1, color='b'):
    ax.annotate('', xy=(x0, y0), xytext=(x1, y1), xycoords='data', textcoords='data', color=color,
                arrowprops={'arrowstyle': '<-', 'color': color})


if __name__ == '__main__':

    for step in [0, 1, 2, 3, 4]:
        f, ax = plt.subplots()

        xgrid = np.linspace(-1, 0, 101)
        curvature = 0.9
        a = curvature
        # a x^2 + (a - 1)*x goes through (0, 0) and (-1, 1)
        ygrid = curvature * xgrid ** 2 + (curvature - 1) * xgrid

        # dy/dx = 2*a*x - 1 - a
        dydx = 2 * curvature * xgrid + (curvature - 1)
        dx = -0.3

        if step > 1:
            ax.plot(xgrid, ygrid, ls='--')

        if step > 2:
            dy = dydx[-1] * dx
            draw_arrow(ax, 0, 0, dx, dy)
            ax.text(dx / 2, dy / 2 - 0.05, '$\lambda_{ii}(0)$', va='top', ha='center', color='b')

        if step > 3:
            # alpha
            dydx *= 15
            dy = dydx[-1] * dx
            draw_arrow(ax, 0, 0, dx, dy, color='r')
            ax.text(dx / 2, dy / 2 + 0.05, r'$\lambda_{ii}(\alpha_0)$', va='bottom', ha='left', color='r')

        if step > 0:
            ax.plot([0, -1], [0, 1], ls='--', color='k')

        # Datapoints
        ax.plot([-1], [1], 'ko')
        ax.text(-1.0, 1.1, '$E_i(N-1)$', ha='right')
        ax.text(0.05,  -0.05, '$E(N)$', ha='left')
        ax.plot([0], [0], 'ko')

        # ax.get_xaxis().set_visible(False)
        # ax.get_yaxis().set_visible(False)
        ax.set_xlim([-1.4, 0.2])
        ax.set_ylim([-0.2, 1.2])
        ax.set_xlabel('occupation')
        ax.set_ylabel('energy')
        ax.set_xticks([])
        ax.set_yticks([])
        sns.despine()
        plt.savefig(f'fig_alpha_calc_step_{step}.pdf', format='pdf')
