# CSV temperature plots

Install Python 3.10 or newer, then install the dependencies once:

```sh
python -m pip install -r requirements.txt
```

Put your CSV files in the same folder as `read_data.py` and run:

```sh
python read_data.py
```

The script discovers all `.csv` files (including `.CSV`), prints the row count
and linear fit results, and plots temperature (y) against its time derivative (x)
for each run, including the fitted line. It saves a graph beside each file with the same
name and a `.png` extension. Existing graphs with that name are overwritten.
Add more CSV files and run the command again to process them.
Files are discovered each time you run the command;
the script does not watch the folder in the background.

To process another folder:

```sh
python read_data.py "path/to/measurements"
```

The first CSV column contains time in seconds. Every remaining column is a run
containing temperatures in degrees Celsius. Column names can be chosen freely:

```csv
Time,Temperature Run 1,Temperature Run 2
0,67.23,73.05
0.05,67.21,73.09
```

UTF-8 files with or without a BOM are supported. An optional units row with `s`
in the first column is skipped. Derivatives use a five-point central difference
and require uniformly spaced times. The first and last two samples have no
derivative. Blank temperature cells are read as NaN and passed through to the
derivatives and linear regression.
Invalid files are reported by filename while
the remaining files continue processing; the command exits with status 1 if any
file fails.
