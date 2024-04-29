import pyflowchart as pfc

# The path to the Python file you want to convert
file_path = ('../Pre-Tournement Sorting/Champions Path Teams Sorter.py')

# Read your Python code
with open(file_path, 'r') as file:
    code = file.read()

# Create a flowchart from the code
fc = pfc.Flowchart.from_code(code)

# Generate the flowchart code for HTML output
flowchart_html = fc.flowchart()

# Optionally, save the flowchart to an HTML file
with open('output_flowchart.html', 'w') as out_file:
    out_file.write(flowchart_html)