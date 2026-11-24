# Sales Data Analysis + Interactive Dashboard

## Project files
- `sales_data.csv` — sample retail sales dataset
- `sales_analysis.py` — original Python analysis and static chart script
- `dashboard.py` — interactive Streamlit dashboard
- `requirements.txt` — required Python libraries

## Run in VS Code (Windows)

1. Extract this ZIP file.
2. Open the `Sales_Data_Analysis_Dashboard` folder in VS Code.
3. Open **Terminal → New Terminal**.
4. (Optional but recommended) Create a virtual environment:

   ```bash
   python -m venv venv
   ```

5. Activate it:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, you can skip the virtual environment and continue.

6. Install the libraries:

   ```bash
   python -m pip install -r requirements.txt
   ```

7. Start the dashboard:

   ```bash
   python -m streamlit run dashboard.py
   ```

8. Streamlit will open the dashboard in your browser. If it does not, copy the
   `Local URL` shown in the terminal (usually `http://localhost:8501`) into Chrome.

## How to use the dashboard
- Use the left sidebar to filter by city, category, and product.
- KPI cards update based on your selected filters.
- Explore product, city, category, and monthly revenue charts.
- Scroll down to view the filtered records and download them as CSV.

## Run the original analysis script
To generate the original summary CSV files and PNG charts in the `output` folder:

```bash
python sales_analysis.py
```

## Revenue calculation
Revenue = (Quantity × Unit Price) − Discount

The included dataset is sample practice data, not actual company/customer data.
