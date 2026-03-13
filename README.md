# csv_cleaner
CSV cleaner is a tool that helps users clean and preprocess CSV datasets easily.
This tool allows users to inspect datasets, handle missing values, validate data types, remove duplicates, and export cleaned data along with a report.

# How It Works ⚙️
  ### 1. Load CSV File 📂
  The user selects a CSV file through the graphical interface.
  
  The application reads the dataset using Pandas and prepares it for inspection and cleaning.
     
  ### 3. Dataset Inspection 🔍
  Once the file is loaded, the tool analyzes the dataset and provides information such as:
  * Column names
  * Detected data types
  * Missing values in each column
  * Duplicate rows
            
  This step helps users understand the structure and quality of the dataset before cleaning.
     
  ### 5. Column-wise Data Type Validation ⚙️
  Each column is displayed with a dropdown menu where the user can select the desired data type.\
  The tool then:
  1. Attempts to convert the column to the selected type
  2. Detects rows that fail conversion and convert them into NaN
  3. Reports failed conversions in the cleaning report
  4. This ensures that columns contain consistent and valid data types.
     
  ### 7. Missing Value Handling 🧩
  Before applying missing value handling methods, common representations of missing data such as "", "N/A", "null", "?", and "-" are automatically converted into NaN to ensure consistent processing.
  Users can choose different strategies to handle missing values for each column, including:
  * Dropping rows with missing values
  * Replacing with Mean
  * Replacing with Median
  * Replacing with Mode
  * Forward Fill (ffill)
  * Backward Fill (bfill)
    
  This allows flexible handling of incomplete data.
     
  ### 9. Duplicate Removal 🧹 
  The tool detects duplicate rows in the dataset and removes them automatically to ensure data uniqueness.<br>
          
          Note:
            If duplicate rows contain missing values, they may be modified during the Missing Value Handling step 
            before duplicate removal is performed. In such cases, the report may show 0 duplicates removed, 
            even though the duplicate rows were effectively resolved during the cleaning process.
            
            To verify the result, users can reload the cleaned CSV file and check the Inspection Report, 
            where the duplicate count will be 0.
     
### 11. Generate Cleaning Report 📄
After processing, the tool generates a report summarizing all operations performed, including:
* Data type conversions
* Failed conversions
* Missing value handling
* Duplicate removals
    
### 7. Export Cleaned Datset 💾
  Finally, the cleaned dataset can be exported as a new CSV file along with the generated cleaning report.

# Tech Stack 🛠️
![Python](https://img.shields.io/badge/Python-core-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-purple)
![NumPy](https://img.shields.io/badge/NumPy-Numerical%20Computing-orange)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)


# Demo 🎬
![VideoProject1-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/022f061a-6ff5-4f56-8809-4abfee47eca1)

## How to Run ▶️
Install dependencies:
* pip install pandas
* pip install NumPy

Run the application:
* python main_ui.py
