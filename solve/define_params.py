import os
import subprocess


class DefineParams:
    def __init__(self, case_dir="openfoam_case"):
        self.case_dir = case_dir
        self.system_dir = os.path.join(self.case_dir, "system")
        self.constant_dir = os.path.join(self.case_dir, "constant")
        self.zero_dir = os.path.join(self.case_dir, "0")
        #self.poly_mesh_dir = os.path.join(self.constant_dir, "polyMesh")
        #self.block_mesh_dict_path = os.path.join(self.system_dir, "blockMeshDict")

        self.create_case_directories()
        
        
        #openfoam_dir = "openfoam_case"
        #system_dir = os.path.join(openfoam_dir, "system")
        #os.makedirs(system_dir, exist_ok=True)

    def create_case_directories(self):
        """Create the necessary OpenFOAM case directory structure."""
        #os.makedirs(self.system_dir, exist_ok=True)
        #os.makedirs(self.poly_mesh_dir, exist_ok=True)
        os.makedirs(self.zero_dir, exist_ok=True)

    def write_vel_params(self, dimensions, internalField, boundaryField):
        """Write a basic blockMeshDict file for a simple rectangular block."""
        U_file = f"""
/*--------------------------------*- C++ -*----------------------------------*\\
| =========                 |                                                 |
| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\    /   O peration     | Version:  8                                     |
|   \\  /    A nd           | Web:      www.OpenFOAM.org                      |
|    \\/     M anipulation  |                                                 |
\\*--------------------------------------------------------------------------*/

FoamFile
{{
    version     2.0;
    format      ascii;
    class       volVectorField;
    object      U;
}}

// Define dimensions of velocity
dimensions {dimensions};

// Define internal field
internalField {internalField};

// Define 
boundaryField
{
    {boundaryField}
};
"""
        with open(self.zero_dir, "w") as f:
            f.write(U_file)

    def write_pres_params(self, dimensions, internalField, boundaryField):
        """Write a basic blockMeshDict file for a simple rectangular block."""
        p_file = f"""
/*--------------------------------*- C++ -*----------------------------------*\\
| =========                 |                                                 |
| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\    /   O peration     | Version:  8                                     |
|   \\  /    A nd           | Web:      www.OpenFOAM.org                      |
|    \\/     M anipulation  |                                                 |
\\*--------------------------------------------------------------------------*/

FoamFile
{{
    version     2.0;
    format      ascii;
    class       volScalarField;
    object      p;
}}

// Define dimensions of pressure
dimensions {dimensions};

// Define internal field
internalField {internalField};

// Define 
boundaryField
{
    {boundaryField}
};
"""
        with open(self.zero_dir, "w") as f:
            f.write(p_file)


if __name__ == "__main__":
    generator = DefineParams()
    generator.write_vel_params()
    generator.write_pres_params()