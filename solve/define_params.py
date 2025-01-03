import os
import subprocess


class DefineParams:
    def __init__(self, case_dir="openfoam_case"):
        self.case_dir = case_dir
        self.fluid_system_dir = os.path.join(self.case_dir, "fluid/system")
        self.solid_system_dir = os.path.join(self.case_dir, "solid/system")
        self.fluid_constant_dir = os.path.join(self.case_dir, "fluid/constant")
        self.solid_constant_dir = os.path.join(self.case_dir, "solid/constant")
        self.fluid_zero_dir = os.path.join(self.case_dir, "fluid/0")
        self.solid_zero_dir = os.path.join(self.case_dir, "solid/0")

        self.vel_dir = os.path.join(self.fluid_zero_dir, "U")
        self.pres_dir = os.path.join(self.fluid_zero_dir, "p")
        self.def_dir = os.path.join(self.solid_zero_dir, "D")
        self.dis_dir = os.path.join(self.solid_zero_dir, "pointD")
        self.for_dir = os.path.join(self.solid_zero_dir, "solidForce")
        #self.poly_mesh_dir = os.path.join(self.constant_dir, "polyMesh")
        #self.block_mesh_dict_path = os.path.join(self.system_dir, "blockMeshDict")

        #self.create_case_directories()
        
        
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
        with open(self.vel_dir, "w") as f:
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
        with open(self.pres_dir, "w") as f:
            f.write(p_file)

    def write_soliddef_params(self, dimensions, internalField, boundaryField):
        """Write a basic blockMeshDict file for a simple rectangular block."""
        D_file = f"""
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
    object      D;
}}

// Define dimensions of solid deformation
dimensions {dimensions};

// Define internal field
internalField {internalField};

// Define 
boundaryField
{
    {boundaryField}
};
"""
        with open(self.def_dir, "w") as f:
            f.write(D_file)

    def write_nodaldis_params(self, dimensions, internalField, boundaryField):
        """Write a basic blockMeshDict file for a simple rectangular block."""
        pointD_file = f"""
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
    class       pointVectorField;
    object      pointD;
}}

// Define dimensions of nodal displacement
dimensions {dimensions};

// Define internal field
internalField {internalField};

// Define 
boundaryField
{
    {boundaryField}
};
"""
        with open(self.dis_dir, "w") as f:
            f.write(pointD_file)

    def write_solidfor_params(self, dimensions, internalField, boundaryField):
        """Write a basic blockMeshDict file for a simple rectangular block."""
        solidForce_file = f"""
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
    location    0;
    object      solidForce;
}}

// Define dimensions of force
dimensions {dimensions};

// Define internal field
internalField {internalField};

// Define 
boundaryField
{
    {boundaryField}
};
"""
        with open(self.for_dir, "w") as f:
            f.write(solidForce_file)


if __name__ == "__main__":
    generator = DefineParams()
    generator.write_vel_params()
    generator.write_pres_params()
    generator.write_soliddef_params()
    generator.write_nodaldis_params()
    generator.write_solidfor_params()