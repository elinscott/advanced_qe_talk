from koopmans.io import read

# Read in the input file
workflow = read('h2o.json')

# Run the workflow
workflow.run()
