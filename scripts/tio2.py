from ase import spacegroup
from koopmans.workflows import SinglepointWorkflow

# Create an Atoms object
a = 3.78
c = 9.51
atoms = spacegroup.crystal(['Ti', 'O'],
                           basis=[(0, 0, 0), (0, 0, 0.2)],
                           spacegroup=141,
                           cellpar=[a, a, c, 90, 90, 90])

# Create a koopmans Workflow object
workflow = SinglepointWorkflow(atoms=atoms,
     pseudopotentials = {'Ti': 'Ti_ONCV_PBE-1.0.upf', 'O': 'O_ONCV_PBE-1.0.upf'},
     ...)
