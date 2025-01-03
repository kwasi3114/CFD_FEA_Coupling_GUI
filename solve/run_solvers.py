import subprocess
import os

def run_solvers(operation, cfd_case_dir="openfoam_case/fluid", fea_case_dir="openfoam_case/solid-fenics", run_in_parallel=False, num_processors=4):
    """
    Runs the CFD, FEA, or coupled solvers for a case.

    Parameters:
        operation (str): The type of operation to run ('cfd', 'fea', or 'coupled').
        cfd_case_dir (str): Path to the CFD solver case directory.
        fea_case_dir (str): Path to the FEA solver case directory.
        run_in_parallel (bool): Whether to run solvers in parallel (default: False).
        num_processors (int): Number of processors to use if running in parallel (default: 4).
    """
    try:
        if operation == 'cfd':
            # CFD solver command
            cfd_command = ["pimpleFoam"]
            if run_in_parallel:
                cfd_command = ["mpirun", "-np", str(num_processors), "pimpleFoam", "-parallel"]

            # Change directory and run CFD solver
            print(f"Running CFD solver in: {cfd_case_dir}")
            subprocess.run(["bash", "-c", f"cd {cfd_case_dir} && {' '.join(cfd_command)} | tee log.cfd"], check=True)
            print("CFD solver completed successfully.")

        elif operation == 'fea':
            # FEA solver using FEniCS
            fea_script = os.path.join(fea_case_dir, "fea_solver.py")
            if not os.path.isfile(fea_script):
                raise FileNotFoundError(f"FEniCS FEA solver script not found: {fea_script}")

            print(f"Running FEA solver using FEniCS in: {fea_case_dir}")
            subprocess.run(["python3", fea_script], check=True)
            print("FEA solver completed successfully.")

        elif operation == 'coupled':
            # Coupled solver using FEniCS
            coupled_script = os.path.join(fea_case_dir, "coupled_solver.py")
            if not os.path.isfile(coupled_script):
                raise FileNotFoundError(f"FEniCS coupled solver script not found: {coupled_script}")

            print(f"Running coupled solver using FEniCS in: {fea_case_dir}")
            subprocess.run(["python3", coupled_script], check=True)
            print("Coupled solver completed successfully.")

        else:
            raise ValueError(f"Invalid operation: {operation}. Valid options are 'cfd', 'fea', or 'coupled'.")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the solver(s): {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

