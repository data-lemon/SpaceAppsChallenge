#plot timeseries of cases
import matplotlib.pyplot as plt

def ts_cases(dates, case_ts, subregions):
    """
    input:
        dates: list of arrays
        case_ts: list of total cases arrays per subregion
        subregioNS: list of subregions
    """
    nplots = len(subregions)
    plt.figure()
    for i in range(nplots):
        plt.plot(dates[i], case_ts[i], label=subregions[i])
        plt.xticks(dates[::4])
        
    plt.ylabel("Total cases")
    plt.xlabel("Days")
    plt.legend("loc"=best)
    plt.show()

