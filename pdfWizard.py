"""
"""


# PACKAGE IMPORTS
from fpdf import FPDF
import pandas as pd                 # Pandas, used to represent CSVs and large data sets as a DataFrame.
import numpy as np                  # NumPy, adds Arrays to python and enables large arithmatic operations.
import matplotlib.pyplot as plt     # MatPlotLib's PyPlot, used to graph data sets and create data visualizations.
import argparse, os, shutil         # Argparse, OS, and Shutil, used for File Manipulation and the Command Line Interface
import json                         # JSON, used to parse JSON files and convert to Dictionary data types.

# LOCAL FILE IMPORTS
import analyticsEngine as ae        # AnalyticsWizard, used as an API to parse and process the Bulk Upload Data File into small chunks of information.

# IMPORT CONSTANTS
TEXT_SAVE_NAME = "resources/text.json"                                                  # Path to TEXT save file (JSON).
with open(TEXT_SAVE_NAME) as file: TEXT = json.load(file)                               # TEXT, used for all of the text in the PDF report; stored in the file, 'resources/text.json'.

# MISC CONSTANTS
WIDTH = 8.3
HEIGHT = 11

# COLOURS
VIVERY_GREEN = (0, 72, 61)

# STYLES





# PDFCONSTRUCTOR CLASS
class pdfConstructor:
    """
    """
    def __init__(
            self, 
            new_df: pd.DataFrame(), 
            new_directory: str,
            new_filename: str,
            new_network_name: str
            ) -> None:
        """
        """
        # Initialize class variables
        self.df = new_df
        self.directory = new_directory
        self.filename = new_filename
        self.network_name = new_network_name

        # Add network name to TEXT
        TEXT["FILE"]["network name"] = new_network_name
        
        # Create PDF
        self.pdf = FPDF(orientation='P', unit='in', format='A4')
        self.pdf.set_top_margin(1)
        self.pdf.set_auto_page_break(1)
        self.pdf.set_left_margin(1)
        self.pdf.set_right_margin(1)

        # Add font family
        self.pdf.add_font('Roobert Medium', '', fname='resources\Roobert Font Suite\TTF\Roobert-Medium.ttf', uni=True)
        self.pdf.add_font('Roobert Light Italic', '', fname='resources\Roobert Font Suite\TTF\Roobert-LightItalic.ttf', uni=True)
        self.pdf.add_font('Roobert Regular', '', fname='resources\Roobert Font Suite\TTF\Roobert-Regular.ttf', uni=True)
        return
    

    def create_page(self) -> None:
        """
        """
        self.pdf.add_page()
        return
    

    def save_pdf(self) -> None:
        """
        """
        self.pdf.output(self.filename)
        try:
            shutil.move(self.filename, self.directory)
        except OSError:
            os.remove(self.directory + '/' + self.filename)
            shutil.move(self.filename, self.directory)
        return
    

    def add_image(self, graphing_function, df: pd.DataFrame, directory: str, w: int, h: int) -> None:
        """
        """
        filepath = graphing_function(df, directory)
        self.pdf.image(filepath, (WIDTH - w)/2, FPDF.get_y(self.pdf), w, h)
        self.pdf.ln(h)
        return


    def add_h1_text(self, text: str) -> None:
        """
        """
        self.pdf.set_y(FPDF.get_y(self.pdf))
        if FPDF.get_y(self.pdf) > 1:
            self.pdf.ln(0.5)
        self.pdf.set_text_color(0, 72, 61)
        self.pdf.set_font('Roobert Medium', '', 20)
        self.pdf.cell(0, 0, text, 0, 0, 'C')
        self.pdf.ln(0.3)
        return
    

    def add_h2_text(self, text: str) -> None:
        """
        """
        self.pdf.set_y(FPDF.get_y(self.pdf))
        self.pdf.set_text_color(250, 249, 246)
        self.pdf.set_font('Roobert Medium', '', 12)
        self.pdf.cell(0, 0, text, 0, 0, 'C')
        return
    

    def add_normal_text(self, text: str, alignment='L') -> None:
        """
        """
        self.pdf.ln(0.20)
        self.pdf.set_y(FPDF.get_y(self.pdf))
        self.pdf.set_text_color(0, 72, 61)
        self.pdf.set_font('Roobert Regular', '', 11)
        self.pdf.multi_cell(6.3, self.pdf.font_size, text, 0, alignment)
        return
        

    def add_linked_normal_text(self, text: str, link: str) -> None:
        """
        """
        pass


    def add_subtitle_text(self, text: str) -> None:
        """
        """
        self.pdf.ln(0.15)
        self.pdf.set_y(FPDF.get_y(self.pdf))
        self.pdf.set_text_color(0, 72, 61)
        self.pdf.set_font('Roobert Light Italic', '', 9)
        self.pdf.multi_cell(6.3, self.pdf.font_size, text, 0, 'C')


    def add_linked_subtitle_text(self, text: str, link: str) -> None:
        """
        """
        pass


    def add_horizontal_line(self, x: int, y:int) -> None:
        """
        """
        pass


    def add_table(self, x: int, y:int) -> None:
        """
        """
        pass


    def add_line_break(self, height: int) -> None:
        self.pdf.ln(height)
        return




# MAIN
if __name__ == "__main__":
    # Define console parser
    parser = argparse.ArgumentParser(description="Create data visualizations for a Pre-Validated file")
    # Add file argument
    parser.add_argument("file", action="store", help="The file to validate.")
    # Add network name argument
    parser.add_argument("network_name", action="store", help="To name the PDF and customize to the specific Network")
    # Console arguments
    args = parser.parse_args()
    
    # Create directory name
    directory = "data_" + args.file.split("\\")[-1].replace(".csv", "")
    # Create network name
    network_name = args.network_name
    # Create DataFrame
    df = pd.read_csv(args.file)

    # Create directory within project folder
    if not os.path.isdir(directory):
        os.mkdir(directory)
    if not os.path.isdir(directory + "/resources"):
        os.mkdir(directory + "/resources")
    if not os.path.isdir(directory + "/csvs"):
        os.mkdir(directory + "/csvs")
    if not os.path.isdir(directory + "/images"):
        os.mkdir(directory + "/images")
    # Move file to directory
    if args.file.split("\\")[0] != directory:
        shutil.move(args.file, directory)

    # Create pdfConstructor instance
    constructor = pdfConstructor(df, directory, network_name.replace(" ", "_").lower() + TEXT["FILE"]["filename"], network_name)

    # Create PDF
    constructor.create_page()
    constructor.add_h1_text(TEXT["LOCATION MAP"]["title"])
    constructor.add_image(ae.create_map, df, directory, 6.5, 4.2)
    constructor.add_subtitle_text(TEXT["LOCATION MAP"]["subtitle"])
    constructor.add_normal_text(TEXT["LOCATION MAP"]["paragraph"], alignment='C')
    constructor.add_h1_text(TEXT["NETWORK OVERVIEW"]["title"])
    constructor.save_pdf()
