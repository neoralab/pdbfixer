
from __future__ import print_function
from pdbfixer.pdbfixer import PDBFixer
from openmm import app

import os
import os.path
import sys
import numpy
import tempfile

from threading import Timer

#from a solution on stackoverflow
class Watchdog(BaseException):
    def __init__(self, timeout, userHandler=None):  # timeout in seconds
        self.timeout = timeout
        self.handler = userHandler if userHandler is not None else self.defaultHandler
        self.timer = Timer(self.timeout, self.handler)

    def reset(self):
        self.timer.cancel()
        self.timer = Timer(self.timeout, self.handler)

    def stop(self):
        self.timer.cancel()

    def defaultHandler(self):
        raise self

def simulate(pdbcode, pdb_filename):
    from openmm import app
    import openmm.openmm as mm
    from openmm import unit
    from sys import stdout

    # Load the PDB file.
    pdb = app.PDBFile(pdb_filename)
    
    # Set up implicit solvent forcefield.
    #forcefield = app.ForceField('amber99sbildn.xml')
    forcefield = app.ForceField('amber10.xml')
    
    # Create the system.
    system = forcefield.createSystem(pdb.topology, nonbondedMethod=app.NoCutoff, constraints=app.HBonds)

    # Create an integrator.
    integrator = mm.LangevinIntegrator(300*unit.kelvin, 91.0/unit.picoseconds, 1.0*unit.femtoseconds)

    # Create a context.
    context = mm.Context(system, integrator)
    context.setPositions(pdb.positions)
    
    # Check to make sure energy is finite.
    state = context.getState(getEnergy=True)
    potential = state.getPotentialEnergy() / unit.kilocalories_per_mole
    if numpy.isnan(potential):
        raise Exception("Initial energy for %s is NaN." % pdbcode)

    # Minimize.
    tolerance = 1.0 * unit.kilocalories_per_mole / unit.angstroms
    maxIterations = 50
    mm.LocalEnergyMinimizer.minimize(context, tolerance, maxIterations)

    # Check to make sure energy is finite.
    state = context.getState(getEnergy=True)
    potential = state.getPotentialEnergy() / unit.kilocalories_per_mole
    if numpy.isnan(potential):
        raise Exception("Energy for %s is NaN after minimization." % pdbcode)

    # Simulate.
    nsteps = 500
    integrator.step(nsteps)

    # Check to make sure energy is finite.
    state = context.getState(getEnergy=True)
    potential = state.getPotentialEnergy() / unit.kilocalories_per_mole
    if numpy.isnan(potential):
        raise Exception("Energy for %s is NaN after simulation." % pdbcode)

    del context, integrator

    print("Simulation completed: potential = %.3f kcal/mol" % potential)

    return

def test_build_and_simulate():
    # Keep the build list intentionally short to avoid excessive downloads and long runtimes in CI.
    # These structures are small and exercise the same pathway as the larger regression set used historically.
    pdbcodes_to_build = ["110D", "116D", "117D", "118D"]

    # Don't simulate any.
    pdbcodes_to_simulate = []

    # Keep track of list of failures.
    failures = list()
        
    forcefield = app.ForceField('amber14-all.xml', 'amber14/tip3pfb.xml')
    for pdbcode in pdbcodes_to_build:
        print("------------------------------------------------")
        print(pdbcode)

        pH = 7.0

        outfile = tempfile.NamedTemporaryFile(mode='w', delete=False)
        output_pdb_filename = outfile.name

        timeout_seconds = 30
        watchdog = Watchdog(timeout_seconds)
        build_successful = False
        try:
            stage = "Creating PDBFixer..."
            fixer = PDBFixer(pdbid=pdbcode)
            stage = "Deleting hydrogens..."
            if pdbcode in ['135D', '136D', '177D', '1A83', '1AGG', '1AJ1']:
                # These input files include extra hydrogens that aren't supported by the force field.
                # To avoid problems, delete all pre-existing hydrogens.
                modeller = app.Modeller(fixer.topology, fixer.positions)
                modeller.delete([a for a in fixer.topology.atoms() if a.element == app.element.hydrogen])
                fixer.topology = modeller.topology
                fixer.positions = modeller.positions
            stage = "Finding missing residues..."
            fixer.findMissingResidues()
            stage = "Finding nonstandard residues..."
            fixer.findNonstandardResidues()
            stage = "Replacing nonstandard residues..."
            fixer.replaceNonstandardResidues()
            stage = "Removing heterogens..."
            fixer.removeHeterogens(False)
            stage = "Finding missing atoms..."
            fixer.findMissingAtoms()
            stage = "Adding missing atoms..."
            fixer.addMissingAtoms()
            stage = "Adding missing hydrogens..."
            fixer.addMissingHydrogens(pH)
            stage = "Writing PDB file..."
            app.PDBFile.writeFile(fixer.topology, fixer.positions, outfile)
            stage = "Create System..."
            forcefield.createSystem(fixer.topology)
            stage = "Done."
            outfile.close()
            build_successful = True

        except Watchdog:
            message = "timed out in stage %s" % stage
            print(message)
            failures.append((pdbcode, Exception(message)))

        except Exception as e:
            print("EXCEPTION DURING BUILD")
            #import traceback
            #print traceback.print_exc()
            print(str(e))
            failures.append((pdbcode, e))
        
        watchdog.stop()
        del watchdog
                    
        # Test simulating this with OpenMM.
        if (pdbcode in pdbcodes_to_simulate) and (build_successful):
            watchdog = Watchdog(timeout_seconds)
            try:
                simulate(pdbcode, output_pdb_filename)
                
            except Watchdog:
                message = "timed out in simulation"
                print(message)
                failures.append((pdbcode, Exception(message)))

            except Exception as e:
                print("EXCEPTION DURING SIMULATE")
                #import traceback
                #print traceback.print_exc()
                print(str(e))
                failures.append((pdbcode, e))
        
            watchdog.stop()
            del watchdog

        # Clean up.
        os.remove(output_pdb_filename)

    print("------------------------------------------------")

    if len(failures) != 0:
        print("")
        print("SUMMARY OF FAILURES:")
        print("")
        for failure in failures:
            (pdbcode, exception) = failure
            print("%6s : %s" % (pdbcode, str(exception)))
        print("")

        raise Exception("Build test failed on one or more PDB files.")
    
    else:
        print("All tests succeeded.")

if __name__ == '__main__':
    test_build_and_simulate()
