# EHR Data Profiling Tool

This is a draft version of data profiling tool designed to analyze electronic health record (EHR) data and It provides insights into data quality and completeness, and helps identify areas for improvement. It will also facilitate the development of filtering and cleaning scripts for health dataset.

## Features

- **Data profiling:** Provides detailed statistics and summaries of EHR data, including missing values, duplicates, and outliers.
- **Data visualization:** Generates interactive graphs and visualizations to help users better understand their EHR data.
- **Data quality assessment:** Evaluates data quality based on a set of pre-defined rules and flags any issues that require attention.
- **Data completeness assessment:** Calculates data completeness percentages for each field in the EHR dataset and identifies fields with low completion rates.
- **Data field distribution analysis:** Provides visualizations and statistics to help users understand the distribution of values in each field.

## Getting Started

To get started with this tool, you will need to have access to a dataset of electronic health records. You will also need to have Python 3 installed on your machine.

1. Clone this repository to your local machine.
2. Install the required Python packages using `pip install -r requirements.txt`.
3. Open `data_profiling_tool.py` and update the file path to your EHR dataset.
4. Run the tool using `python data_profiling_tool.py`.

## Contributing

If you find any bugs or have suggestions for new features, please create a new issue in this repository. Pull requests are also welcome.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.