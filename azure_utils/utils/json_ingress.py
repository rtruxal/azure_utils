import json
import pkg_resources

json_files = [f for f in pkg_resources.resource_listdir('config', '')
              if f.endswith('.json')]
model = json.load(pkg_resources.resource_stream('config', json_files[0]))
