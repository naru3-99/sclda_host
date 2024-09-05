from typing import Any, Callable, List, Union

import multiprocessing as mp
import concurrent.futures

_manager = mp.Manager()
ALL_PROCESS_LS = _manager.list()

def start_process(
    target: Callable[..., Any], *args: Union[List[Any], Any]
) -> mp.Process:
    """
    Starts a new process with the specified target function.

    Parameters:
    target (Callable): The function to be executed in the new process.
    *args (List[Any]): The list of arguments to be passed to the target function.

    Returns:
    Process: The new process object.
    """
    process = mp.Process(target=target, args=args)
    process.start()
    ALL_PROCESS_LS.append(process)
    return process


def is_process_alive(process: mp.Process) -> bool:
    return process.is_alive()


def are_all_processes_terminated() -> bool:
    """
    Checks if all processes in the global process list have terminated.

    Returns:
    bool: True if all processes have terminated, False otherwise.
    """
    # すべてのプロセスが終了しているか確認
    return all(not is_process_alive(process) for process in ALL_PROCESS_LS)


def stop_process(process: mp.Process) -> None:
    """
    Terminates the specified process.

    Parameters:
    process (Process): The process object to be terminated.
    """
    if is_process_alive(process):
        process.terminate()


def parallel_process(func: Callable[..., Any], data_list: List[Any]) -> List[Any]:
    """
    Applies the specified function to every element in the list using concurrent.futures to parallelize the operation.

    Args:
        func (Callable[..., Any]): A function that takes one or more arguments and returns a value.
        data_list (List[Any]): A list of elements (or tuples of elements) to which the function will be applied.

    Returns:
        List[Any]: A list of results after applying the function to the elements of data_list.
    """
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(func, data_list)
    return list(results)
