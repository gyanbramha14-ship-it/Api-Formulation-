import requests
import streamlit as st
import pandas as pd
from urllib.parse import quote

st.set_page_config(
    page_title="Pharma Drug Formulation Database",
    page_icon="💊",
    layout="wide"
)


DRUGS = [
    {
        "name": "Paracetamol",
        "class": "Analgesic / Antipyretic",
        "forms": ["Tablet", "Capsule", "Syrup", "Suspension", "Injection"],
        "routes": ["Oral", "Intravenous"],
        "uses": "Pain and fever",
        "solubility": "Moderately soluble in water",
        "dose_type": "Medium dose",
        "stability": "Protect from moisture and excessive heat"
    },
    {
        "name": "Ibuprofen",
        "class": "NSAID",
        "forms": ["Tablet", "Capsule", "Suspension", "Gel"],
        "routes": ["Oral", "Topical"],
        "uses": "Pain, inflammation and fever",
        "solubility": "Practically insoluble in water",
        "dose_type": "Medium dose",
        "stability": "Protect from moisture and light"
    },
    {
        "name": "Aspirin",
        "class": "NSAID / Antiplatelet",
        "forms": ["Tablet", "Chewable Tablet"],
        "routes": ["Oral"],
        "uses": "Pain, fever and antiplatelet therapy",
        "solubility": "Slightly soluble in water",
        "dose_type": "Low to medium dose",
        "stability": "Moisture sensitive; hydrolysis may occur"
    },
    {
        "name": "Naproxen",
        "class": "NSAID",
        "forms": ["Tablet", "Capsule", "Suspension"],
        "routes": ["Oral"],
        "uses": "Pain and inflammation",
        "solubility": "Practically insoluble in water",
        "dose_type": "Medium dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Diclofenac",
        "class": "NSAID",
        "forms": ["Tablet", "Capsule", "Gel", "Injection", "Suppository"],
        "routes": ["Oral", "Topical", "Intramuscular", "Rectal"],
        "uses": "Pain and inflammation",
        "solubility": "Practically insoluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from moisture and light"
    },
    {
        "name": "Amoxicillin",
        "class": "Penicillin Antibiotic",
        "forms": ["Tablet", "Capsule", "Oral Suspension"],
        "routes": ["Oral"],
        "uses": "Bacterial infections",
        "solubility": "Slightly soluble in water",
        "dose_type": "High dose",
        "stability": "Moisture and temperature controlled storage"
    },
    {
        "name": "Azithromycin",
        "class": "Macrolide Antibiotic",
        "forms": ["Tablet", "Capsule", "Oral Suspension", "Injection"],
        "routes": ["Oral", "Intravenous"],
        "uses": "Bacterial infections",
        "solubility": "Slightly soluble in water",
        "dose_type": "Medium dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Ciprofloxacin",
        "class": "Fluoroquinolone Antibiotic",
        "forms": ["Tablet", "Oral Suspension", "Eye Drops", "Injection"],
        "routes": ["Oral", "Ophthalmic", "Intravenous"],
        "uses": "Bacterial infections",
        "solubility": "Slightly soluble in water",
        "dose_type": "Medium dose",
        "stability": "Protect from light"
    },
    {
        "name": "Levofloxacin",
        "class": "Fluoroquinolone Antibiotic",
        "forms": ["Tablet", "Eye Drops", "Injection"],
        "routes": ["Oral", "Ophthalmic", "Intravenous"],
        "uses": "Bacterial infections",
        "solubility": "Soluble in acidic conditions",
        "dose_type": "Medium dose",
        "stability": "Protect from light"
    },
    {
        "name": "Doxycycline",
        "class": "Tetracycline Antibiotic",
        "forms": ["Tablet", "Capsule"],
        "routes": ["Oral"],
        "uses": "Bacterial infections",
        "solubility": "Slightly soluble in water",
        "dose_type": "Low to medium dose",
        "stability": "Protect from moisture and light"
    },
    {
        "name": "Metronidazole",
        "class": "Antibacterial / Antiprotozoal",
        "forms": ["Tablet", "Suspension", "Gel", "Injection"],
        "routes": ["Oral", "Topical", "Intravenous"],
        "uses": "Anaerobic and protozoal infections",
        "solubility": "Sparingly soluble in water",
        "dose_type": "High dose",
        "stability": "Protect from light"
    },
    {
        "name": "Tinidazole",
        "class": "Antiprotozoal",
        "forms": ["Tablet"],
        "routes": ["Oral"],
        "uses": "Protozoal and anaerobic infections",
        "solubility": "Slightly soluble in water",
        "dose_type": "High dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Cefixime",
        "class": "Cephalosporin Antibiotic",
        "forms": ["Tablet", "Capsule", "Oral Suspension"],
        "routes": ["Oral"],
        "uses": "Bacterial infections",
        "solubility": "Poorly soluble in water",
        "dose_type": "Medium dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Cephalexin",
        "class": "Cephalosporin Antibiotic",
        "forms": ["Capsule", "Tablet", "Oral Suspension"],
        "routes": ["Oral"],
        "uses": "Bacterial infections",
        "solubility": "Soluble in water",
        "dose_type": "High dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Ceftriaxone",
        "class": "Cephalosporin Antibiotic",
        "forms": ["Injection"],
        "routes": ["Intravenous", "Intramuscular"],
        "uses": "Serious bacterial infections",
        "solubility": "Soluble in water",
        "dose_type": "High dose",
        "stability": "Sterile product; protect from light"
    },
    {
        "name": "Pantoprazole",
        "class": "Proton Pump Inhibitor",
        "forms": ["Tablet", "Injection"],
        "routes": ["Oral", "Intravenous"],
        "uses": "Acid-related disorders",
        "solubility": "Practically insoluble in water",
        "dose_type": "Low dose",
        "stability": "Acid sensitive; enteric protection may be required"
    },
    {
        "name": "Omeprazole",
        "class": "Proton Pump Inhibitor",
        "forms": ["Capsule", "Tablet", "Powder"],
        "routes": ["Oral"],
        "uses": "Acid-related disorders",
        "solubility": "Practically insoluble in water",
        "dose_type": "Low dose",
        "stability": "Acid and moisture sensitive"
    },
    {
        "name": "Esomeprazole",
        "class": "Proton Pump Inhibitor",
        "forms": ["Tablet", "Capsule", "Injection"],
        "routes": ["Oral", "Intravenous"],
        "uses": "Acid-related disorders",
        "solubility": "Practically insoluble in water",
        "dose_type": "Low dose",
        "stability": "Acid sensitive"
    },
    {
        "name": "Famotidine",
        "class": "H2-Receptor Antagonist",
        "forms": ["Tablet", "Injection"],
        "routes": ["Oral", "Intravenous"],
        "uses": "Acid-related disorders",
        "solubility": "Freely soluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Ondansetron",
        "class": "Antiemetic",
        "forms": ["Tablet", "Orally Disintegrating Tablet", "Injection"],
        "routes": ["Oral", "Intravenous"],
        "uses": "Nausea and vomiting",
        "solubility": "Soluble depending on salt form",
        "dose_type": "Low dose",
        "stability": "Protect from light"
    },
    {
        "name": "Domperidone",
        "class": "Gastroprokinetic / Antiemetic",
        "forms": ["Tablet", "Suspension"],
        "routes": ["Oral"],
        "uses": "Nausea and gastric motility disorders",
        "solubility": "Practically insoluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Metoclopramide",
        "class": "Antiemetic / Gastroprokinetic",
        "forms": ["Tablet", "Injection", "Oral Solution"],
        "routes": ["Oral", "Intravenous", "Intramuscular"],
        "uses": "Nausea and vomiting",
        "solubility": "Soluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from light"
    },
    {
        "name": "Loperamide",
        "class": "Antidiarrheal",
        "forms": ["Capsule", "Tablet", "Oral Solution"],
        "routes": ["Oral"],
        "uses": "Diarrhea",
        "solubility": "Practically insoluble in water",
        "dose_type": "Very low dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Lactulose",
        "class": "Osmotic Laxative",
        "forms": ["Oral Solution", "Syrup"],
        "routes": ["Oral"],
        "uses": "Constipation and hepatic encephalopathy",
        "solubility": "Freely soluble in water",
        "dose_type": "High volume liquid dose",
        "stability": "Protect from excessive heat"
    },
    {
        "name": "Metformin",
        "class": "Biguanide Antidiabetic",
        "forms": ["Tablet", "Extended-Release Tablet"],
        "routes": ["Oral"],
        "uses": "Type 2 diabetes",
        "solubility": "Freely soluble in water",
        "dose_type": "High dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Glimepiride",
        "class": "Sulfonylurea Antidiabetic",
        "forms": ["Tablet"],
        "routes": ["Oral"],
        "uses": "Type 2 diabetes",
        "solubility": "Practically insoluble in water",
        "dose_type": "Very low dose",
        "stability": "Protect from moisture and light"
    },
    {
        "name": "Gliclazide",
        "class": "Sulfonylurea Antidiabetic",
        "forms": ["Tablet", "Modified-Release Tablet"],
        "routes": ["Oral"],
        "uses": "Type 2 diabetes",
        "solubility": "Practically insoluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Sitagliptin",
        "class": "DPP-4 Inhibitor",
        "forms": ["Tablet"],
        "routes": ["Oral"],
        "uses": "Type 2 diabetes",
        "solubility": "Soluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Dapagliflozin",
        "class": "SGLT2 Inhibitor",
        "forms": ["Tablet"],
        "routes": ["Oral"],
        "uses": "Diabetes and selected cardiovascular or renal conditions",
        "solubility": "Slightly soluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Levothyroxine",
        "class": "Thyroid Hormone",
        "forms": ["Tablet", "Injection"],
        "routes": ["Oral", "Intravenous"],
        "uses": "Hypothyroidism",
        "solubility": "Very slightly soluble in water",
        "dose_type": "Very low dose",
        "stability": "Sensitive to light and moisture"
    },
    {
        "name": "Amlodipine",
        "class": "Calcium Channel Blocker",
        "forms": ["Tablet"],
        "routes": ["Oral"],
        "uses": "Hypertension and angina",
        "solubility": "Slightly soluble in water",
        "dose_type": "Very low dose",
        "stability": "Protect from light"
    },
    {
        "name": "Atenolol",
        "class": "Beta Blocker",
        "forms": ["Tablet", "Injection"],
        "routes": ["Oral", "Intravenous"],
        "uses": "Hypertension and cardiovascular conditions",
        "solubility": "Soluble in water",
        "dose_type": "Medium dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Metoprolol",
        "class": "Beta Blocker",
        "forms": ["Tablet", "Extended-Release Tablet", "Injection"],
        "routes": ["Oral", "Intravenous"],
        "uses": "Hypertension and cardiovascular conditions",
        "solubility": "Soluble in water",
        "dose_type": "Medium dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Losartan",
        "class": "Angiotensin Receptor Blocker",
        "forms": ["Tablet"],
        "routes": ["Oral"],
        "uses": "Hypertension",
        "solubility": "Slightly soluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Telmisartan",
        "class": "Angiotensin Receptor Blocker",
        "forms": ["Tablet"],
        "routes": ["Oral"],
        "uses": "Hypertension",
        "solubility": "Practically insoluble in water",
        "dose_type": "Medium dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Enalapril",
        "class": "ACE Inhibitor",
        "forms": ["Tablet", "Injection"],
        "routes": ["Oral", "Intravenous"],
        "uses": "Hypertension and heart failure",
        "solubility": "Soluble depending on salt form",
        "dose_type": "Low dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Furosemide",
        "class": "Loop Diuretic",
        "forms": ["Tablet", "Oral Solution", "Injection"],
        "routes": ["Oral", "Intravenous", "Intramuscular"],
        "uses": "Edema and hypertension",
        "solubility": "Slightly soluble in water",
        "dose_type": "Low to medium dose",
        "stability": "Protect from light"
    },
    {
        "name": "Hydrochlorothiazide",
        "class": "Thiazide Diuretic",
        "forms": ["Tablet", "Capsule"],
        "routes": ["Oral"],
        "uses": "Hypertension and edema",
        "solubility": "Slightly soluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from light"
    },
    {
        "name": "Spironolactone",
        "class": "Potassium-Sparing Diuretic",
        "forms": ["Tablet", "Oral Suspension"],
        "routes": ["Oral"],
        "uses": "Edema and selected cardiovascular conditions",
        "solubility": "Practically insoluble in water",
        "dose_type": "Medium dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Atorvastatin",
        "class": "Statin",
        "forms": ["Tablet"],
        "routes": ["Oral"],
        "uses": "Dyslipidemia",
        "solubility": "Practically insoluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from light and moisture"
    },
    {
        "name": "Rosuvastatin",
        "class": "Statin",
        "forms": ["Tablet"],
        "routes": ["Oral"],
        "uses": "Dyslipidemia",
        "solubility": "Slightly soluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Clopidogrel",
        "class": "Antiplatelet",
        "forms": ["Tablet"],
        "routes": ["Oral"],
        "uses": "Prevention of thrombotic cardiovascular events",
        "solubility": "Practically insoluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Salbutamol",
        "class": "Bronchodilator",
        "forms": ["Tablet", "Syrup", "Inhaler", "Nebulizer Solution"],
        "routes": ["Oral", "Inhalation"],
        "uses": "Bronchospasm and asthma",
        "solubility": "Soluble depending on salt form",
        "dose_type": "Low dose",
        "stability": "Protect from light"
    },
    {
        "name": "Budesonide",
        "class": "Corticosteroid",
        "forms": ["Inhaler", "Nebulizer Suspension", "Capsule"],
        "routes": ["Inhalation", "Oral"],
        "uses": "Respiratory and inflammatory conditions",
        "solubility": "Practically insoluble in water",
        "dose_type": "Very low dose",
        "stability": "Protect from light and moisture"
    },
    {
        "name": "Montelukast",
        "class": "Leukotriene Receptor Antagonist",
        "forms": ["Tablet", "Chewable Tablet", "Granules"],
        "routes": ["Oral"],
        "uses": "Asthma and allergic rhinitis",
        "solubility": "Practically insoluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Cetirizine",
        "class": "Antihistamine",
        "forms": ["Tablet", "Syrup", "Oral Solution"],
        "routes": ["Oral"],
        "uses": "Allergic conditions",
        "solubility": "Soluble depending on salt form",
        "dose_type": "Low dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Loratadine",
        "class": "Antihistamine",
        "forms": ["Tablet", "Syrup"],
        "routes": ["Oral"],
        "uses": "Allergic conditions",
        "solubility": "Practically insoluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Fexofenadine",
        "class": "Antihistamine",
        "forms": ["Tablet", "Oral Suspension"],
        "routes": ["Oral"],
        "uses": "Allergic conditions",
        "solubility": "Soluble depending on salt form",
        "dose_type": "Medium dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Mupirocin",
        "class": "Topical Antibiotic",
        "forms": ["Cream", "Ointment"],
        "routes": ["Topical"],
        "uses": "Local bacterial skin infections",
        "solubility": "Practically insoluble in water",
        "dose_type": "Topical",
        "stability": "Protect from heat"
    },
    {
        "name": "Clotrimazole",
        "class": "Antifungal",
        "forms": ["Cream", "Lotion", "Tablet", "Vaginal Tablet"],
        "routes": ["Topical", "Vaginal"],
        "uses": "Fungal infections",
        "solubility": "Practically insoluble in water",
        "dose_type": "Topical",
        "stability": "Protect from moisture"
    },
    {
        "name": "Fluconazole",
        "class": "Triazole Antifungal",
        "forms": ["Tablet", "Capsule", "Oral Suspension", "Injection"],
        "routes": ["Oral", "Intravenous"],
        "uses": "Fungal infections",
        "solubility": "Soluble in water",
        "dose_type": "Medium dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Acyclovir",
        "class": "Antiviral",
        "forms": ["Tablet", "Cream", "Ointment", "Injection"],
        "routes": ["Oral", "Topical", "Intravenous"],
        "uses": "Herpes virus infections",
        "solubility": "Slightly soluble in water",
        "dose_type": "Medium to high dose",
        "stability": "Protect from moisture"
    },
    {
        "name": "Hydrocortisone",
        "class": "Corticosteroid",
        "forms": ["Cream", "Ointment", "Tablet", "Injection"],
        "routes": ["Topical", "Oral", "Intravenous"],
        "uses": "Inflammatory and allergic conditions",
        "solubility": "Practically insoluble in water",
        "dose_type": "Low dose",
        "stability": "Protect from light"
    }
]


