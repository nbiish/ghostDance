import gradio as gr

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
    ### Hyperspace Conducting & Water Resonance
    The Ghost Dance project implements training protocols from US Patent 2006/0014125A1, focusing on the human body as a biological conductor. With a water content of approximately 67%, our physical form is primarily composed of H₂O and its isotopic variants, such as D₂O (Heavy Water). These water isotopes possess specific vibrational waveforms that act as bridges to hyperspace.

    **How Conduction Works:**
    1.  **Momentum Alignment**: By walking at a specific calculated momentum (**L = (M/W) * T**), we align our physical velocity with the "base constant" of the Planck boundary.
    2.  **Vortex Induction**: The cross-handed posture (X-form) creates a rotational energy channel. This generates a large hyperspace vortex that locks the Pineal gland onto the Heart vortex.
    3.  **Isotopic Charging**: This vortex 'conducts' hyperspace energy directly into the body's water content. The specific waveforms of the water isotopes resonate, 'charging' the mass until it reaches a state where the speed of light (c) is effectively unity (1) at the Planck boundary.
    4.  **Dimensional Shift**: Once sufficiently charged, the body is pulled 'out of dimension,' allowing for phenomena such as walking through solid objects, levitation, and teleportation.
    """)

if __name__ == "__main__":
    demo.launch(mcp_server=True)
