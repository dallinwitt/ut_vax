# Utah Kindergarten Vaccination Rates
## Data Analysis and Visualization

#### Motivation
There has been a strong pushback recently against vaccinations, particularly the MMR vaccine, which prevents measles, a disease with a basic reproduction number (R<sub>0</sub>) around 16. This high of an R<sub>0</sub> would wreak havoc on any classroom not properly vaccinated. The goal of this project was to determine the immunization rates across kindergarten classrooms in Utah, and how that rate was influenced by factors such as locale, location, and poverty rate. 

The data for this analysis came from the [Utah open data catalog](https://opendata.utah.gov/Health/Vaccinations-By-School-District-And-School-Utah-20/3nnk-8ku2), and the [National Center for Educational Statistics](https://nces.ed.gov/).

#### Methods
I used Python to analyze the datasets, which were both flat text files. I had to mutate the school and district names using regex, but was eventually able to merge them into a single dataframe. 

I visualized the data using Seaborn and Matplotlib. I used swarm plots, box plots, and bar charts to help convey the relationship that locale, location, and poverty rate had with herd immunity in Utah classrooms.

#### Outcomes
The data showed that a shockingly high number of Utah classrooms would be susceptible to an outbreak of measles. 
* Almost half of kindergarten classrooms in charter and private schools are *not* herd immune.
* Cities and suburbs tended to fare better than towns and rural areas. 
* Utah's poorest schools actually tended to be its most vaccinated, while its wealthiest schools were its least vaccinated.
