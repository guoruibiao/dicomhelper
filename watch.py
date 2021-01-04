#coding: utf8

import pydicom

filepath = "./dataone/1/I9500000"
filepath = "/tmp/I9500000"
ds = pydicom.dcmread(filepath)

metas = [
    "PatientID","PatientName","PatientBirthDate","PatientSex","InstitutionName",
    "PatientStatus", "PatientWeight", "ContrastBolusAgent", "StudyDescription",
]

for meta in metas:
    print(ds.data_element(meta))