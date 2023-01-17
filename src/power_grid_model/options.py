# SPDX-FileCopyrightText: 2022 Contributors to the Power Grid Model project <dynamic.grid.calculation@alliander.com>
#
# SPDX-License-Identifier: MPL-2.0


"""
Option class
"""
from typing import Any

from power_grid_model.power_grid_core import OptionsPtr
from power_grid_model.power_grid_core import power_grid_core as pgc


class OptionSetter:
    _setter: callable

    def __init__(self, setter):
        self._setter = setter

    def __set__(self, instance: "Options", value: Any):
        self._setter(instance.opt, value)

    def __get__(self, instance, owner):
        raise NotImplementedError("Cannot get option value!")


class Options:
    _opt: OptionsPtr
    # option setter
    calculation_type = OptionSetter(pgc.set_calculation_type)
    calculation_method = OptionSetter(pgc.set_calculation_method)
    symmetric = OptionSetter(pgc.set_symmetric)
    error_tolerance = OptionSetter(pgc.set_err_tol)
    max_iteration = OptionSetter(pgc.set_max_iter)
    threading = OptionSetter(pgc.set_threading)

    @property
    def opt(self) -> OptionsPtr:
        if not self._opt:
            raise ValueError("Null option pointer!")
        return self._opt

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls, *args, **kwargs)
        instance._opt = pgc.create_options()
        return instance

    def __del__(self):
        pgc.destroy_options(self._opt)

    # not copyable
    def __copy__(self):
        raise NotImplementedError("Class not copyable")

    def __deepcopy__(self, memodict):
        raise NotImplementedError("class not copyable")
