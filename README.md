# Buenos Aires Public Transport Analysis

> Data analysis project exploring how bus stops are distributed across Buenos Aires (CABA)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://caba-public-transport-analysis-mxjtgaunapfehj73pqd5cf.streamlit.app/)

## What is this project about?

This is my first complete data analysis project. I wanted to understand how public transportation works in Buenos Aires by looking at where bus stops are located throughout the city. The idea was simple: download some real data, clean it up, explore it, and create something visual that people can interact with.

I'm not trying to build a complex model or anything super technical - I just wanted to answer basic questions like: Which neighborhoods have more bus stops? Where are the busiest streets? How does coverage look across different areas?

## Where did I get the data?

All the data comes from the **Buenos Aires Open Data Portal** (https://data.buenosaires.gob.ar), which is a free resource where the city government shares datasets about the city. I downloaded four GeoJSON files:

- **Bus Stops** ([link](https://data.buenosaires.gob.ar/dataset/colectivos-paradas)): Every bus stop in the city with its location, street address, and which bus lines stop there
- **Streets** ([link](https://data.buenosaires.gob.ar/dataset/calles)): The street network of Buenos Aires
- **Comunas** ([link](https://data.buenosaires.gob.ar/dataset/comunas)): The 15 administrative districts that divide the city
- **Barrios** ([link](https://data.buenosaires.gob.ar/dataset/barrios)): The 48 neighborhoods of Buenos Aires

These files are basically like spreadsheets with geographic information attached - they have regular data columns plus a "geometry" column that stores the shapes and locations.

## What did I do?

### 1. Data Cleaning ([01_data_cleaning.ipynb](notebooks/01_data_cleaning.ipynb))

This was probably the hardest part. I had to:

- **Fix column names**: Make everything lowercase and consistent
- **Handle encoding issues**: Some Spanish characters (like ñ in "NUÑEZ") were showing up as weird symbols (�). I had to match these corrupted names with the correct ones
- **Fix typos**: Found neighborhoods with wrong spellings like "BARRANCAS" instead of "BARRACAS"
- **Remove invalid data**
- **Standardize text**: Made all street names and neighborhood names consistent so I could match them across datasets
- **Aggregate streets**: Streets were stored as thousands of tiny segments, so I grouped them by name to make analysis easier

### 2. Exploratory Data Analysis ([02_EDA_bus_stops.ipynb](notebooks/02_EDA_bus_stops.ipynb))

After cleaning, I explored the data to understand patterns. Here's what I looked at:

**Basic counts:**
- How many bus stops are there in total?
- How are they distributed across comunas and neighborhoods?
- Which areas have the most stops?

**Density analysis:**
- I calculated "stops per square kilometer" because just counting stops isn't fair - bigger areas naturally have more stops
- This helped me see which neighborhoods are actually well-covered vs. just large

**Street analysis:**
- Which streets have the most bus stops?
- These are usually the main avenues that cross large parts of the city

**Bus lines coverage:**
- Which bus lines serve the most stops?
- Which areas have the most variety of bus lines available?
- Where do many lines overlap? (these could be important transfer points)

I used maps (choropleth and hexbin) and bar charts to visualize all of this. Maps are great for seeing spatial patterns, and charts make it easy to compare numbers.

### 3. Interactive Dashboard ([dashboards/](dashboards/))

After doing all this analysis in notebooks, I wanted to make it interactive so anyone could explore it without running Python code. I built a **Streamlit dashboard** with four pages:

- **Home**: Introduction and overview
- **Overview**: General counts and distributions by comuna/barrio
- **Stops Density**: Shows density (stops per km²) instead of raw counts
- **Streets with Most Stops**: Highlights the main corridors
- **Lines & Coverage**: Explores bus line diversity and coverage

Streamlit was perfect for this because it's simple to use - you write Python and it creates a web app automatically.

## What tools did I use?

Here's everything I used and why:

- **Python**: The main programming language - it's popular for data analysis and has great libraries
- **pandas**: For working with tabular data (like spreadsheets) - loading, filtering, aggregating
- **geopandas**: Like pandas but for geographic data - lets you work with maps and locations
- **matplotlib & seaborn**: For creating charts and plots in the notebooks
- **plotly**: For interactive charts in the dashboard
- **shapely**: For geometric operations (checking if a point is inside a boundary, etc.)
- **streamlit**: For building the interactive web dashboard

I chose these because they're the standard tools in data analysis, they have good documentation, and there are tons of tutorials online.

## Project structure

```
├── data/
│   ├── raw/                    # Original GeoJSON files from the open data portal
│   └── processed/              # Cleaned data saved as GeoPackage files
├── notebooks/
│   ├── 01_data_cleaning.ipynb  # All the data cleaning steps
│   └── 02_EDA_bus_stops.ipynb  # Exploratory analysis and visualizations
├── dashboards/
│   ├── Home.py                 # Main dashboard page
│   ├── pages/                  # Each page of the dashboard
│   └── utils/                  # Helper functions for the dashboard
├── src/
│   ├── normalize_columns.py    # Function to standardize column names
│   └── normalize_strings.py    # Function to clean up text data
└── requirements.txt            # List of all Python libraries needed
```

## How to run this project

1. Clone this repository
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. To see the dashboard:
   ```bash
   cd dashboards
   streamlit run Home.py
   ```
4. To explore the analysis, open the Jupyter notebooks in the `notebooks/` folder

## What I learned

This was my first complete project from start to finish, and I learned a ton:

- **Real data is messy**: I spent way more time cleaning data than I expected.
- **Start simple**: I didn't try to do anything fancy - just clean the data, explore it, and visualize it. That was enough for a first project
- **Geospatial data is different**: Working with maps and coordinates adds complexity, but geopandas makes it manageable
- **Documentation matters**: The notebooks explain what I did and why. This helps me remember later and helps others understand
- **Iterative process**: I went back and forth between cleaning and analysis many times.

## What's next?

Some ideas for future improvements:
- **Include train and subte (subway) data**: Combine bus stops with train stations and subway stations to get a complete picture of public transport coverage
- Calculate accessibility metrics (how far is the average person from a bus stop?)
- Compare this with population density data
- Add more interactivity to the dashboard (filters, selection tools)
