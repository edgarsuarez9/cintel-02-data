import plotly.express as px
from shiny.express import input, ui, render
from shinywidgets import render_plotly
import palmerpenguins  # This package provides palmer penguins dataset
import seaborn as sns
import numpy as np

penguins_df = palmerpenguins.load_penguins()

# Filter out rows with NaN values in the "body_mass_g" column
penguins_df = penguins_df.dropna(subset=["body_mass_g"])

ui.page_opts(title="Suarez Penguin Data", fillable=True)

# Adds a shiny ui sidebar for user interaction
with ui.sidebar(open="open"):
    # use ui.h2() funtion to add a 2nd level header to the sidebar
    ui.h2("Sidebar")

    #Use ui.input_selectize() to create a dropdown input to choose a column
    ui.input_selectize(
        "selected_attribute",
        "Select Attribute",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
    )

    #use ui.input_numeric() to create a numeric input for the number of plotly histogram bins
    ui.input_numeric("Plotly_bin_count", "Bin Count", 1, min=1, max=50)

    # Use ui.input_slider() to create a slider input for the number of Seaborn bins
    ui.input_slider("seaborn_bin_count", "Seaborn Slider", 0, 100, 50)

    #use ui.input_checkbox_group() to create checkbox group input to filter species
    ui.input_checkbox_group("Selected_Species_list", "Species Checkbox", ["Adelie", "Gentoo", "Chinstrap"], selected=["Adelie"], inline=True,)

    #use ui.hr() to add a horizontal rule to the sidebar
    ui.hr()

    #use ui.a() to add a hyperlink to the sidebar
    ui.a("Github", href="https://github.com/edgarsuarez9/cintel-02-data/tree/main", target="_blank",)

#create Data Table and Data Grid 

with ui.layout_columns(col_widths=(20, 80)):
    with ui.card(full_screen=True):
        
        ui.h4("Palmer Penguins Data Table")
        @render.data_frame
        def penguins_datatable():
            return render.DataTable(penguins_df)

#create Data Grid (showing all data)
    with ui.card(full_screen=True):
        
        ui.h4("Palmer Penguins Data Grid")
        @render.data_frame
        def penguins_data():
            return render.DataGrid(penguins_df)    

#create a Plotly Histogram (showing all species)
with ui.layout_columns(col_widths=(20, 80)):
    with ui.card(full_screen=True):
        ui.h4("Species Histogram")

        @render_plotly
        def plotly_histogram():
            return px.histogram(penguins_df, x="species", color="species")

#create a Seaborn Histogram (showing all species)   
    with ui.card(full_screen=True):
        ui.h4("Seaborn Histogram")
        @render.plot(alt="Seaborn Histogram")
        def seaborn_histogram():
            bins = input.seaborn_bin_count()
            ax = sns.histplot(data=penguins_df, x="body_mass_g", bins=bins, hue="species")  
            ax.set_title("Palmer Penguins")
            ax.set_xlabel("Mass")
            ax.set_ylabel("Count")
            return ax   

#create a plotly scatterplot (showing all species)
    with ui.card(full_screen=True):

        ui.card_header("Plotly Scatterplot: Species")

        @render_plotly
        def plotly_scatterplot():
            return px.scatter(penguins_df, title="Plotly Scatter Plot", x="body_mass_g", y="bill_depth_mm", color="species", labels={
                "bill_length_mm": "Bill Length (mm)",
                "body_mass_g": "Body Mass (g)",
            })
