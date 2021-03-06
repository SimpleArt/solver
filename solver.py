from Bracketing_Methods.bisection              import bisection
from Bracketing_Methods.secant                 import secant
from Bracketing_Methods.dekker                 import dekker
from Bracketing_Methods.brent                  import brent
from Bracketing_Methods.newton_quadratic       import newton_quadratic
from Bracketing_Methods.chandrupatla           import chandrupatla
from Bracketing_Methods.chandrupatla_quadratic import chandrupatla_quadratic
from Bracketing_Methods.chandrupatla_mixed     import chandrupatla_mixed

from math import sqrt
import sys
realmin = sys.float_info.min  # Smallest positive float
realmax = sys.float_info.max  # Largest positive float
sqrtmin = sqrt(realmin)       # Smallest positive root
sqrtmax = sqrt(realmax)       # Largest positive root
inf = float('inf')         # Infinity in floats
nan = float('nan')         # Not a number
print_iterations  = False  # Printing intermediate iterations
print_result      = False  # Printing the final iteration
return_iterations = False  # Return the number of iterations with the result

def is_nan(x):
    return x != x

def is_infinite(x):
    return abs(x) == float('inf')

def sign(x):
    """Returns the sign of x.
    """
    if x > 0: return +1
    if x < 0: return -1
    else: return 0

def mean(x, y, flag):
    """Alternates between using
    - arithmetic means and
    - geometric means
    to guarantee fast travel
    through all possible floats."""
    
    # Check 0 if it's in the interval
    if sign(x)*sign(y) < 0:
        return 0.0
    
    # Sort x, y by absolute value
    if abs(x) > abs(y):
        x, y = y, x
    
    # Try arithmetic mean if flag or the
    # relative error of x and y are small
    # enough to avoid square roots.
    if flag or 0.25 < x/y:
        if x/y < 0.125: return 0.75*x+0.25*y
        if abs(y) < realmax/2: return 0.5*(x+y)
        # Overflow
        return 0.5*x+0.5*y
    
    # If geometric mean should be tried but
    # if there is a sign issue, then return
    # 0. Will eventally force both points to
    # have the same sign due to tolerance
    # pulling it onto one side.
    if abs(x) > sqrtmin and abs(y) < sqrtmax:
        return sign(y)*sqrt(x*y)
    # Under-/Over- Flow
    return sign(y)*sqrt(abs(x))*sqrt(abs(y))

bracketing_method_dict = {
    'bisection'              : bisection,
    'binary search'          : bisection,
    'regula falsi'           : secant,
    'false position'         : secant,
    'secant'                 : secant,
    'muller'                 : newton_quadratic,
    'quadratic'              : newton_quadratic,
    'dekker'                 : dekker,
    'brent'                  : brent,
    'iq'                     : brent,
    'inverse quadratic'      : brent,
    'chandrupatla'           : chandrupatla,
    'chandrupatla quadratic' : chandrupatla_quadratic,
    'quadratic safe'         : chandrupatla_quadratic,
    'chandrupatla mixed'     : chandrupatla_mixed       # default
}

