import yaml

def loadyaml(filename):
    with open(filename,'r') as f:
        return yaml.safe_load(f)