from ase.build import bulk
from koopmans.kpoints import Kpoints
from koopmans.projections import ProjectionBlocks
from koopmans.workflows import SinglepointWorkflow

# Use ASE to create bulk silicon
atoms = bulk('Si')

# Define the projections for the Wannierization (same for filled and empty manifold)
si_proj = [{'fsite': [0.25, 0.25, 0.25], 'ang_mtm': 'sp3'}]
si_projs = ProjectionBlocks([{'filled': True, **si_proj},
                             {'filled': False, **si_proj}],
                             atoms=atoms)

# Create the workflow
workflow = SinglepointWorkflow(atoms = atoms,
        projections = si_projs,
        ecutwfc = 40.0,
        kpoints = Kpoints(grid=[8, 8, 8], path='LGXKG', cell=atoms.cell),
        calculator_parameters = {'pw': {'nbnd': 10},
        'w90_emp': {'dis_froz_max': 10.6, 'dis_win_max': 16.9}})

# Run the workflow
workflow.run()
