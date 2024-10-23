import plotly.graph_objects as go
import colorsys

def hsl_to_hex(h, s, l):
    # Convert HSL to a range used by colorsys (h between 0 and 1, s and l between 0 and 1)
    h = h / 360
    s = s / 100
    l = l / 100
    # Convert HSL to RGB using colorsys
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    # Convert RGB to HEX
    return f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"

def generate_hex_colors(hue, num_colors, saturation_position, lightness_ends=[95, 80]):
    # Define the starting lightness level
    lightness_start = 20

    # Saturation values are ordered to generate grey colors first
    saturation_values = [0, saturation_position]

    # Adjust distribution when total colors aren't evenly divisible
    # The second saturation group gets the extra color when num_colors is odd
    num_colors_per_saturation = [num_colors // 2 + (num_colors % 2 > i) for i in range(len(saturation_values))][::-1]

    # Generate the color list
    colors = []
    for idx, (saturation, lightness_end) in enumerate(zip(saturation_values, lightness_ends)):
        step = (lightness_end - lightness_start) / (num_colors_per_saturation[idx] - 1)
        if saturation == 0:
            # Normal progression for 0% saturation
            colors += [
                hsl_to_hex(hue, saturation, lightness_start + i * step)
                for i in range(num_colors_per_saturation[idx])
            ]
        else:
            # Reverse progression for saturated colors
            colors += [
                hsl_to_hex(hue, saturation, lightness_end - i * step)
                for i in range(num_colors_per_saturation[idx])
            ]

    return colors

# Parameters
saturation_position = 70  # Adjustable saturation level
hue = 138
num_colors = 17  # Adjusted for an odd total to test uneven distribution

# Generate colors
colors = generate_hex_colors(hue, num_colors, saturation_position)

# Plotting
fig = go.Figure()
for i, color in enumerate(colors):
    # Stacking bars vertically
    fig.add_trace(go.Bar(
        x=[1],  # Dummy value for bar width
        y=[10],  # Constant height for all bars
        base=i * 10,  # Multiply by 10 to stack bars without overlapping
        orientation='v',  # Vertical bars
        marker_color=color,
        text=color,
        textposition='auto',
        width=10,  # Fixed width for all bars
        showlegend=False
    ))

fig.update_layout(
    title="HEX Color Generation (Uniform Width, Vertical Stacking)",
    xaxis_title="Color Index",
    yaxis=dict(showticklabels=False, range=[0, num_colors * 10]),  # Hide Y-axis ticks, adjust range to fit all bars
    plot_bgcolor="white",
    bargap=0.05  # Small gap between bars to visually separate them
)
fig.show()
