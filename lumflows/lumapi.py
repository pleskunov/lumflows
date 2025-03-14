from lumapi_connector import connector # type: ignore
from .definitions import *
from .spectral_tools import freq_to_wavelength

class API():
    def __init__(self, fdtd = None, units = NANO):
        if fdtd is None:
            api_connector = connector.LumAPI()
            self.api = api_connector.connect()        
            self.fdtd = self.api.FDTD()
        else:
            self.api = None
            self.fdtd = fdtd
            self.units = units
            self.monitors = []


    def _update_units(self, **kwargs):
        return {key: value * self.units if isinstance(value, (int, float)) else value for key, value in kwargs.items()}


    def load_project(self, file):
        print("Loading the project...")
        self.fdtd.load(file + ".fsp")


    def run(self):
        self.fdtd.run()


    def switch_to_layout(self):
        self.fdtd.switchtolayout()


    def disable(self, name):
        self.fdtd.setnamed(name, "enabled", 0)


    def enable(self, name):
        self.fdtd.setnamed(name, "enabled", 1)


    def get_wavelengths(self, monitor_name):
        frequency = self.fdtd.getdata(monitor_name, "f")
        return freq_to_wavelength(frequency)


    def get_transmitted_power(self, monitor_name):
        return self.fdtd.transmission(monitor_name)


    def add_fdtd_region_with_span(self, dimension, **kwargs):
        """
        Add an FDTD region defining its geometry using the center-span coordinates.
        
        Parameters:
        ----------
        dimension : str
            Defines the simulation dimension (e.g., "2D" or "3D").

        x, y, z: float
            Center x, y and z coordinates.
        
        x_span, y_span, z_span: float
            Span in x, y and z coordinates.
        """
        self.fdtd.addfdtd(dimension=dimension, **self._update_units(**kwargs))


    def add_fdtd_region_with_min_max(self, dimension, **kwargs):
        """
        Add an FDTD region defining its geometry using the min-max coordinates.
        
        Parameters:
        ----------
        dimension : str
            Defines the simulation dimension (e.g., "2D" or "3D").

        x_min, y_min, z_min: float
            Minimum x, y and z coordinates.
        
        x_max, y_max, z_max: float
            Maximum in x, y and z coordinates.
        """
        self.fdtd.addfdtd(dimension=dimension, **self._update_units(**kwargs))


    def set_mesh_type(self, mesh_type = MESH_AUTO):
        """
        Set mesh type.

        Parameters:
        -----------
        mesh_type: str
            Type of the mesh to be used (e.g. "auto non-uniform" or "uniform").
        """
        self.fdtd.setnamed(FDTD_DOMAIN, MESH_TYPE, mesh_type)


    def set_mesh_refinement(self, mesh_technology = MESH_C1):
        """
        Set mesh refinement technology.

        Parameters:
        -----------
        mesh_technology: str
            The mesh refinement technology to be used (e.g. "conformal variant 0", "conformal variant 1", etc.).
        """
        self.fdtd.setnamed(FDTD_DOMAIN, MESH_REFINEMENT, mesh_technology)


    def set_all_bc_symmetry(self, symmetry: bool):
        """
        Set whether all boundary conditions use symmetry.

        Parameters:
        -----------
        symmetry: bool
            If True, all boundary conditions will use symmetry.
        """
        self.fdtd.setnamed(FDTD_DOMAIN, ALL_BC_SYMMETRY, symmetry)


    def set_bc_x(self, bc_min = BC_PML, bc_max = BC_PML):
        """
        Set boundary conditions for the X-axis.

        Parameters:
        -----------
        bc_min: str
            Boundary condition for X_min (e.g., "periodic", "PML").
        bc_max: str
            Boundary condition for X_max (e.g., "periodic", "PML").
        """
        self.fdtd.setnamed(FDTD_DOMAIN, BC_X_MIN, bc_min)
        self.fdtd.setnamed(FDTD_DOMAIN, BC_X_MAX, bc_max)


    def set_bc_y(self, bc_min = BC_PML, bc_max = BC_PML):
        """
        Set boundary conditions for the Y-axis.

        Parameters:
        -----------
        bc_min: str
            Boundary condition for Y_min (e.g., "periodic", "PML").
        bc_max: str
            Boundary condition for Y_max (e.g., "periodic", "PML").
        """
        self.fdtd.setnamed(FDTD_DOMAIN, BC_Y_MIN, bc_min)
        self.fdtd.setnamed(FDTD_DOMAIN, BC_Y_MAX, bc_max)


    def set_bc_z(self, bc_min = BC_PML, bc_max = BC_PML):
        """
        Set boundary conditions for the Z-axis.

        Parameters:
        -----------
        bc_min: str
            Boundary condition for Z_min (e.g., "PML", "periodic").
        bc_max: str
            Boundary condition for Z_max (e.g., "PML", "periodic").
        """
        self.fdtd.setnamed(FDTD_DOMAIN, BC_Z_MIN, bc_min)
        self.fdtd.setnamed(FDTD_DOMAIN, BC_Z_MAX, bc_max)

    
    def set_pml_profile(self, pml_profile = PML_STEEP_ANGLE):
        self.fdtd.setnamed(FDTD_DOMAIN, PML_PROFILE, pml_profile)


    def set_number_of_pml_layers(self, number_of_layers = 32):
        self.fdtd.setnamed(FDTD_DOMAIN, PML_LAYERS, number_of_layers)


    def add_power_monitor(self, name, monitor_type, **kwargs):
        """
        Add a Frequency Domain Power Monitor defining its geometry using the center-span/or min-max coordinates.
        
        Parameters:
        ----------
        name: str
            Name of the monitor.
        
        monitor_type: str
            Type of the monitor.

        x, y, z: float (optional)
            Center x, y and z coordinates.
        
        x_span, y_span, z_span: float (optional)
            Span in x, y and z coordinates.

        x_min, y_min, z_min: float (optional)
            Minimum x, y and z coordinates.
        
        x_max, y_max, z_max: float (optional)
            Maximum in x, y and z coordinates.
        """
        print("Adding monitor to the simulation...")
        self.monitors.append(self.fdtd.addpower(name=name, monitor_type=monitor_type, **self._update_units(**kwargs)))

    
    def set_global_monitor_option(self, key, value):
        self.fdtd.setglobalmonitor(key, value)


    def set_number_of_points_globally(self, number_of_points = 701):
        self.set_global_monitor_option(FDP_MONITOR_FREQ_POINTS, number_of_points)

    
    def set_monitor_option(self, monitor_name, option, value):
        self.fdtd.setnamed(monitor_name, option, value)

    
    def add_plane_wave_source(self, name, wavelength_start = 0.21 * 1e-6, wavelength_stop = 2.5 * 1e-6, **kwargs):
        """
        Add a Plane Wave Light Source defining its geometry using the center-span/or min-max coordinates.
        
        Parameters:
        ----------
        name: str
            Name of the monitor.
        
        wavelength_start: float
            Start wavelength.

        wavelength_stop: float
            Stop wavelength.

        x, y, z: float (optional)
            Center x, y and z coordinates.
        
        x_span, y_span, z_span: float (optional)
            Span in x, y and z coordinates.

        x_min, y_min, z_min: float (optional)
            Minimum x, y and z coordinates.
        
        x_max, y_max, z_max: float (optional)
            Maximum in x, y and z coordinates.
        """
        self.fdtd.addplane(name=name, wavelength_start=wavelength_start, wavelength_stop=wavelength_stop, **self._update_units(**kwargs))
  
    
    def set_source_option(self, source_name, option, value):
        self.fdtd.setnamed(source_name, option, value)


    def set_injection_axis(self, source_name, axis = "z"):
        self.set_source_option(source_name, LIGHT_SRC_INJECTION_AX, axis)


    def set_injection_direction(self, source_name, direction):
        self.set_source_option(source_name, LIGHT_SRC_INJECTION, direction)


    def set_source_polarization(self, source_name, polarization_angle):
        self.set_source_option(source_name, LIGHT_SRC_POLARIZATION, polarization_angle)