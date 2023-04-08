from dataprofiler import Data, Profiler
import pathlib
import json


path = "./rawdata"
data = pathlib.Path(path)

# recursively read files
files = list(data.rglob("*.csv*"))
# conver POSIX to string
files = [str(file) for file in files]


# load a file
df = Data(files[50])

# Profile a dataset
profile = Profiler(df)

# 
report = profile.report(report_options={"output_format":"pretty"})

print(json.dumps(report,indent=4))