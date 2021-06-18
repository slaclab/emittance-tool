# emittance-tool
Python-based emittance measurement


This code was originally written by Philipp Dijkstal at PSI, in `original`.
There you will also find an "example" folder with some data and a script inside to trigger the analysis of the raw data and the display of the results.

In general, the code is structured in the following way:

- `EmitMeasToolCore.py` : data acquisition

- `EmitMeasToolMain.py`: GUI

- `beamdynamics.py`: analysis

- `MatchingToolMain.py`: matching

- `plot_results.py`: display

- `EmittanceToolConfig.py1: configuration