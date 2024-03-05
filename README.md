# Dicoding Data Analyst Submission

## Dataset
[Bike Sharing Dataset](https://drive.google.com/file/d/1RaBmV6Q6FYWU4HWZs80Suqd7KQC34diQ/view?usp=sharing) [(Sumber)](https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset)

## Folder Structure
```bash
├── dashboard
│   ├── bicycle.jpg
│   └── dashboard.py
│   └── day.csv
│   └── hour.csv
├── data
│   ├── Readme.txt
│   └── day.csv
│   └── hour.csv
├── README.md
├── notebook.ipynb
├── requirements.txt
└── url.txt
```

## Setup environment
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install numpy pandas scipy matplotlib seaborn jupyter streamlit babel
```

## Run streamlit app (local)
1. Clone this repository
   ```
   https://github.com/angelatungky/dashboard-task.git
   ```
2. Direct the path to the dashboard directory
   ```
   cd dashboard-task/dashboard
   ```
3. Run streamlit app
   ```
   streamlit run dashboard.py
   ```

## Run streamlit app (cloud)
```
https://dashboard-task-dicoding.streamlit.app/
```
