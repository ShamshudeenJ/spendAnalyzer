# spendAnalyzer

To Track the personal expense and plot them w.r.t Time


## Initial setup

```console
python -m venv venv
git clone https://github.com/ShamshudeenJ/spendAnalyzer.git
cd spendAnalyzer
.\venv\Scripts\activate
pip install -r .\requirements.txt
```
## To run Application

```console
streamlit run .\src\main.py
```

## To export Jupyter notebook to Static HTML page

```console
jupyter nbconvert --execute --to html .\src\notebooks\main.ipynb --no-input
```