def help(input = None):
    if input == 'root_in':
        print("""Usage:
solver.root_in(f, x1, x2, {method, iterations, abs_err_1, abs_err_2, rel_err, f1, f2})

@params
    f: the searched function for the root.
    x1, x2: initial bracket.
    method: string name of the method used for solver.root_in.
    iterations: limit on the number of iterations before binary search is used instead of the chosen method.
    abs_err_1: desired absolute error of |x1-x2|.
    rel_err_1: desired relative error of |x1-x2|.
    abs_err_2: larger initial absolute error searched for.
    rel_err_2: larger initial relative error searched for.
    f1, f2: optional initial values of f(x1) and f(x2).

@defaults
    method: 'chandrupatla'
    iterations: 200
    abs_err_1: 1e-14
    abs_err_2: 1e+16 * abs_err_1
    rel_err: 1e-14

Attempts to solve f(x) = 0 between x1 and x2, given f(x1) and f(x2) have different signs, where convergence to a root can be guaranteed using binary search, a.k.a. bisection.

To guarantee convergence, binary search, is used after 4 consecutive iterations without the bracketing interval halving.

To avoid unnecessary binary search when the root is actually being approached rapidly, the distance from the last computed point is tripled after 3 consecutive iterations without the bracketing interval halving.

Use solver.help('methods') for more specific information, or check the github wiki at https://github.com/SimpleArt/solver/wiki.
""")
    elif input == 'optimize':
        print("""Usage:
solver.optimize(g, x1, x2, {method, iterations, abs_err_1, abs_err_2, rel_err, f})

@params
    g: the searched function for the local extrema.
    x1, x2: initial bracket.
    f: the searched function for the root. Represents the derivative of g for solver.optimize.
    method: string name of the method used for solver.root_in.
    iterations: limit on the number of iterations before binary search is used instead of the chosen method.
    abs_err_1: desired absolute error of |x1-x2|.
    rel_err_1: desired relative error of |x1-x2|.
    abs_err_2: larger initial absolute error searched for.
    rel_err_2: larger initial relative error searched for.

@defaults
    f: g(x+dx) - g(x-dx), where dx = abs_err_1 + rel_err*abs(x)
    method: 'chandrupatla'
    iterations: 200
    abs_err_1: 1e-8
    err_1: 1e+10 * abs_err_1

Attempts to find extreme values of g(x) between x1 and x2, given g(x) is increasing at one point and decreasing at the other. Uses solver.root_in to find the root of f(x), the derivative of g(x).

Use solver.help('methods') for more specific information, or check the github wiki at https://github.com/SimpleArt/solver/wiki.
""")
    elif input == 'methods':
        print("""bracketing_method_dict = {
    'bisection'              : bisection,
    'binary search'          : bisection,
    'regula falsi'           : secant,
    'false position'         : secant,
    'secant'                 : secant,
    'muller'                 : newton_quadratic,
    'quadratic'              : newton_quadratic,
    'dekker'                 : dekker,
    'brent'                  : brent,
    'iq'                     : brent,
    'inverse quadratic'      : brent,
    'chandrupatla'           : chandrupatla,
    'chandrupatla quadratic' : chandrupatla_quadratic,
    'chandrupatla mixed'     : chandrupatla_mixed       # default
}

bisection   : returns the midpoint of the interval.
secant      : returns the secant estimate of the root using x1 and x2.
quadratic   : returns the quadratic interpolation estimate of the root using x1, x2, and x3.
dekker      : returns the secant estimate of the root, using x2 and x3.
brent       : returns the inverse quadratic interpolation estimate of the root when possible, using x1, x2, and x3.
chandrupatla: returns the inverse quadratic interpolation estimate of the root when the interpolation is monotone, using x1, x2, and x3.

Usage:
bracketing_method(x1, f1, x2, f2, x3, f3, x4, f4, t)

@params:
    x1, f1: bracketing point for x2.
    x2, f2: last estimate of the root.
    x3, f3: last removed point from the interval.
    x4, f4: second last removed point from the interval, initially None.
    t: last computed t, used to check if bisection was last used.

@returns:
    t: the combination of x1 and x2 for the next iteration,
       i.e. the next x is x2 + t*(x1-x2).
""")
    else:
        print("""Usage:
solver.root_in(f, x1, x2, {method, iterations, abs_err_1, abs_err_2, rel_err, f1, f2})
solver.optimize(g, x1, x2, {method, iterations, abs_err_1, abs_err_2, rel_err, f})

@params
    g: the searched function for the local extrema.
    f: the searched function for the root. Represents the derivative of g for solver.optimize.
    x1, x2: initial bracket.
    method: string name of the method used for solver.root_in.
    iterations: limit on the number of iterations before binary search is used instead of the chosen method.
    abs_err_1: desired absolute error of |x1-x2|.
    rel_err_1: desired relative error of |x1-x2|.
    abs_err_2: larger initial absolute error searched for.
    rel_err_2: larger initial relative error searched for.
    f1, f2: optional initial values of f(x1) and f(x2).

Use solver.help('root_in'), solver.help('optimize'), or solver.help('methods') for more specific information, or check the github wiki at https://github.com/SimpleArt/solver/wiki.
""")


