import json,sys
from .core import from_json,evaluate
if __name__=='__main__':
    data=json.load(open(sys.argv[1]))
    chunks,policy=from_json(data); result=evaluate(chunks,policy)
    print(json.dumps(result.as_dict(),indent=2)); raise SystemExit(0 if result.allowed else 2)
