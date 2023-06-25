import os
import ctypes
import platform
from multiprocessing import Process
from time import sleep


__all__ = ['perform_network_assignment_DTALite', 'run_DTALite']


_os = platform.system()
if _os.startswith('Windows'):
    _dtalite_dll = os.path.join(os.path.dirname(__file__), 'bin/DTALite.dll')
    _dtalitemm_dll = os.path.join(os.path.dirname(__file__), 'bin/DTALiteMM.dll')
elif _os.startswith('Linux'):
    _dtalite_dll = os.path.join(os.path.dirname(__file__), 'bin/DTALite.so')
elif _os.startswith('Darwin'):
    # check CPU is Intel or Apple Silicon
    if platform.machine().startswith('x86_64'):
        _dtalite_dll = os.path.join(os.path.dirname(__file__), 'bin/DTALite_x86.dylib')
        _dtalitemm_dll = os.path.join(os.path.dirname(__file__), 'bin/DTALiteMM_x86.dylib')
    else:
        _dtalite_dll = os.path.join(os.path.dirname(__file__), 'bin/DTALite_arm.dylib')
else:
    raise Exception('Please build the shared library compatible to your OS\
                    using source files')

_dtalitemm_engine = ctypes.cdll.LoadLibrary(_dtalitemm_dll)
_dtalite_engine = ctypes.cdll.LoadLibrary(_dtalite_dll)


_dtalite_engine.network_assignment.argtypes = [ctypes.c_int,
                                               ctypes.c_int,
                                               ctypes.c_int]


def _print_log(input_dir='.'):
    with open(input_dir + '/log_main.txt', 'r') as fp:
        for line in fp:
            print(line)


def perform_network_assignment_DTALite(assignment_mode,
                                       column_gen_num,
                                       column_update_num):
    """ python interface to call DTALite (precompiled as shared library)

    perform network assignment using the selected assignment mode

    WARNING
    -------
    MAKE SURE TO BACKUP agent.csv and link_performance.csv if you have
    called perform_network_assignment() before. Otherwise, they will be
    overwritten by results generated by DTALite.

    Parameters
    ----------
    assignment_mode
        0: Link-based UE, only generates link performance file without agent path file

        1: Path-based UE, generates link performance file and agent path file

        2: UE + dynamic traffic assignment (DTA), generates link performance file and agent path file

        3: ODME

    column_gen_num
        number of iterations to be performed before on generating column pool

    column_update_iter
        number of iterations to be performed on optimizing column pool

    Returns
    -------
    None

    Note
    ----
    The output will depend on the selected assignment_mode.

        Link-based UE: link_performance.csv

        Path-based UE: agent.csv and link_performance.csv

        UE + DTA: agent.csv and link_performance.csv

    agent.csv: paths/columns

    link_performance.csv: assigned volumes and other link attributes
    on each link
    """
    # make sure assignment_mode is right
    assert(assignment_mode in [0, 1, 2, 3])
    # make sure iteration numbers are both non-negative
    assert(column_gen_num>=0)
    assert(column_update_num>=0)

    print('\nDTALite run starts')

    proc_dta = Process(
        target=_dtalite_engine.network_assignment,
        args=(assignment_mode, column_gen_num, column_update_num,)
    )

    proc_print = Process(target=_print_log)

    proc_dta.start()
    proc_print.start()

    proc_dta.join()
    if proc_dta.exitcode is not None:
        sleep(0.1)
        proc_print.join()
        if proc_dta.exitcode == 0:
            print(
                f'check link_performance.csv in {os.getcwd()} for link performance\n'
                f'check agent.csv in {os.getcwd()} for unique agent paths\n'
            )


def run_DTALite():
    print('\nDTALite run starts')

    proc_dta = Process(target=_dtalitemm_engine.DTALiteAPI())
    proc_print = Process(target=_print_log)

    proc_dta.start()
    proc_print.start()

    proc_dta.join()
    if proc_dta.exitcode is not None:
        sleep(0.1)
        proc_print.join()