def bracketing_method(x1, f1, x2, f2, x3, f3, x4, f4, t):
    """Interface for the bracketing method.
    
    @params:
        x1, f1: bracketing point for x2.
        x2, f2: last estimate of the root.
        x3, f3: last removed point from the interval.
        x4, f4: second last removed point from the interval, initially None.
        t: last computed t.
    
    @returns:
        t: the combination of x1 and x2 for the next iteration,
           i.e. the next x is x1 + t*(x2-x1).
    """
    
    pass


def root_in(f, x1, x2,
                method = 'chandrupatla mixed',
                iterations = 70,
                abs_err_1 = None,
                rel_err_1 = None,
                abs_err_2 = None,
                rel_err_2 = None,
                x_init = nan,
                f1 = None,
                f2 = None
            ):
    """Run a bracketing method to find a root of f between x1 and x2.
    Requires f(x1) and f(x2) to have different signs.
    Otherwise:
    - only one iteration of the secant method is used.
    - the returned result is out of [x1, x2].
    """
    
    """Set bracketing method to be used"""
    bracketing_method = bracketing_method_dict[method]
    
    # Compute initial points
    if x1 == x2: return x1
    if is_infinite(x1):
        x1 = sign(x1)*realmax
    if is_infinite(x2):
        x2 = sign(x2)*realmax
    if f1 is None: f1 = f(x1)
    if f2 is None: f2 = f(x2)
    if is_nan(f1) or is_nan(f2) or f1 == f2:
        return 0 if return_iterations else 0.5*(x1+x2)
    if f1 == 0:
        return 0 if return_iterations else x1
    if f2 == 0:
        return 0 if return_iterations else x2
    if sign(f1) == sign(f2):
        return 0 if return_iterations else (f2*x1-f1*x2)/(f2-f1)
    
    # Set default errors
    if abs_err_1 is None: abs_err_1 = 1e-14 * min(1, abs(x2-x1))
    if rel_err_1 is None: rel_err_1 = 1e-14
    if abs_err_2 is None: abs_err_2 = 1e+12 * abs_err_1
    if rel_err_2 is None: rel_err_2 = 1e+12 * rel_err_1
    
    # Swap errors if necessary
    if abs_err_1 > abs_err_2: abs_err_1, abs_err_2 = abs_err_2, abs_err_1
    if rel_err_1 > rel_err_2: rel_err_1, rel_err_2 = rel_err_2, rel_err_1
    
    # Set minimum errors if necessary
    if abs_err_1 < 4*realmin: abs_err_1 = 4*realmin
    if rel_err_1 < 1e-14: rel_err_1 = 1e-14
    if abs_err_2 < 4*realmin: abs_err_2 = 4*realmin
    if rel_err_2 < 1e-14: rel_err_2 = 1e-14
    
    """Initialize variables"""
    n = 0
    bisection_fails = 0
    x3, f3 = None, None
    t = 0.5
    bisection_flag = True
    
    """Loop until convergence"""
    while (is_infinite(x1) or abs(x1-x2) > abs_err_1 + 0.5*rel_err_1*abs(x1+x2)) and f2 != 0 and not is_nan(f2):
        
        # Maximum number of iterations before pure bisection is used.
        if n == iterations:
            bracketing_method = bisection
        
        """Compute next point"""
        
        # 0. Skip if initial point is in the interval.
        # 1. Compute the next point.
        # 1.1. Alternate between arithmetic and geometric mean,
        # 1.2. or just use x = x2 + t*(x1-x2).
        # 2. Apply tolerance.
        # 3. Compute f(x).
        if sign(x_init-x1)*sign(x_init-x2) == -1:
            x = x_init
            t = (x-x2)/(x1-x2)
        else:
            if t == 0.5:
                x = mean(x1, x2, bisection_flag)
            else:
                x = x2 + t*(x1-x2)
            if abs(x1-x2) < 16*(abs_err_2 + rel_err_2*abs(x)):
                abs_err_2 = abs_err_1
                rel_err_2 = rel_err_1
        
        x += 0.25*(abs_err_2 + rel_err_2*abs(x))*sign(0.5*(x1+x2)-x)
        fx = f(x)
        
        """======For seeing iterations======"""
        if print_iterations: print(f'f({x}) \t= {fx}')
        
        """Swap to ensure x replaces x2"""
        if sign(f1) == sign(fx):
            t = 1-t
            x1, x2 = x2, x1
            f1, f2 = f2, f1
        
        x, x2, x3 = x3, x, x2
        fx, f2, f3 = f3, fx, f2
        
        """Update counters"""
        n += 1
        min_x = sign(x1)*sign(x2)*min(abs(x1), abs(x2))
        max_x = max(abs(x1), abs(x2))
        if 8*min_x < max_x:
            if (x1-x2)/(x1-x3) > 0.125:
                bisection_flag = not bisection_flag
            bisection_fails += 1
        elif t < 0.5:
            bisection_fails += 1
        elif t > 0.5:
            bisection_fails = 0
        elif t == 0.5 and (x1-x2)/(x1-x3) > 0.125:
            bisection_flag = not bisection_flag
            if (x1-x2)/(x1-x3) > 0.75:
                bisection_fails += 1
            else:
                bisection_fails = 0
        else:
            bisection_fails = 0
        
        """Compute t for next iteration"""
        
        # Try the current bracketing method
        if bisection_fails < 3:
            t = bracketing_method(x1, f1, x2, f2, x3, f3, x, fx, t)
        
        # Adjust the current bracketing
        # method to encourage tight bounds.
        if bisection_fails == 3:
            
            # Try the Illinois method
            temp = bracketing_method(x1, 0.5*f3*((x1-x2)/(x3-x2)), x2, f2, x3, f3, x, fx, t)
            
            # Resort to over-stepping if Illinois has no effect or is too slow
            if 4*n > iterations or temp == bracketing_method(x1, f1, x2, f2, x3, f3, x, fx, t):
                temp *= 2
                if temp >= 1: temp -= 1
            
            # Resort to bisection if over-stepped too much
            t = min(0.5, temp)
        
        # Resort to bisection if
        # - interval failed to halve after a corrective adjustment
        # - t is out of bounds
        if bisection_fails > 3 or t >= 1 or t <= 0 or is_nan(t):
            t = 0.5
    
    """======For seeing final result======"""
    if print_result:
        print(f'{n}th iteration:')
        if f2 == 0:
            print(f'f({x2}) = 0.0')
        else:
            print(f'f({(x1*f2-x2*f1)/(f2-f1)}) = {f((x1*f2-x2*f1)/(f2-f1))}')
    
    """Return secant iteration"""
    if return_iterations: return n
    if f2 == 0: return x2
    elif is_nan(f2): return (x1*f3-x3*f1)/(f3-f1)
    else: return (x1*f2-x2*f1)/(f2-f1)


