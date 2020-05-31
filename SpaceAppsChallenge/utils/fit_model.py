import pandas as pd
import yaml
from NASAcovid19.Code import load_bing
import xarray as xr
import matplotlib.pyplot as plt
import  numpy as np
from scipy.optimize import curve_fit
import cartopy.crs as ccrs
# load input to select hotspots


def preprocess(days, cases):
    days = [pd.Timestamp(year=2020, month=int(d.split('/')[0]),
                         day=int(d.split('/')[1])) for d in days]
    # continuous_days = pd.date_range(days[0], days[-1], freq='1D')
    continuous_days = pd.date_range(pd.Timestamp(2020, 3, 1), days[-1], freq='1D')
    da = xr.DataArray(cases, dims=['time'], coords={'time': days})
    da = da.interp(time=continuous_days, method='slinear', kwargs={'fill_value': 'extrapolate'})
    return da

def fsigmoid(x, a, b, L):
    return L / (1.0 + np.exp(-a*(x-b)))

with open("cov_vars.yaml") as input_file:
    covid_vars = yaml.safe_load(input_file)
hotspots = load_bing.hotspot(**covid_vars)
hotspots.filter_region()
hotspots.group_subregion()

da_list = []
region_list = []
for i, region in enumerate(hotspots.subregions[1:]):
    try:
        da_temp = preprocess(hotspots.days[i], hotspots.case_ts[i])
        da_temp['lat'] = hotspots.lats[i]
        da_temp['lon'] = hotspots.lons[i]
    except ValueError:
        pass
    else:
        da_list.append(da_temp)
        region_list.append(region)
da = xr.concat(da_list, dim=pd.Index(region_list, name='Region'))
da = da.where(da > 20, drop=True)
inflection_point = []
growth_rate = []
plt.style.use('bmh')
for region in da.Region.values:

    da_ = da.sel(Region=region).dropna('time')
    da_ = da_.where(da_ > 20, drop=True)
    X = da_.time.values
    X = np.array([i for i, _ in enumerate(X)])
    y = da_.values


    try:
        a, b, L = curve_fit(fsigmoid, X, y, method='dogbox', bounds=([0, 0, 20], [0.5, 100, 40000]))[0]
    except:
        print(f'Region {region} not fitting')
        growth_rate.append(np.nan)
        inflection_point.append(np.nan)
    else:
        y_pred = np.array([fsigmoid(x, a, b, L) for x in X])
        inflection_point.append(b)
        growth_rate.append(a)


        plt.plot(y)
        plt.plot(y_pred)
        plt.xlabel('Days since 20th case')
        plt.ylabel('Cases')
        plt.title(region)
        plt.legend(['Observations', 'Model'])
        plt.savefig(f'../Plot/fit_{region}.png')
        plt.close()

da['growth_rate'] = ('Region'), growth_rate
da['inflection_point'] = ('Region'), inflection_point
da.to_netcdf('../Data/fit_parameters.nc')

fig, ax = plt.subplots(1, 1, subplot_kw={'projection': ccrs.PlateCarree()})
x = da.where(da.growth_rate.notnull(), drop=True).lon.values
y = da.where(da.growth_rate.notnull(), drop=True).lat.values
c = da.growth_rate.where(da.growth_rate.notnull(), drop=True).values
p = ax.scatter(x.tolist(), y.tolist(), c=c, cmap='nipy_spectral', vmax=0.3)
ax.coastlines()
fig.colorbar(p)
plt.show()
plt.close()

fig, ax = plt.subplots(1, 1, subplot_kw={'projection': ccrs.PlateCarree()})
x = da.where(da.inflection_point.notnull(), drop=True).lon.values
y = da.where(da.inflection_point.notnull(), drop=True).lat.values
c = da.inflection_point.where(da.inflection_point.notnull(), drop=True).values
p = ax.scatter(x.tolist(), y.tolist(), c=c, cmap='nipy_spectral', vmax=60)
ax.coastlines()
fig.colorbar(p)
plt.title('Inflection point \n (day of maximum cases)')
plt.show()
plt.close()


da.isel(time=0).drop('time').to_dataframe(name='Cases').to_csv('../Data/dataframe_fitparameters.csv')