#scatter plot covid-19 cases
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import matplotlib.colors as colors

class MidpointNormalize(colors.Normalize):
	"""
	Normalise the colorbar so that diverging bars work there way either side from a prescribed midpoint value)

	e.g. im=ax1.imshow(array, norm=MidpointNormalize(midpoint=0.,vmin=-100, vmax=100))
	"""
	def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
		self.midpoint = midpoint
		colors.Normalize.__init__(self, vmin, vmax, clip)

	def __call__(self, value, clip=None):
		# I'm ignoring masked values and all kinds of edge cases to make a
		# simple example...
		x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
		return np.ma.masked_array(np.interp(value, x, y), np.isnan(value))
    
def plot_hotspots(field, lons, lats, coords):
    """
    Plot scatter map of cases
    input:
        lons: list
        lats: list
        field: list
        coords:array
    """
    field = np.asarray(field)
    plt.figure(figsize=(9,8), dpi=300)   
    crs=ccrs.PlateCarree()
    plt.axes(projection=ccrs.PlateCarree())
    # Earth's grid
    ax = plt.subplot(projection=crs)
    ax.coastlines('10m')
    ax.set_extent(coords)  
    #scatter plot
    plt.scatter(lons, lats, marker='o', c=field, s=30, cmap="magma_r", edgecolor="k", linewidth=0.5, transform=crs)
    levels=np.arange(0,17000, 1000)
    cb = plt.colorbar(boundaries=levels)
    cb.ax.tick_params(labelsize=14)
    cb.set_label("Total Cases"+" per admin county", fontsize = 14)
    plt.show()