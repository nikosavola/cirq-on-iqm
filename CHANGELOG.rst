=========
Changelog
=========


Version 0.7
===========

Bugfixes
--------

* Off-by-one error fixed in `IQMDevice.map_circuit <https://github.com/iqm-finland/cirq-on-iqm/blob/a2d09dab583434c89f569e711ac35085ec371342/src/cirq_iqm/iqm_device.py#L120>`_. `#29 <https://github.com/iqm-finland/cirq-on-iqm/pull/29>`_


Version 0.6
===========

Features
--------

* Project setup updated. `#22 <https://github.com/iqm-finland/cirq-on-iqm/pull/22>`_

  * ``pyproject.toml`` added.
  * ``PyScaffold`` dependency removed.
  * Sphinx bumped to version 4.0.2.
  * API docs generated using recursive ``sphinx.ext.autosummary``.
  * ``tox`` scripts for building docs, dist packages.


Version 0.5
===========

Features
--------

* Gate decomposition and circuit optimization procedure simplified. `#21 <https://github.com/iqm-finland/cirq-on-iqm/pull/21>`_
* Cirq dependency bumped to 0.11. `#23 <https://github.com/iqm-finland/cirq-on-iqm/pull/23>`_

NOTE: Before installing this version, please manually uninstall Cirq 0.10. See Cirq 0.11
release notes for more details: https://github.com/quantumlib/Cirq/releases/tag/v0.11.0


Version 0.4
===========

Features
--------

* Convert data to IQM internal format when running requests. `#20 <https://github.com/iqm-finland/cirq-on-iqm/pull/20>`_


Version 0.3
===========

Features
--------

* Settings file support. `#17 <https://github.com/iqm-finland/cirq-on-iqm/pull/17>`_


Version 0.2
===========

Features
--------

* Adonis native gate set updated, CZ-targeting decompositions added. `#15 <https://github.com/iqm-finland/cirq-on-iqm/pull/15>`_
* Circuits can be sent to be executed remotely on IQM hardware. `#13 <https://github.com/iqm-finland/cirq-on-iqm/pull/13>`_


Version 0.1
===========

Released 2021-04-21

Features
--------

* Supports the Adonis and Valkmusa architectures.
* Extends the OpenQASM language with gates native to the IQM architectures.
* Loads quantum circuits from OpenQASM files.
* Decomposes gates into the native gate set of the chosen architecture.
* Optimizes the circuit by merging neighboring gates, and commuting z rotations towards the end of the circuit.
* Circuits can be simulated using both the standard Cirq simulators and the
  `qsim <https://quantumai.google/qsim>`_ simulators.
