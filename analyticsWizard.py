# Import packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import argparse
import os
import shutil


def save_graph(file_name: str, directory: str, dpi: int) -> None:
    """
    """
    plt.savefig(file_name, dpi=dpi)
    try:
        shutil.move(file_name, directory)
    except:
        os.remove(directory + '\\' + file_name)
        shutil.move(file_name, directory)
    plt.close()
    return


def orgs_columns_empty(df: pd.DataFrame) -> pd.DataFrame:
    """
    """
    temp_df = df[['Organization External ID',
        'Organization Name',
        'Organization Address 1',
        'Organization Address 2',
        'Organization City',
        'Organization State',
        'Organization Zip',
        'Organization Contact Phone',
        'Organization Contact Phone Ext',
        'Organization Contact Email',
        'Organization Contact Name',
        'Organization Phone',
        'Organization Phone Ext',
        'Organization Email',
        'Organization Website',
        'Organization About Us',
        'Organization Logo',
        'Organization Approval Status',
        'Organization Active Status']].drop_duplicates(subset=['Organization External ID'], keep='last')
    temp_df['Organization Master Contact Phone'] = (temp_df['Organization Contact Phone'].astype(str) + temp_df['Organization Contact Phone Ext'].astype(str)).replace("nannan", "")
    print(temp_df['Organization Master Contact Phone'])
    temp_df['Organization Master Phone'] = (temp_df['Organization Phone'].astype(str) + temp_df['Organization Phone Ext'].astype(str)).replace("nannan", "")
    temp_df['Organization Master Address'] = (temp_df['Organization Address 1'].astype(str) + temp_df['Organization Address 2'].astype(str)).replace("nannan", "")
    temp_df = temp_df.drop(['Organization Contact Phone', 'Organization Contact Phone Ext', 'Organization Phone', 'Organization Phone Ext', 'Organization Address 1', 'Organization Address 2'], axis=1).mask(temp_df == '')
    return pd.DataFrame(data=temp_df.isna().sum())


def orgs_contact_completeness(df: pd.DataFrame, directory: str) -> None:
    """
    """
    # Collect data
    nan_count = df[['Organization External ID', 'Organization Contact Phone', 'Organization Contact Email', 'Organization Contact Name']].drop_duplicates().isna().sum(axis = 1).to_numpy()
    nan_count = (nan_count - 3) * -33

    # Create graph
    plt.hist(nan_count, edgecolor='black', bins=[-10, 10, 23, 43, 56, 76, 90, 110])
    plt.xticks(np.array([0, 33, 66, 100]), fontsize=6, labels=["No Contact Information", "Two Contact Pieces Missing", "One Contact Piece Missing", "Ready for Engagement"])
    plt.title("Organization Contact Information Engagement Levels")
    plt.xlabel("Engagement Levels")
    plt.ylabel("Number of Locations")
    save_graph("organization_contact_completeness.png", directory, 300)
    return


def locs_contact_completeness(df: pd.DataFrame, directory: str) -> None:
    """
    """
    # Collect data
    nan_count = df[['Location External ID', 'Location Contact Phone', 'Location Contact Email', 'Location Contact Name']].drop_duplicates().isna().sum(axis = 1).to_numpy()
    nan_count = (nan_count - 3) * -33

    # Create graph
    plt.hist(nan_count, edgecolor='black', bins=[-10, 10, 23, 43, 56, 76, 90, 110])
    plt.xticks(np.array([0, 33, 66, 100]), fontsize=6, labels=["No Contact Information", "Two Contact Pieces Missing", "One Contact Piece Missing", "Ready for Engagement"])
    plt.title("Location Contact Information Engagement Levels")
    plt.xlabel("Engagement Levels")
    plt.ylabel("Number of Locations")

    save_graph("location_contact_completeness.png", directory, 300)


def progs_contact_completeness(df: pd.DataFrame, directory: str) -> None:
    """
    """
    # Collect data
    nan_count = df[['Program External ID', 'Program Contact Phone', 'Program Contact Email', 'Program Contact Name']].drop_duplicates().isna().sum(axis = 1).to_numpy()
    nan_count = (nan_count - 3) * -33

    # Create graph
    plt.hist(nan_count, edgecolor='black', bins=[-10, 10, 23, 43, 56, 76, 90, 110])
    plt.xticks(np.array([0, 33, 66, 100]), fontsize=6, labels=["No Contact Information", "Two Contact Pieces Missing", "One Contact Piece Missing", "Ready for Engagement"])
    plt.title("Program Contact Information Engagement Levels")
    plt.xlabel("Engagement Levels")
    plt.ylabel("Number of Locations")

    save_graph("program_contact_completeness.png", directory, 300)


