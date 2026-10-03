import math
import csv
import json
import quanscient as qs
from utils import Mesh, Variables, Consts, Empty, Fields, DerivedFields
from expressions import expr
from materials import mat
from regions import reg
from parameters import par

var = Variables()
mesh = Mesh()
fld = Fields()
df = DerivedFields()

# Load the mesh
mesh.mesh = qs.mesh()
mesh.mesh.setphysicalregions(*reg.get_region_data())
mesh.skin = reg.get_next_free()
mesh.mesh.selectskin(mesh.skin)
mesh.mesh.partition()
mesh.mesh.load("gmsh:simulation.msh", mesh.skin, 1, 1)

var.step_index = 0.0
var.start_time = 0.0
var.time_step = 1.0
var.end_time = 10.0 - 1e-08 * var.time_step
var.num_time_steps = int((var.end_time - var.start_time) / var.time_step) + 1

# Displacement field
fld.u = qs.field("h1xyz")
fld.u.setorder(reg.all, 1)

# Temperature field
fld.T = qs.field("h1")
fld.T.setorder(reg.all, 2)

df.sigma = qs.parameter(6, 1)

# Mechanical stress
df.sigma.addvalue(reg.thermal_expansion_target, -par.H() * qs.expression(6, 1, [par.alpha(), par.alpha(), par.alpha(), 0.0, 0.0, 0.0]) * (fld.T - 293.15))
df.sigma.addvalue(reg.all, par.H() * qs.strain(fld.u))

# Initial value interaction
fld.T.setvalue(reg.all, 293.15)

# Constraint interaction
fld.u.compx().setconstraint(reg.constraint_target, 0.0)
fld.u.compy().setconstraint(reg.constraint_target, 0.0)
fld.u.compz().setconstraint(reg.constraint_target, 0.0)

# Constraint interaction: Constraint 2
fld.u.compx().setconstraint(reg.constraint_2_target, 0.0)
fld.u.compz().setconstraint(reg.constraint_2_target, 0.0)

# Constraint interaction: Constraint 3
fld.u.compz().setconstraint(reg.constraint_3_target, 0.0)

form = qs.formulation()

# Heat solid
form += qs.integral(reg.all, qs.predefineddiffusion(qs.dof(fld.T), qs.tf(fld.T), par.k(), par.rho() * par.cp()))

# Convection interaction
form += qs.integral(reg.convection_target, -10.0 * (qs.dof(fld.T) - 293.15) * qs.tf(fld.T))

# Heat source interaction
form += qs.integral(reg.heat_source_target, ((60.0 * 0.35) / (qs.getpi() * math.pow(expr.radius, 2.0)) * qs.exp(-qs.pow(((qs.getx() - (expr.V * qs.t() - 0.05)) / expr.radius), 2.0))) * qs.tf(fld.T))

# Solid mechanics
form += qs.integral(reg.all, qs.predefinedelasticity(qs.dof(fld.u), qs.tf(fld.u), par.H()))
# Inertia terms
form += qs.integral(reg.all, -par.rho() * qs.dtdt(qs.dof(fld.u)) * qs.tf(fld.u))

# Thermal expansion interaction
form += qs.integral(reg.thermal_expansion_target, par.H() * qs.expression(6, 1, [par.alpha(), par.alpha(), par.alpha(), 0.0, 0.0, 0.0]) * (qs.dof(fld.T) - 293.15) * qs.strain(qs.tf(fld.u)))
form += qs.integral(reg.thermal_expansion_target, -293.15 * par.H() * qs.expression(6, 1, [par.alpha(), par.alpha(), par.alpha(), 0.0, 0.0, 0.0]) * qs.strain(qs.dt(qs.dof(fld.u))) * qs.tf(fld.T))

timestepper = qs.genalpha(form, qs.vec(form), qs.vec(form))
timestepper.settolerance(1e-05)
timestepper.setrelaxationfactor(-1)
qs.settime(var.start_time)

while qs.gettime() < var.end_time:
    timestepper.allnext(relrestol=1e-06, maxnumit=1000, timestep=var.time_step, maxnumnlit=1000)

    # Field output: Wafer surface temperature
    qs.setoutputfield("Wafer surface temperature", reg.wafer_top_surface, fld.T, 2, qs.gettime())

    # Field output: Wafer max in-plane principal stress
    qs.setoutputfield("Wafer max in-plane principal stress", reg.wafer_volume, (qs.comp(0, df.sigma) + qs.comp(1, df.sigma)) / 2.0 + qs.sqrt(qs.pow(((qs.comp(0, df.sigma) - qs.comp(1, df.sigma)) / 2.0), 2.0) + qs.pow(qs.comp(5, df.sigma), 2.0)), 2, qs.gettime())

    # Value output: Wafer peak in-plane principal stress
    var.discrete = qs.allmax(reg.wafer_volume, (qs.comp(0, df.sigma) + qs.comp(1, df.sigma)) / 2.0 + qs.sqrt(qs.pow(((qs.comp(0, df.sigma) - qs.comp(1, df.sigma)) / 2.0), 2.0) + qs.pow(qs.comp(5, df.sigma), 2.0)), 5)
    qs.setoutputvalue("Wafer peak in-plane principal stress", var.discrete, qs.gettime())

    # Field output: Copper von Mises stress
    qs.setoutputfield("Copper von Mises stress", reg.copper_volume, qs.vonmises(df.sigma), 2, qs.gettime())

    # Field output: Aluminium von Mises stress
    qs.setoutputfield("Aluminium von Mises stress", reg.aluminium_volume, qs.vonmises(df.sigma), 2, qs.gettime())

    # Value output: Copper peak von Mises stress
    var.discrete = qs.allmax(reg.copper_volume, qs.vonmises(df.sigma), 5)
    qs.setoutputvalue("Copper peak von Mises stress", var.discrete, qs.gettime())

    # Value output: Aluminium peak von Mises stress
    var.discrete = qs.allmax(reg.aluminium_volume, qs.vonmises(df.sigma), 5)
    qs.setoutputvalue("Aluminium peak von Mises stress", var.discrete, qs.gettime())

    var.step_index += 1

