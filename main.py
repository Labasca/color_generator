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


def get_adjusted_lightness_ranges(num_colors):
    # Adjust lightness ranges based on number of colors
    if num_colors <= 3:
        return {
            'grey_start': 30,
            'grey_end': 85,
            'color_start': 40,
            'color_end': 75
        }
    elif num_colors <= 5:
        return {
            'grey_start': 25,
            'grey_end': 90,
            'color_start': 35,
            'color_end': 80
        }
    else:
        return {
            'grey_start': 20,
            'grey_end': 95,
            'color_start': 35,
            'color_end': 80
        }


def generate_hex_colors(hue, num_colors, saturation_position):
    # Get adjusted lightness ranges based on number of colors
    ranges = get_adjusted_lightness_ranges(num_colors)

    # Saturation values are ordered to generate grey colors first
    saturation_values = [0, saturation_position]

    # Adjust distribution when total colors aren't evenly divisible
    num_colors_per_saturation = [num_colors // 2 + (num_colors % 2 > i) for i in range(len(saturation_values))][::-1]

    # Generate the color list
    colors = []
    for idx, saturation in enumerate(saturation_values):
        if saturation == 0:
            # Grey colors
            lightness_start = ranges['grey_start']
            lightness_end = ranges['grey_end']
        else:
            # Colorful colors
            lightness_start = ranges['color_start']
            lightness_end = ranges['color_end']

        num_in_group = num_colors_per_saturation[idx]

        # Handle special case when only 1 color in group
        if num_in_group == 1:
            # Use middle lightness value for single colors
            middle_lightness = (lightness_start + lightness_end) / 2
            colors.append(hsl_to_hex(hue, saturation, middle_lightness))
            continue

        step = (lightness_end - lightness_start) / (num_in_group - 1)

        if saturation == 0:
            # Normal progression for 0% saturation
            colors += [
                hsl_to_hex(hue, saturation, lightness_start + i * step)
                for i in range(num_in_group)
            ]
        else:
            # Reverse progression for saturated colors
            colors += [
                hsl_to_hex(hue, saturation, lightness_end - i * step)
                for i in range(num_in_group)
            ]

    return colors


# Parameters
saturation_position = 78  # Adjustable saturation level
hue = 221
num_colors = 20  # Adjusted for an odd total to test uneven distribution

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
