from session import Connector
from .definitions import *
from .spectral_tools import freq_to_wavelength

class FDTD:
    ######################################################################
    #                                                                    #
    # __init__                                                           #
    #                                                                    #
    ######################################################################
    def __init__(self, filename = None, hide = False, serverArgs = {}, remoteArgs = {}, units = NANO):
        """
        Launches a new FDTD session.

        Parameters:
        -----------

        filename : str, optional
            A string specifying either a script file or a project file:
            - If a project file is provided, it will be loaded.
            - If a script file is provided, it will be executed.

        hide : bool, optional, default=False
            Determines whether the Ansys Lumerical GUI environment is visible on startup.
            - If True, the GUI is hidden, and all pop-up messages are disabled.

        serverArgs : dict, optional
            A dictionary of command-line arguments to pass to the software at launch.

            Example:
                serverArgs = {"use-solve": True, "platform": "offscreen", "threads": "2"}

        remoteArgs : dict, optional
            A dictionary containing connection details, required only when using the Python API remotely 
            on a Linux machine running the Interop Server.

            Example:
                remoteArgs = {"hostname": "192.168.215.129", "port": 8989}

        units : float, optional, default=nm
            A scaling factor for object dimensions and wavelengths.
        """
        connector = Connector
        self.api = connector.connect()        
        self.fdtd = self.api.FDTD(filename=filename, hide=hide, serverArgs=serverArgs, remoteArgs=remoteArgs)

        self.units = units
        self.monitors = []


    ######################################################################
    #                                                                    #
    # __getattr__                                                        #
    #                                                                    #
    ######################################################################
    def __getattr__(self, mathod):
        # Delegate method calls to `self.fdtd` for missing attributes.
        return getattr(self.fdtd, mathod)


    ######################################################################
    #                                                                    #
    # _update_units                                                      #
    #                                                                    #
    ######################################################################
    def _update_units(self, **kwargs):
        return {key: value * self.units if isinstance(value, (int, float)) else value for key, value in kwargs.items()}


    ######################################################################
    #                                                                    #
    # load_project                                                       #
    #                                                                    #
    ######################################################################
    def load_project(self, file):
        """
        Loads a simulation project file.

        Parameters:
        -----------
        file : str
            The name of the project file (without the extension). 
            The function will automatically append ".fsp" to the filename.

        Notes:
        ------
        - If the project file contains simulation results, they will also be loaded.
        """
        self.fdtd.load(file + ".fsp")


    ######################################################################
    #                                                                    #
    # run_simulation                                                     #
    #                                                                    #
    ######################################################################
    def run_simulation(self):
        """
        Runs the current simulation.

        Notes:
        ------
        - Upon completion, all simulation data is saved to the current simulation file.
        - The updated simulation file is then reloaded by the GUI.
        """
        self.fdtd.run()


    ######################################################################
    #                                                                    #
    # switch_to_layout                                                   #
    #                                                                    #
    ######################################################################
    def switch_to_layout(self):
        """
        Switches the solver into LAYOUT mode allowing to add and/or modify simulation objects.
        """
        self.fdtd.switchtolayout()


    ######################################################################
    #                                                                    #
    # disable_object                                                     #
    #                                                                    #
    ######################################################################
    def disable_object(self, object_name):
        """
        Disables a specified simulation object.
        """
        self.fdtd.setnamed(object_name, "enabled", 0)


    ######################################################################
    #                                                                    #
    # enable_object                                                      #
    #                                                                    #
    ######################################################################
    def enable_object(self, object_name):
        """
        Enables a specified simulation object.
        """
        self.fdtd.setnamed(object_name, "enabled", 1)


    ######################################################################
    #                                                                    #
    # get_data                                                           #
    #                                                                    #
    ######################################################################
    def get_data(self, monitor_name, data):
        return self.fdtd.getdata(monitor_name, data)


    ######################################################################
    #                                                                    #
    # get_wvls                                                           #
    #                                                                    #
    ######################################################################
    def get_wvls(self, monitor_name):
        """
        Computes wavlengths using the frequency data from a frequency domain power monitor.
        """
        return freq_to_wavelength(self.get_data(monitor_name, "f"))


    ######################################################################
    #                                                                    #
    # get_wavelengths                                                    #
    #                                                                    #
    ######################################################################
    def get_wavelengths(self, monitor_name):
        """
        Computes wavlengths using the frequency data from a frequency domain power monitor.
        This is an alias for get_wvls() function.
        """
        return self.get_wvls(monitor_name)


    ######################################################################
    #                                                                    #
    # get_transmitted_power                                              #
    #                                                                    #
    ######################################################################
    def get_transmitted_power(self, monitor_name):
        """
        Retrieves the transmitted power from a specified monitor.

        Parameters:
        -----------
        monitor_name : str
            The name of the power or profile monitor.

        Returns:
        --------
        float
            The transmitted power, normalized to the source power.
            - A value of 0.3 indicates that 30% of the injected optical power 
            passed through the monitor.
            - Negative values indicate power flowing in the opposite direction.
        """
        return self.fdtd.transmission(monitor_name)


    ######################################################################
    #                                                                    #
    # add_fdtd_region_with_span                                          #
    #                                                                    #
    ######################################################################
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


    ######################################################################
    #                                                                    #
    # add_fdtd_region_with_min_max                                       #
    #                                                                    #
    ######################################################################
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


    ######################################################################
    #                                                                    #
    # set_mesh_type                                                      #
    #                                                                    #
    ######################################################################
    def set_mesh_type(self, mesh_type = MESH_AUTO):
        """
        Set mesh type.

        Parameters:
        -----------
        mesh_type: str
            Type of the mesh to be used (e.g. "auto non-uniform" or "uniform").
        """
        self.fdtd.setnamed(FDTD_DOMAIN, MESH_TYPE, mesh_type)


    ######################################################################
    #                                                                    #
    # set_mesh_refinement                                                #
    #                                                                    #
    ######################################################################
    def set_mesh_refinement(self, mesh_technology = MESH_C1):
        """
        Set mesh refinement technology.

        Parameters:
        -----------
        mesh_technology: str
            The mesh refinement technology to be used (e.g. "conformal variant 0", "conformal variant 1", etc.).
        """
        self.fdtd.setnamed(FDTD_DOMAIN, MESH_REFINEMENT, mesh_technology)


    ######################################################################
    #                                                                    #
    # set_all_bc_symmetry                                                #
    #                                                                    #
    ######################################################################
    def set_all_bc_symmetry(self, symmetry: bool):
        """
        Set whether all boundary conditions use symmetry.

        Parameters:
        -----------
        symmetry: bool
            If True, all boundary conditions will use symmetry.
        """
        self.fdtd.setnamed(FDTD_DOMAIN, ALL_BC_SYMMETRY, symmetry)


    ######################################################################
    #                                                                    #
    # set_bc_x                                                           #
    #                                                                    #
    ######################################################################
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

    ######################################################################
    #                                                                    #
    # set_bc_y                                                           #
    #                                                                    #
    ######################################################################
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

    ######################################################################
    #                                                                    #
    # set_bc_z                                                           #
    #                                                                    #
    ######################################################################
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


    ######################################################################
    #                                                                    #
    # set_pml_profile                                                    #
    #                                                                    #
    ######################################################################
    def set_pml_profile(self, pml_profile = PML_STEEP_ANGLE):
        self.fdtd.setnamed(FDTD_DOMAIN, PML_PROFILE, pml_profile)


    ######################################################################
    #                                                                    #
    # set_number_of_pml_layers                                           #
    #                                                                    #
    ######################################################################
    def set_number_of_pml_layers(self, number_of_layers = 32):
        self.fdtd.setnamed(FDTD_DOMAIN, PML_LAYERS, number_of_layers)


    ######################################################################
    #                                                                    #
    # add_power_monitor                                                  #
    #                                                                    #
    ######################################################################
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


    ######################################################################
    #                                                                    #
    # set_global_monitor_option                                          #
    #                                                                    #
    ######################################################################
    def set_global_monitor_option(self, key, value):
        self.fdtd.setglobalmonitor(key, value)


    ######################################################################
    #                                                                    #
    # set_number_of_points_globally                                      #
    #                                                                    #
    ######################################################################
    def set_number_of_points_globally(self, number_of_points = 701):
        self.set_global_monitor_option(FDP_MONITOR_FREQ_POINTS, number_of_points)


    ######################################################################
    #                                                                    #
    # set_monitor_option                                                 #
    #                                                                    #
    ######################################################################
    def set_monitor_option(self, monitor_name, option, value):
        self.fdtd.setnamed(monitor_name, option, value)


    ######################################################################
    #                                                                    #
    # add_plane_wave_source                                              #
    #                                                                    #
    ######################################################################
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
  

    ######################################################################
    #                                                                    #
    # set_source_option                                                  #
    #                                                                    #
    ######################################################################
    def set_source_option(self, source_name, option, value):
        self.fdtd.setnamed(source_name, option, value)


    ######################################################################
    #                                                                    #
    # set_injection_axis                                                 #
    #                                                                    #
    ######################################################################
    def set_injection_axis(self, source_name, axis = "z"):
        self.set_source_option(source_name, LIGHT_SRC_INJECTION_AX, axis)


    ######################################################################
    #                                                                    #
    # set_injection_direction                                            #
    #                                                                    #
    ######################################################################
    def set_injection_direction(self, source_name, direction):
        self.set_source_option(source_name, LIGHT_SRC_INJECTION, direction)


    ######################################################################
    #                                                                    #
    # set_source_polarization                                            #
    #                                                                    #
    ######################################################################
    def set_source_polarization(self, source_name, polarization_angle):
        self.set_source_option(source_name, LIGHT_SRC_POLARIZATION, polarization_angle)