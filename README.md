# API Health Checker

## Overview
This program monitors the health of HTTP endpoints specified in a YAML configuration file, logging each endpoint’s availability percentage every 15 seconds.
\nAny configuration file that contains API endpoint details can be given as input in the command line, the full path to the file needs to be given.
If no config file is given, the program will use the default config file that is mentioned in the assignment as an example. 

## Requirements
- Python 3.7+
- FastAPI
- httpx
- pyyaml

## Installation

```bash
pip install fastapi httpx pyyaml
```
## Running the program
 
```bash
git clone https://github.com/mk797/api-health-check
```

```bash
cd api-health-check
```

```bash
python3 health_check.py [config file path]
```
