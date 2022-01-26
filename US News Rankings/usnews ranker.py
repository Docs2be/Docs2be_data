import pandas as pd
import numpy as np
import plotly.express as px

# Importing and processing the df
def us_news_plotter():
    # Cleaning the data using a relative path (.. or .)
    #main_dir = "C:/Users/TooFastDan/Documents/MD_PhD Application/Nonprofit"
    usnews = pd.read_excel("../US News Rankings/hist_med_school_rank.xlsx", sheet_name="data", index_col=0)
    all_cols = list(usnews.columns)
    filt_cols = [y for y in all_cols if isinstance(y, int)]  # filtering for only integer columns with year numbers
    usnews = usnews[filt_cols]
    usnews = usnews.replace(".", np.nan)
    usnews = usnews.reset_index()
    usnews = usnews.rename(columns={"index": "school"})

    # Renaming schools to be consistent with AAMC data
    usnews["school"] = usnews["school"].replace({
        "Hopkins": "Johns Hopkins",
        "WashU": "Washington U St Louis",
        "Penn": "Pennsylvania-Perelman",
        "UCSF": "UC San Francisco",
        "Columbia": "Columbia-Vagelos",
        "Cornell": "Cornell-Weill",
        "UCLA": "UCLA-Geffen",
        "Vandy": "Vanderbilt",
        "UCSD": "UC San Diego",
        "Pitt": "Pittsburgh",
        "Northwestern": "Northwestern-Feinberg",
        "Chicago": "Chicago-Pritzker",
        "UNC-CH": "North Carolina",
        "Case": "Case Western Reserve",
        "U Alabama": "Alabama",
        "U Iowa": "Iowa-Carver",
        "UVA": "Virginia",
        "NYU": "NYU-Grossman",
        "Sinai": "Mount Sinai-Icahn",
        "BU": "Boston",
        "U Colorado": "Colorado",
        "U Oregon": "Oregon",
        "Dartmouth": "Dartmouth-Geisel",
        "USC": "Southern Cal-Keck",
        "OSU": "Ohio State",
        "U Minn - TC": "Minnesota",
        "IU - Indianapolis": "Indiana",
        "Brown": "Brown-Alpert",
        "UF": "Florida",
        "U Utah": "Utah",
        "U Kentucky": "Kentucky",
        "Jefferson": "Jefferson-Kimmel",
        "Med Col Wisco": "MC Wisconsin",
        "U Mass - Worch": "Massachusetts",
        "U Miami": "Miami-Miller",
        "Stony Brook": "Renaissance Stony Brook",
        "Temple": "Temple-Katz",
        "U Illinois": "Illinois",
        "USF": "USF-Morsani"
    })

    # Melting to make things graphable
    usnews = usnews.melt(id_vars="school", value_vars=usnews.columns[1:], var_name="year", value_name="rank")

    # Using plotly to graph school rank data over time
    fig = px.line(data_frame=usnews, x="year", y="rank", line_group="school", color="school",
                  title="USNews Research Ranks Over Time", width=1300, height=800)
    fig['layout']['yaxis']['autorange'] = "reversed"
    return fig.show()

us_news_plotter()