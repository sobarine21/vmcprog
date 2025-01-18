import streamlit as st
import pythreejs
import pycam
import numpy as np
from stl import mesh
import io

# Streamlit App UI
st.title("CNC VMC Design Copilot")
st.write("Use Generative AI to design CNC VMC models and generate G-code files with enhanced features.")
st.write("This app can also visualize your 3D models and generate toolpaths using pycam.")

# Part Specifications
st.header("Part Specifications")
shape = st.selectbox("Select Part Shape:", ["Cylinder", "Cube", "Cone", "Sphere", "Prism", "Custom"])
diameter = st.number_input("Enter diameter (mm):", min_value=1, value=50)
height = st.number_input("Enter height (mm):", min_value=1, value=100)
length = st.number_input("Enter length (mm):", min_value=1, value=100) if shape in ["Cube", "Prism"] else 0
width = st.number_input("Enter width (mm):", min_value=1, value=50) if shape in ["Prism", "Cube"] else 0

material = st.selectbox("Select material:", ["Aluminum", "Steel", "Titanium", "Brass", "Plastic", "Other"])

# Tooling Information
tool_type = st.selectbox("Select tool type:", ["End Mill", "Ball End Mill", "Face Mill", "Drill", "Tap", "Reamer", "Slot Cutter"])
tool_diameter = st.number_input("Enter tool diameter (mm):", min_value=1, value=10)
cutting_speed = st.number_input("Enter cutting speed (mm/min):", min_value=1, value=150)
feed_rate = st.number_input("Enter feed rate (mm/min):", min_value=1, value=100)
depth_of_cut = st.number_input("Enter depth of cut (mm):", min_value=0.1, value=5.0)

# Upload 3D Model (STL)
st.header("Upload and Visualize 3D Model")
uploaded_file = st.file_uploader("Upload 3D model (STL)", type=["stl"])

if uploaded_file is not None:
    # Read the uploaded STL file and display it using pythreejs
    st.write("3D Model Visualization")
    
    # Load the STL model using pycam or other libraries
    stl_mesh = mesh.Mesh(io.BytesIO(uploaded_file.read()))
    
    # Convert the model into 3D mesh for visualization using pythreejs
    geometry = pythreejs.BufferGeometry(attributes={
        'position': pythreejs.BufferAttribute(np.array(stl_mesh.vectors).reshape(-1, 3).astype(np.float32), 3)
    })
    
    material = pythreejs.MeshLambertMaterial(color='blue')
    mesh = pythreejs.Mesh(geometry=geometry, material=material)
    
    scene = pythreejs.Scene(children=[mesh, pythreejs.AmbientLight(intensity=0.5)])
    camera = pythreejs.PerspectiveCamera(position=[3, 3, 3], lookAt=[0, 0, 0])
    
    renderer = pythreejs.WebGLRenderer(camera=camera, scene=scene, width=600, height=400)
    
    # Display the 3D model in Streamlit
    st.write(renderer)

# Toolpath Generation and G-code Creation using Pycam
st.header("Generate Toolpath and G-code")

if uploaded_file is not None:
    # Generate toolpath using pycam (simulating roughing operation)
    st.write("Generating Toolpath...")
    
    # Save the uploaded STL file to disk
    with open("uploaded_model.stl", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Example of using pycam to load model and generate a toolpath
    part = pycam.load_model("uploaded_model.stl")
    
    # Generate toolpath (for simplicity, using roughing operation here)
    toolpath = part.generate_toolpath(operation="roughing", tool_diameter=tool_diameter, cutting_speed=cutting_speed, feed_rate=feed_rate, depth_of_cut=depth_of_cut)
    
    # Convert the toolpath into G-code
    gcode = toolpath.to_gcode()
    
    # Display the G-code and provide download option
    st.text_area("Generated G-code", gcode)
    st.download_button("Download G-code", data=gcode, file_name="generated_toolpath.gcode")

# Display Success Message
st.write("CNC Design and Toolpath Generation Complete!")