BASE_EXCIPIENTS = {
    "Diluent": [
        "Microcrystalline cellulose",
        "Lactose",
        "Dicalcium phosphate",
        "Mannitol"
    ],
    "Binder": [
        "Povidone",
        "Pregelatinized starch",
        "Hydroxypropyl cellulose"
    ],
    "Disintegrant": [
        "Croscarmellose sodium",
        "Crospovidone",
        "Sodium starch glycolate"
    ],
    "Lubricant": [
        "Magnesium stearate",
        "Stearic acid",
        "Sodium stearyl fumarate"
    ],
    "Glidant": [
        "Colloidal silicon dioxide",
        "Talc"
    ],
    "Suspending agent": [
        "Sodium carboxymethylcellulose",
        "Xanthan gum",
        "Methylcellulose"
    ],
    "Preservative": [
        "Methylparaben",
        "Propylparaben",
        "Potassium sorbate"
    ],
    "Vehicle": [
        "Purified water",
        "Glycerin",
        "Propylene glycol"
    ],
    "Film former": [
        "Hypromellose",
        "Polyvinyl alcohol"
    ],
    "Sweetener": [
        "Sucrose",
        "Sorbitol",
        "Sucralose"
    ],
    "Buffer or pH adjuster": [
        "Phosphate buffer",
        "Citrate buffer",
        "Sodium hydroxide",
        "Citric acid"
    ]
}


def find_drug(name):
    for
