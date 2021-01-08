#coding: utf8

import pydicom
from pydicom._dicom_dict import DicomDictionary

filepath = "./dataone/1/I9500000"
filepath = "/tmp/I9500000"
ds = pydicom.dcmread(filepath)

metas = [
    # "PatientID","PatientName","PatientBirthDate","PatientSex","InstitutionName",
    # "PatientStatus", "PatientWeight", "ContrastBolusAgent", "StudyDescription",
    # 机构信息
    "InstitutionName",
    # 患者信息
    "PatientName", "PatientID", "IssuerOfPatientID", "PatientBirthDate", "PatientSex", "OtherPatientIDs",
    "PatientAge", "PatientSize", "PatientWeight", "AdditionalPatientHistory",
    # 症状描述
    "ContrastBolusAgent", "BodyPartExamined",
]

for meta in metas:
    print(ds.data_element(meta))

import sys
sys.exit(0)
dd = DicomDictionary
canAnomoyous = []
for item in dd.items():
    code, alias = item[0], item[1][4]
    # alias = str(alias).strip(" ").replace(" ", "")
    try:
        val = ds.data_element(alias)
    except Exception as e:
        # print("error=", e)
        continue
    canAnomoyous.append(alias)
    print(code, " | ", alias, " | ", val)

print("------------------")
print(canAnomoyous)
print(len(canAnomoyous))