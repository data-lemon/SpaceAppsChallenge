#read covid 19 bing files

import pandas as pd

class hotspot:
    """
    Create hotspot constructor
    """
    
    def __init__(self, datfile, region):
        """
        Initialise hotspot class
        """
        print("**************INPUT************")
        print("I am suing filepath",datfile)
        print("Filtering region:",region)
        print("**************INPUT************")
        
        #assign input
        self.datfile = datfile
        self.region = region[0] # yaml loads as list
        #load pandas frame of COVID-19 cases raw data
        self.df = pd.read_csv(datfile[0]) 
    
    def filter_region(self):
        """
        Filter data frame for region
        """
        self.df = self.df.loc[self.df["Country_Region"]==self.region]
        self.df["Updated"] = self.df["Updated"].map(lambda x:str(x)[:-5])
    def group_subregion(self):
        
        #replace Nan values with tag aggergated which indicates it is not specific to admin reg2
        self.df["AdminRegion2"] = self.df["AdminRegion2"].fillna("aggregated")
        #list unique values of subregs
        self.subregions = self.df.AdminRegion2.unique() #first element is aggregated
        #group subregions by adminregion2
        df_subregions = self.df.groupby("AdminRegion2")
        
        #list of lats
        
        self.lats = []
        self.lons = []
        self.total_cases = []
        self.active_cases = []
        self.case_ts = []
        self.days = []
        for subs in self.subregions[1:]:
            
            site = df_subregions.get_group(subs)
            self.lats.append(site["Latitude"].unique()[0])
            self.lons.append(site["Longitude"].unique()[0])
            self.total_cases.append(site["Confirmed"].values[-1])
            self.active_cases.append(site["Confirmed"].values[-1]-site["Recovered"].values[-1])
            self.case_ts.append(site["Confirmed"].values)
            self.days.append(site["Updated"].values)
        
        
    
