"""Pruebas sin red de motor/openverse.py (licencias, restricciones, créditos). Uso: python3 motor/prueba_openverse.py"""
import sys; import os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from motor import openverse as ov
def cm(short, url="", lic="", terms="", restr="", artist="<a href='x'>Hans Glaser</a>", copyrighted="False"):
    return {"query":{"pages":{"1":{"title":"File:Celestial phenomenon over Nuremberg.jpg","imageinfo":[{"url":"https://upload.wikimedia.org/x.jpg","descriptionurl":"https://commons.wikimedia.org/wiki/File:X.jpg","width":2000,"height":2800,
      "extmetadata":{"LicenseShortName":{"value":short},"LicenseUrl":{"value":url},"License":{"value":lic},"UsageTerms":{"value":terms},"Restrictions":{"value":restr},"Artist":{"value":artist},"Copyrighted":{"value":copyrighted}}}]}}}}
casos=[("Public domain","", "pd-old-100","Public domain",True),
("Public domain","", "pd-us-expired","Public domain in the United States",False),
("Public domain","", "pd-usgov-nasa","Public domain",True),
("CC BY 4.0","https://creativecommons.org/licenses/by/4.0","cc-by-4.0","",True),
("CC BY-SA 4.0","https://creativecommons.org/licenses/by-sa/4.0","cc-by-sa-4.0","",False),
("CC BY-NC 2.0","https://creativecommons.org/licenses/by-nc/2.0","","",False),
("CC0","https://creativecommons.org/publicdomain/zero/1.0","cc0","",True),
("CC BY 2.0","https://creativecommons.org/licenses/by/2.0","cc-by-2.0","",True)]
ok=True
for short,url,lic,terms,esperado in casos:
    r=ov.evaluar_commons(cm(short,url,lic,terms)); ok&= r["ok"]==esperado; print(short,lic,"->",r["ok"],r.get("motivo",r.get("licencia")))
r=ov.evaluar_commons(cm("CC BY 4.0","https://creativecommons.org/licenses/by/4.0",restr="personality")); print("personality ->",r["ok"]); ok&=not r["ok"]
r=ov.evaluar_met({"isPublicDomain":False}); ok&=not r["ok"]
r=ov.evaluar_met({"isPublicDomain":True,"primaryImage":"https://images.metmuseum.org/a.jpg","title":"Armor","artistDisplayName":"","objectURL":"https://www.metmuseum.org/art/collection/search/1"}); ok&=r["ok"]; print("met ->",r["ok"])
print(ov.filtrar([{"license":"by-sa","source":"wikimedia"},{"license":"by","source":"flickr"},{"license":"cc0","source":"met","width":3000,"height":2000},{"license":"by","source":"wikimedia","width":640,"height":480},{"license":"pdm","source":"wikimedia","mature":True}]))
e={**ov.evaluar_commons(cm("CC BY 4.0","https://creativecommons.org/licenses/by/4.0")),"video":"01"}; print(ov.credito(e))
print("TODO OK" if ok else "FALLOS")