def count_orgs(df: pd.DataFrame) -> int:
    """
    Counts the number of unique organizations in a DataFrame.
    Unique organizations are determined by the 'Organization External ID' column.

    :param df: A Pandas DataFrame
    :return: The number of unique organizations, represented as an integer.
    """
    return df['Organization External ID'].nunique()


def count_valid_orgs(df: pd.DataFrame) -> int:
    """
    Counts the number of unique organizations that are both active and approved.

    :param df: A Pandas DataFrame
    :return: The number of unique organizations that are both approved and active, represented as an integer. 

    :note: Active and Approved organizations are determined by the 'Organization Active Status' and 'Organization Approved Status' columns.
    :note: Unique organizations are determined by the 'Organization External ID' column.
    """
    df = df[(df['Organization Active Status'] == True) & (df['Organization Approval Status'] == True)]
    return df['Organization External ID'].nunique()


def count_locs(df: pd.DataFrame) -> int:
    """
    Counts the number of unique locations in a DataFrame. Unique locations are determined by the 'Location External ID'.

    :param df: A Pandas DataFrame
    :return: The number of unique locations, represented as an integer.
    """
    return df['Location External ID'].nunique()


def count_valid_locs(df: pd.DataFrame) -> int:
    """
    Counts the number of unique locations that are both active and approved.

    :param df: A Pandas DataFrame
    :return: The number of unique locations that are both approved and active, represented as an integer. 
    
    :note: Active and Approved locations are determined by the 'Location Active Status' and 'Location Approved Status' columns.
    :note: Unique locations are determined by the 'Location External ID' column.
    """
    df = df[(df['Location Active Status'] == True) & (df['Location Approval Status'] == True)]
    return df['Location External ID'].nunique()


def count_progs(df: pd.DataFrame) -> int:
    """
    Counts the number of unique programs in a DataFrame. Unique programs are determined by the 'Program External ID'.

    :param df: A Pandas DataFrame
    :return: The number of unique programs, represented as an integer.
    """
    return df['Program External ID'].nunique()


def count_valid_progs(df: pd.DataFrame) -> int:
    """
    Counts the number of unique programs that are both active and approved.

    :param df: A Pandas DataFrame
    :return: The number of unique programs that are both approved and active, represented as an integer. 

    :note: Active and Approved programs are determined by the 'Program Active Status' and 'Program Approved Status' columns.
    :note: Unique programs are determined by the 'Program External ID' column.
    """
    df = df[(df['Program Active Status'] == True) & (df['Program Approval Status'] == True)]
    return df['Program External ID'].nunique()


if __name__ == "__main__":
    # Define console parser
    parser = argparse.ArgumentParser(description="Create data visualizations for a Pre-Validated file")
    # Add file argument
    parser.add_argument("file", action="store", help="The file to validate.")
    # Add silent argument
    parser.add_argument('--silent', action='store', nargs='+', help='Name of visualizations to not generate')
    # Console arguments
    args = parser.parse_args()
    
    # Create directory name
    directory = "data_" + args.file.split("\\")[-1].replace(".csv", "")
    # Create DataFrame
    df = pd.read_csv(args.file)
    # Create a list of visualization functions
    graphing_functions = [
        orgs_contact_completeness,
        locs_contact_completeness,
        progs_contact_completeness
    ]
    # Create a list of text functions
    calculating_functions = [
        orgs_columns_empty,
        count_orgs,
        count_valid_orgs,
        count_locs,
        count_valid_locs,
        count_progs,
        count_valid_progs
    ]

    # Create directory within project folder
    if not os.path.isdir(directory):
        os.mkdir(directory)
    # Move file to directory
    if args.file.split("\\")[0] != directory:
        shutil.move(args.file, directory)

    # Create list of silenced functions
    silenced_functions = args.silent if args.silent else []

    # Create valid visualizations functions
    valid_graphing_functions = [graph for graph in graphing_functions if graph.__name__ not in silenced_functions]
    # Create valid text functions
    valid_calculation_functions = [calculation for calculation in calculating_functions if calculation.__name__ not in silenced_functions]
    
    # Execute functions
    [graph(df, directory) for graph in valid_graphing_functions]
    [print(calculation.__name__ + ": " + str(calculation(df))) for calculation in valid_calculation_functions]
