from ase import build
from koopmans.workflows import SinglepointWorkflow

# Create an Atoms object
atoms = build.molecule('H2O', vacuum=5.0)

# Create a koopmans Workflow object
workflow = SinglepointWorkflow(atoms=atoms)

# Run the workflow
workflow.run()