def optimize(g, x1, x2,
                 method = 'chandrupatla mixed',
                 iterations = 70,
                 abs_err_1 = None,
                 rel_err_1 = None,
                 abs_err_2 = None,
                 rel_err_2 = None,
                 x = None,
                 f = None
             ):
    """Runs an optimization method to find relative extrema of g between x1 and x2.
    Requires g to be increasing on one side and decreasing on the other.
    Otherwise:
    - only one iteration of the secant method is used.
    - the returned result is out of [x1, x2].
    
    The derivative is measured by f(x) = g(x+dx) - g(x-dx),
    where dx is based on the error.
    solver.bracket(f, x1, x2, method, iterations, abs_err_1, abs_err_2, rel_err) is used to find the root.
    """
    
    """Set default error"""
    if abs_err_1 is None: abs_err_1 = 1e-8 * min(1, abs(x2-x1))
    if rel_err_1 is None: rel_err_1 = 1e-8
    if abs_err_2 is not None and abs_err_1 > abs_err_2: abs_err_1, abs_err_2 = abs_err_2, abs_err_1
    if rel_err_2 is not None and rel_err_1 > rel_err_2: rel_err_1, rel_err_2 = rel_err_2, rel_err_1
    if abs_err_1 < 4*realmin: abs_err_1 = 4*realmin
    if rel_err_1 < 1e-12: rel_err_1 = 1e-12
    
    """Symmetric difference"""
    if f is None:
        def f(x):
            dx = abs_err_1 + rel_err_1*abs(x)
            g_plus, g_minus = g(x+dx), g(x-dx)
            if is_infinite(g_plus) and g_plus == g_minus: return sign(x)*g_plus
            else: return g_plus - g_minus
    
    x = root_in(f, x1, x2, method, iterations, abs_err_1, rel_err_1, abs_err_2, rel_err_2, x)
    """======For seeing final result======"""
    if print_result and not return_iterations: print(f'\ng({x}) \t= {g(x)}')
    return x


