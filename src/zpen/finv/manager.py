from typing import Any, Dict, Iterable, List, Callable
import time

import zmq
from zmq.decorators import context, socket

MAX_TASKS_TO_SEND = 10


# noinspection DuplicatedCode
def run_strategies(func: Callable, param_space: Dict[str, Iterable]) -> List:
    """
    :param func: pickleable function to call with each set of params from param_space
    :param param_space: dict of parameters as keys, values can be one of the:
        -- any iterable of possible values
        -- Tuple of 3 floats: start, end, step [ end is inclusive ]
    :return:
    """
    print("run_strategies")
    param_space = _spread_the_tuples(param_space)
    params_list: List[Dict[str, Any]] = _get_params_list(param_space)

    results = _work(func=func, params_list=params_list)
    return results


@context()
@socket(zmq.PUSH)  # pushes jobs to workers
@socket(zmq.PULL)  # receives results from collector
def _work(ctx, push, pull, func: Callable, params_list: List[Dict[str, Any]]) -> List:
    push.bind("tcp://*:5557")
    pull.connect("tcp://localhost:5559")
    time.sleep(.3)  # allow all workers to connect

    task_to_run_next = 0
    tasks_total_count = len(params_list)
    tasks_to_start_first = min(tasks_total_count, MAX_TASKS_TO_SEND)
    for i in range(tasks_to_start_first):
        push.send_pyobj({"func": func, "params": params_list[task_to_run_next]})
        task_to_run_next += 1

    results = []
    for j in range(tasks_total_count):
        result = pull.recv_pyobj()
        results.append(result)
        if task_to_run_next < tasks_total_count:
            push.send_pyobj({"func": func, "params": params_list[task_to_run_next]})
            task_to_run_next += 1

    return results


# noinspection DuplicatedCode
def run_strategies_no_zmq(func: Callable, param_space: Dict[str, Iterable]) -> List:
    """
    :param func: pickleable function to call with each set of params from param_space
    :param param_space: dict of parameters as keys, values can be one of the:
        -- any iterable of possible values
        -- Tuple of 3 floats: start, end, step [ end is inclusive ]
    :return:
    """
    print("run_strategies START")

    param_space = _spread_the_tuples(param_space)
    params_list: List[Dict[str, Any]] = _get_params_list(param_space)

    results = []

    for params in params_list:
        result = func(**params)
        results.append({"result": result, "params": params})

    print("run_strategies END")
    return results


def _spread_the_tuples(param_space: Dict[str, Iterable]) -> Dict[str, Iterable]:
    """
    Changes 3-tuples like (1, 3, 0.5) into lists like [1.0, 1.5, 2.0, 2.5, 3.0]
    both start and end included
    """
    for p in param_space:
        v = param_space[p]
        if isinstance(v, tuple) and len(v) == 3:
            v1 = tuple(v)
            start = v1[0]
            end = v1[1]
            step = v1[2]
            if isinstance(start, (int, float)) and isinstance(end, (int, float)) and isinstance(step, (int, float)):
                if step == 0 or abs(start - end) / abs(step) > 10000:
                    raise Exception("Infinite loop: step 0 [ or just too many steps ]")
                if step < 0:
                    start, end, step = end, start, -step
                current_value = start
                v2 = []
                while current_value < end + step / 1000:  # trick to include the end
                    v2.append(float(current_value))
                    current_value += step
                param_space[p] = v2

    return param_space


def _get_params_list(param_space: Dict[str, Iterable]) -> List[Dict[str, Any]]:
    param_space = param_space.copy()

    params_list: List[Dict[str, Any]] = []

    if len(param_space) == 0:
        return params_list

    p, p_values = param_space.popitem()

    for v in p_values:
        params = {p: v}
        if len(param_space) == 0:
            params_list.append(params)
        else:
            inner_params_list = _get_params_list(param_space)
            for inner_params in inner_params_list:
                params_list.append(inner_params | params)

    return params_list
