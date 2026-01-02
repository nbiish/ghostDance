from docling.document_converter import DocumentConverter
import gradio as gr
from fastmcp import FastMCP
import sys
import os

# Create MCP server
mcp = FastMCP("GhostDance")

# Constants from the patent
# Updated to match the patent more precisely: 50.909573606
M_CONSTANT = 50.909573606

def calculate_step(weight: float, unit: str):
    """
    Calculates the step length for the Ghost Dance based on weight.
    Returns full step (1s) and half step (0.5s) distances.
    """
    if weight <= 0:
        return "N/A", "N/A", "N/A", "N/A"

    # Convert weight to kilograms if needed
    weight_in_kg = weight * 0.453592 if unit == "pounds" else weight
    
    # Calculate step length using formula L=(M/W)*T
    # where T = 1 second
    full_meters = (M_CONSTANT / weight_in_kg) * 1
    full_feet = full_meters * 3.28084
    
    # Calculate half-step length (T = 0.5 seconds)
    half_meters = full_meters / 2
    half_feet = full_feet / 2
    
    return (
        f"{full_meters:.3f} meters", 
        f"{full_feet:.3f} feet",
        f"{half_meters:.3f} meters",
        f"{half_feet:.3f} feet"
    )

# Register MCP tool
@mcp.tool()
def ghost_dance_calculation(weight: float, unit: str = "pounds") -> str:
    """
    Calculate the required step length for the Ghost Dance.
    
    Args:
        weight: Weight of the person.
        unit: Unit of weight ('pounds' or 'kilograms').
    """
    full_m, full_f, half_m, half_f = calculate_step(weight, unit)
    return (
        f"To perform the Ghost Dance at your weight ({weight} {unit}):\n"
        f"- Full Step (1.0s): {full_m} ({full_f})\n"
        f"- Half Step (0.5s): {half_m} ({half_f})"
    )

@mcp.tool()
def convert_document_to_markdown(file_path: str) -> str:
    """
    Expertly convert any document (PDF, DOCX, PPTX, etc.) to clean Markdown using Docling.
    
    Args:
        file_path: Path to the document to convert.
    """
    if not os.path.exists(file_path):
        return f"Error: File not found at {file_path}"
    
    try:
        converter = DocumentConverter()
        result = converter.convert(file_path)
        md_output = result.document.export_to_markdown()
        
        # Determine output path
        base_name = os.path.splitext(file_path)[0]
        output_path = f"{base_name}_converted.md"
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_output)
            
        return f"Successfully converted {file_path} to {output_path}. First 500 characters:\n\n{md_output[:500]}..."
    except Exception as e:
        return f"Error during conversion: {str(e)}"

# Gradio UI
with gr.Blocks(title="Ghost Dance - A continued prophecy") as demo:
    gr.HTML("<h1 style='text-align: center;'>Ghost Dance - A continued prophecy</h1>")
    gr.Markdown("This is the patent that the math is based on: [US20060014125A1](https://patents.google.com/patent/US20060014125A1/en)")
    
    with gr.Accordion("Basics from the patent"):
        gr.Markdown("""
        **INSTRUCTIONS**: Input weight and then step at designated distance per second.

        The calculation is based on the average person's water content at 67%. 
        Because the atoms making up water sit near the `Planck boundary`, 
        we are able to move that mass outside of the boundary.
        """)
    
    with gr.Row():
        with gr.Column():
            weight_input = gr.Number(label="Weight", value=180.0, minimum=1.0)
            unit_input = gr.Radio(["pounds", "kilograms"], label="Unit", value="pounds")
            calc_btn = gr.Button("Calculate Stride", variant="primary")
        
        with gr.Column():
            with gr.Group():
                gr.Markdown("### Full Step (1.0 second)")
                full_meters_output = gr.Textbox(label="Meters")
                full_feet_output = gr.Textbox(label="Feet")
            
            with gr.Group():
                gr.Markdown("### Half Step (0.5 seconds)")
                half_meters_output = gr.Textbox(label="Meters")
                half_feet_output = gr.Textbox(label="Feet")
    
    calc_btn.click(
        fn=calculate_step,
        inputs=[weight_input, unit_input],
        outputs=[full_meters_output, full_feet_output, half_meters_output, half_feet_output]
    )
    
    gr.Markdown("### Use a metronome to improve your accuracy.")
    gr.HTML('<div style="display: flex; justify-content: center;"><iframe width="560" height="315" src="https://www.youtube.com/embed/ymJIXzvDvj4?start=79" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></div>')

    gr.Markdown("""
    ### Project Intent Review
    The Ghost Dance project implements the training protocols detailed in US Patent 2006/0014125A1. Its primary intent is to enable individuals to acquire sufficient 'hyperspace energy' to transition the physical body out of our dimension. By calculating a specific walking stride relative to body mass and maintaining a cross-handed posture, the system aims to generate a resonant vortex that pulls the body through the Planck boundary. This theoretical shift into hyperspace is claimed to facilitate walking through solid matter, levitation, and teleportation, leveraging the high water content of the human body as a conductive medium for subspace energy.
    """)

if __name__ == "__main__":
    # Check for mcp argument
    if len(sys.argv) > 1 and sys.argv[1] == "mcp":
        mcp.run()
    else:
        demo.launch()
