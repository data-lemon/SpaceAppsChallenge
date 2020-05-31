#main of program to read and analyse covid19 hotspots in the UK
import load_bing as load_bing
import yaml 
import scatter as scat
import timeseries as ts

if __name__ == "__main__":
    ##uk coordinates
    coords = [-11,4, 49, 62]
    # load input to select hotspots
    with open("cov_vars.yaml") as input_file:
        covid_vars = yaml.safe_load(input_file)
     
    # load hotspots of COVID-19
    hotspots = load_bing.hotspot(**covid_vars)
    
    #filter for selected region
    hotspots.filter_region()
    hotspots.group_subregion()
    #df = hotspots.df
    
    
    #plot
    scat.plot_hotspots(hotspots.total_cases, hotspots.lons, hotspots.lats, coords)
   
    ts.ts_cases(hotspots.case_ts[1], hotspots.days[1], hotspots.subregions[1])