FDTD_DOMAIN = "FDTD" 
FDTD_DOMAIN_2D = 1
FDTD_DOMAIN_3D = 2

MESH_TYPE = "mesh type"
MESH_AUTO = "auto non-uniform"

MESH_REFINEMENT = "mesh refinement" 
MESH_C0 = "conformal variant 0"
MESH_C1 = "conformal variant 1"

ALL_BC_SYMMETRY = "allow symmetry on all boundaries"

BC_X_MIN = "x min bc"
BC_X_MAX = "x max bc"
BC_Y_MIN = "y min bc"
BC_Y_MAX = "y max bc"
BC_Z_MIN = "z min bc"
BC_Z_MAX = "z max bc"

BC_PERIODIC = "Periodic"
BC_PML = "PML"

PML_PROFILE = "pml profile"
PML_LAYERS = "pml layers"

PML_STANDARD = 1
PML_STABILZED = 2
PML_STEEP_ANGLE = 3
PML_CUSTOM = 4


FDP_MONITOR_POINT = 1
FDP_MONITOR_LINEAR_X = 2
FDP_MONITOR_LINEAR_Y = 3
FDP_MONITOR_LINEAR_Z = 4
FDP_MONITOR_2D_X_NORMAL = 5
FDP_MONITOR_2D_Y_NORMAL = 6
FDP_MONITOR_2D_Z_NORMAL = 7
FDP_MONITOR_3D = 8

FDP_MONITOR_FREQ_POINTS = "frequency points"

FDP_MONITOR_OPTS = ["standard fourier transform", 
                    "partial spectral average", 
                    "total spectral average", 
                    "output Hx", "output Hy", "output Hz", 
                    "output Ex", "output Ey", "output Ez", 
                    "output Px", "output Py", "output Pz", 
                    "output power"]

LIGHT_SRC_INJECTION_AX = "injection axis"
LIGHT_SRC_INJECTION = "direction"