from irradiance_code import flux_density
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib import animation

# Display animation in Jupyter
from IPython.display import HTML 
from JSAnimation.IPython_display import display_animation
plt.style.use('seaborn-white')  # bmh is also nice
plt.rcParams['animation.embed_limit'] = 2**32  # Allows for larger animation embeddings

# Workaround for basemap to avoid: "KeyError: ['PROJ_LIB']" when using mpl_toolkits outside of a conda environment
import os
os.environ['PROJ_LIB'] = '/Users/jonahgolden/anaconda3/pkgs/proj4-5.2.0-h0a44026_1/share/proj/'
from mpl_toolkits.basemap import Basemap


class FluxAnim():
    '''
    Class for making flux density animations.
    Any field can be set, and make_animation will return an animation object accordingly.
    '''
    
    def __init__(self):
        '''inputs: None. Set fields before running make_animation().
        output: FluxAnim object.
        '''
        self.start_date=datetime.now()
        self.geo_res=1
        self.hours_per_frame=2
        # Set lat and lon ranges of plot
        self.min_lon, self.max_lon, self.lon_step = -180, 180, 60
        self.min_lat, self.max_lat, self.lat_step = -90, 90, 30
        # Vectorize Function
        self.flux_function = np.vectorize(flux_density)
        # Make grid with coordinates
        self.longitudes = [lon for lon in range(self.min_lon, self.max_lon, self.geo_res)]
        self.latitudes = [lat for lat in range(self.min_lat, self.max_lat, self.geo_res)]
        self.lons, self.lats = np.meshgrid(self.longitudes, self.latitudes)
        # Map lines to draw
        self.draw_coast, self.draw_countries, self.draw_states = True, False, False
        
    def _draw_img(self, date):
        flux = self.flux_function(date, self.lats, self.lons)
        img = plt.imshow(flux, extent=[self.min_lon, self.max_lon, self.min_lat, self.max_lat], origin='lower', cmap='viridis') #, aspect='auto')
        plt.clim(0, 1000)
        plt.suptitle(date.strftime("%b %d, %Y, %H:%M:%S UTC"), fontsize=24, weight='bold', x = 0.45, y=0.94)
        return(img)
    
    def _anim_init(self):
        # Map
        m = Basemap(projection='cyl', llcrnrlon=self.min_lon, llcrnrlat=self.min_lat, urcrnrlon=self.max_lon, urcrnrlat=self.max_lat)
        if self.draw_coast: m.drawcoastlines()
        if self.draw_countries: m.drawcountries()
        if self.draw_states: m.drawstates()
        m.drawparallels(np.arange(self.min_lat, self.max_lat+1, self.lat_step), labels=[1,0,0,0], fontsize=14)
        m.drawmeridians(np.arange(self.min_lon, self.max_lon+1, self.lon_step), labels=[0,0,0,1], fontsize=14)
        img = self._draw_img(self.start_date)
        # Colorbar
        cbar = plt.colorbar(img)
        cbar.ax.tick_params(labelsize=14)
        cbar.ax.set_title('Clear Sky\nSolar Flux Density\n' + r'$\bf{\left(w/m^2\right)}$', fontsize=16, y=1.01)
        
    def _animate(self, hour):
        date = self.start_date + timedelta(hours=hour*self.hours_per_frame)
        img = self._draw_img(date)
        #plt.savefig("../images/anim1/image" + str(hour) + ".png")
        return img
    
    def _make_grids(self):
        # Make grid with coordinates
        self.longitudes = [lon for lon in range(self.min_lon, self.max_lon, self.geo_res)]
        self.latitudes = [lat for lat in range(self.min_lat, self.max_lat, self.geo_res)]
        self.lons, self.lats = np.meshgrid(self.longitudes, self.latitudes)

    
    def make_animation(self, frames=24, fps=2):
        self._make_grids()
        interval = (1/fps)*1e+3
        fig = plt.figure(figsize=(16, 8))
        anim = animation.FuncAnimation(fig, self._animate, init_func=self._anim_init,
                                       frames=frames, interval=interval, blit=False)
        return anim
    