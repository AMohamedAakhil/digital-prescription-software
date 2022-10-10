import json

import api

instance = api.RxNorm()

result = instance.get_drug_list("ibuprofen").get("drugGroup").get("conceptGroup")

instance.parse_result(result)

