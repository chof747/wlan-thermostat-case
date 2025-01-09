import FreeCAD
import Part
import Mesh
import os
import sys

# Define the directories
components_dir = 'components'
stl_dir = 'stl'

# Ensure the STL directory exists
if not os.path.exists(stl_dir):
  os.makedirs(stl_dir)

# Read the .stlignore file if it exists
ignore_list = []
ignore_file_path = os.path.join(components_dir, '.stlignore')
if os.path.exists(ignore_file_path):
    with open(ignore_file_path, 'r') as ignore_file:
        ignore_list = [line.strip() for line in ignore_file if line.strip()]

# Scan for FCStd files in the components directory
for filename in os.listdir(components_dir):
  if filename.endswith('.FCStd'):

    # Check if the file is in the ignore list
    if filename in ignore_list:
      print(f"Skipping {filename} as it is listed in .stlignore")
      continue

    # Load the FreeCAD document
    doc_path = os.path.join(components_dir, filename)
    base_na me = os.path.splitext(filename)[0]

    print("\n#####")
    print(f'Opening: {base_name} from "{doc_path}"')

    doc = None        
    try:
      # Load the FreeCAD document
      doc = FreeCAD.open(doc_path)
    except Exception as e:
      print(f"Exception opening file: {doc_path} [{e}]")
      continue
    
    # Export each body as an STL file
    for obj in doc.Objects:
      if obj.TypeId == 'PartDesign::Body' and obj.Shape.Volume != 0 and obj.Label == base_name:
        stl_path = os.path.join(stl_dir, f"{base_name}.stl")
        Mesh.export([obj], stl_path)
        print(f"Exported {stl_path}")
          

    # Close the document
    FreeCAD.closeDocument(doc.Name)

print("Exporting complete.")
sys.exit(0)