def find_all_points(g, x1, x2,
                        divisions = None,
                        method = None,
                        iterations = None,
                        err = None,
                        f = None
                    ):
    """Finds roots and relative extrema of f over the given interval
    by dividing it into many subintervals and trying both root_in and
    optimize, with a refined search for relative extrema if it is
    known they exist in an interval despite optimization over that
    interval being unusable.
    """
    
    """Set defaults"""
    if divisions is None:
        divisions = 100
    if err is None:
        err = 1e-12
    if f is None:
        def f(x):
            dx = err + 1e-8*abs(x)
            if not is_infinite(dx): return g(x+dx) - g(x-dx)
            gx = g(x)
            if is_infinite(gx): return gx * sign(x)
            else: return 0.0
    
    """Initialize variables"""
    roots = []
    extremas = []
    n = divisions
    x4 = x1 - (x2-x1)/n
    x5 = x1
    g4, g5 = g(x4), g(x5)
    
    # Run over each subinterval
    for k in range(n):
        
        # Compute next points
        x3, x4, x5 = x4, x5, x1 + (k+1)*(x2-x1)/n
        g3, g4, g5 = g4, g5, g(x5)
        x = optimize(g, x4, x5, method, iterations, err, f)
        
        # Extrema found
        if sign(x-x4)*sign(x-x5) < 1:
            
            # Avoid duplicate points that land on an endpoint
            if x != x5 or k == n-1: extremas.append(x)
            gx = g(x)
            
            # Root found
            if gx == 0: roots.append(x)
            
            # Root bracketed
            else:
                if sign(gx)*sign(g4) < 0: roots.append(root_in(g, x4, x, method, iterations, err, g4, gx))
                if sign(gx)*sign(g5) < 0: roots.append(root_in(g, x5, x, method, iterations, err, g5, gx))
        
        # Extrema not found but exists
        elif k > 0 and sign(g4-g3)*sign(g4-g5) > -1 and sign(extremas[-1]-x3)*sign(extremas[-1]-x5) == 1:
            
            # Do a refined search with half as many subdivisions
            list1, list2 = find_all_points(g, x3, x5, n//2, method, iterations, err, f)
            roots += list1
            extremas += list2
        
        # Extrema not found but root exists
        elif sign(g4)*sign(g5) < 1:
            
            x = root_in(g, x4, x5, method, iterations, err, g4, g5)
            
            # Avoid duplicate points that land on an endpoint
            if x != x5 or k == n-1: roots.append(x)
    
    return roots, extremas
