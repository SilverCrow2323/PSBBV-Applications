#!/usr/bin/env python3
"""Validate the PSBBV Applications catalogue schema and cross-entry identity rules."""
from __future__ import annotations
import copy, json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
ROOT=Path(__file__).resolve().parents[1]
def load(path): return json.loads(path.read_text(encoding="utf-8"))
def validate_catalogue(schema,catalogue):
 validator=Draft202012Validator(schema,format_checker=FormatChecker())
 errors=list(validator.iter_errors(catalogue))
 if errors: return errors
 ids=set(); title_ids=set()
 for index,app in enumerate(catalogue["applications"]):
  if app["id"] in ids: return [ValueError(f"duplicate application id at applications[{index}]: {app['id']}")]
  ids.add(app["id"])
  title=app.get("title_id")
  if title and title in title_ids: return [ValueError(f"duplicate Vita title ID at applications[{index}]: {title}")]
  if title: title_ids.add(title)
 return []
def main():
 schema=load(ROOT/"schemas"/"application-catalogue.schema.json")
 catalogue=load(ROOT/"catalogue.example.json")
 Draft202012Validator.check_schema(schema)
 validator=Draft202012Validator(schema,format_checker=FormatChecker())
 errors=validate_catalogue(schema,catalogue)
 if errors:
  for error in errors: print(f"INVALID {getattr(error,'json_path','<catalogue>')}: {error}")
  return 1
 invalid=[]
 duplicate_id=copy.deepcopy(catalogue); duplicate_id["applications"]=[
  {"id":"demo-app","name":"Demo One","version":"1.0","status":"planned","platform":"psvita","category":"utility"},
  {"id":"demo-app","name":"Demo Two","version":"1.0","status":"planned","platform":"psvita","category":"utility"}]
 invalid.append(("duplicate application ID",duplicate_id))
 duplicate_title=copy.deepcopy(catalogue); duplicate_title["applications"]=[
  {"id":"demo-one","name":"Demo One","version":"1.0","status":"planned","platform":"psvita","category":"utility","title_id":"PCSE00001"},
  {"id":"demo-two","name":"Demo Two","version":"1.0","status":"planned","platform":"psvita","category":"utility","title_id":"PCSE00001"}]
 invalid.append(("duplicate title ID",duplicate_title))
 bad_digest=copy.deepcopy(catalogue); bad_digest["applications"]=[{
  "id":"approved-demo","name":"Approved Demo","version":"1.0","status":"approved","platform":"psvita","category":"utility",
  "package":{"url":"https://downloads.example.invalid/demo.vpk","size_bytes":1024,"sha256":"not-a-hash","format":"vpk"}}]
 invalid.append(("invalid package digest",bad_digest))
 insecure_url=copy.deepcopy(catalogue); insecure_url["source"]["url"]="http://catalogue.example.invalid/list.json"
 invalid.append(("non-HTTPS source",insecure_url))
 approved_without_package=copy.deepcopy(catalogue); approved_without_package["applications"]=[{
  "id":"approved-demo","name":"Approved Demo","version":"1.0","status":"approved","platform":"psvita","category":"utility"}]
 invalid.append(("approved entry without package",approved_without_package))
 for label,fixture in invalid:
  if not validate_catalogue(schema,fixture):
   print(f"INVALID TEST: {label} was accepted")
   return 1
 print(f"PSBBV Applications catalogue: valid; {len(invalid)} negative cases rejected.")
 return 0
if __name__=="__main__": raise SystemExit(main())
