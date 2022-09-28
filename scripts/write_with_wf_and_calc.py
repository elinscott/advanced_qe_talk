from ase import build
from koopmans.workflows import SinglepointWorkflow
from koopmans.io import write

# Create an Atoms object
atoms = build.molecule('H2O', vacuum=5.0)

# Create a koopmans Workflow object
workflow = SinglepointWorkflow(atoms=atoms,
    pseudopotentials = {'H': 'H_ONCV_PBE-1.0.upf', 'O': 'O_ONCV_PBE-1.0.upf'},
    parameters = {'functional': 'kipz', 'init_orbitals': 'pz'},
    master_calc_params = {'kcp': {'ecutwfc': 50.0}})

# Write out the input file
write(workflow, 'h2o.json')
