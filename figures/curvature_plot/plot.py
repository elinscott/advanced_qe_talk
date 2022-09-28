import sys
sys.path.append('/home/elinscott/Documents/notes/curvature_plot')
from curvature_plotting import ENCurve
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def save(ax, name):
   ax.set_xlim([0.5, 3.5])
   ax.set_ylim([-1, 3])
   ax.set_xticks(range(1,4))
   ax.set_xticklabels(['$N-1$','$N$','$N+1$'])
   ax.set_xlabel('total number of electrons')
   plt.subplots_adjust(left=0.17, right=0.83, top=0.95, bottom=0.15)
   plt.savefig(name)

if __name__ == '__main__':

   sns.set_style('white')
   sns.set_context('talk')

   exact_e = np.array([5, 1.5, 0.25, 0.0, 0.0])

   i_orb = 2

   exact = ENCurve('exact', exact_e)
   koop = ENCurve('Koopmans', exact_e)
   sl = ENCurve('semi-local', exact_e, curvature=1.5) # - 0.1 - 0.2*np.random.rand(len(exact_e)), curvature = 1.5)
   hf = ENCurve('Hartree-Fock', exact_e, curvature=-2.0) # + 0.1 + 0.2*np.random.rand(len(exact_e)), curvature = -2)
   
   f, ax = plt.subplots(1,1)
   plt.subplots_adjust(bottom=0.2)

   # Plot of exact piecewise-linear behaviour only
   exact.plot(ax, ls='--')
   save(ax, 'fig_en_curve_exact.pdf')

   # Add annotations
   exact.label_Delta_E(ax, i_orb)
   exact_epsilon_label = ax.text(i_orb - 0.2, exact_e[i_orb] + 0.5, r'$\left.\frac{dE}{dN}\right|_{N = N^-} = \varepsilon_\mathrm{HO}$', color=exact.color, rotation=0)
   save(ax, 'fig_en_curve_exact_annotated.pdf')

   exact_epsilon_label.remove()
   exact.remove_annotations()

   # Plot of Hartree-Fock
   sl.plot(ax)
   save(ax, 'fig_en_curve_sl.pdf')

   f2, ax2 = plt.subplots(1,1)
   plt.subplots_adjust(bottom=0.2)
   # With annotations
   koop.plot(ax2, ls='--')
   sl.plot(ax2)
   exact.plot_gradient(ax2, i_orb, forward=False, label=r'$\varepsilon_\mathrm{HO}(N) = E(N) - E(N-1)$', ha='left', label_dx=0.02, label_dy=0.02)
   exact.plot_gradient(ax2, i_orb-1, forward=True, label=r'$\varepsilon_\mathrm{LU}(N-1)$', ha='left', label_dx=0.02, label_dy=0.02)

   sl.plot_gradient(ax2, i_orb, forward=False, label=r'$\varepsilon_\mathrm{HO}(N) = \left.\frac{dE}{dN}\right|_{N = N^-}$', va='top', label_dx=-0.1, label_dy=-0.05)
   sl.plot_gradient(ax2, i_orb-1, forward=True, label=r'$\varepsilon_\mathrm{LU}(N-1)$', ha='right', label_dx=-0.02)
   save(ax2, 'fig_en_curve_gradients.pdf')
   ax2.set_xlim([0.75, 2.25])
   ax2.set_ylim([-0.25, 1.75])
   plt.savefig('fig_en_curve_gradients_zoom.pdf', format='pdf')

   plt.figure(f.number)
   sl.plot_extrapolation(ax, i_orb, forward=False, label_error='error', label_extrap=r'$\varepsilon_\mathrm{HO} = \left.\frac{dE}{dN}\right|_{N = N^-}$')
   # sl_epsilon_label = ax.text(i_orb - 0.9, sl.integer_energies[i_orb] - 0.1, r'$\varepsilon_\mathrm{HO} = \left.\frac{dE}{dN}\right|_{N = N^-}$', color=sl.color, fontsize=12)
   sl.label_Delta_E(ax, i_orb)
   save(ax, 'fig_en_curve_sl_annotated.pdf')
   ax.set_xlim([0.75, 2.25])
   ax.set_ylim([-0.25, 1.75])
   plt.savefig('fig_en_curve_sl_annotated_zoom.pdf', format='pdf')

   # With semi-local DFT, keeping annotations
   hf.plot(ax)
   save(ax, 'fig_en_curve_with_all_sl_annotated.pdf')

   sl.remove_annotations()
   # sl_epsilon_label.remove()
   save(ax, 'fig_en_curve_with_all.pdf')

   # Stepping through the Koopman's correction
   hf.curve.remove()

   # DFT+U
   f, ax = plt.subplots(1,1)
   plt.subplots_adjust(bottom=0.2)
   exact.plot(ax, ls='--')
   ax._get_lines.get_next_color()
   sl.plot(ax)
   save(ax, 'fig_en_curve_dftu_without_correction.pdf')
   dftu_correction = ENCurve('+$U$ correction', [ax.get_ylim()[0] for _ in sl.integer_energies], -1*np.array(sl.curvature))
   dftu_correction.plot(ax)
   save(ax, 'fig_en_curve_dftu_correction.pdf')

   # Step 0: the exact solution DFT
   f, ax = plt.subplots(1,1)
   plt.subplots_adjust(bottom=0.2)
   exact.plot(ax, ls='--')
   ax._get_lines.get_next_color()
   sl.plot(ax)
   save(ax, 'fig_en_curve_koopmans_step0.pdf')

   # Step 1: the starting point
   f_i = 2.58
   point = ax.plot(f_i, sl.y[[abs(x - f_i) < 0.00001 for x in sl.x]], 'o', markersize=15)
   point_text = ax.text(f_i, sl.y[[abs(x - f_i) < 0.00001 for x in sl.x]], '1', color='w', va='center', ha='center', fontsize=8)
   point = point[0]
   save(ax, 'fig_en_curve_koopmans_step1.pdf')

   # Step 2: subtracting the curve
   # point.remove()
   point = ax.plot(np.floor(f_i), sl.y[[abs(x - np.floor(f_i)) < 0.00001 for x in sl.x]], 'o', color=point.get_color(), markersize=15)
   point = point[0]
   point_text = ax.text(np.floor(f_i), sl.y[[abs(x - np.floor(f_i)) < 0.00001 for x in sl.x]], '+2', color='w', va='center', ha='center', fontsize=8)
   mask = [x < f_i and x >= np.floor(f_i) for x in sl.x]
   ax.plot(sl.x[mask], sl.y[mask], color=point.get_color())
   save(ax, 'fig_en_curve_koopmans_step2.pdf')

   # Step 3: adding the piecewise-linear behaviour
   fixed_sl = ENCurve(None, sl.integer_energies, [0 for _ in range(len(sl.integer_energies) - 1)])
   # point.remove()
   point = ax.plot(f_i, fixed_sl.y[[abs(x - f_i) < 0.00001 for x in fixed_sl.x]], 'o', color=point.get_color(), markersize=15)
   point_text = ax.text(f_i, fixed_sl.y[[abs(x - f_i) < 0.00001 for x in fixed_sl.x]], '+3', color='w', va='center', ha='center', fontsize=8)
   point = point[0]
   ax.plot(fixed_sl.x[mask], fixed_sl.y[mask], color=point.get_color())
   save(ax, 'fig_en_curve_koopmans_step3.pdf')
