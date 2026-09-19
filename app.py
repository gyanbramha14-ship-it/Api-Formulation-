import requests
import streamlit as st
import pandas as pd
from urllib.parse import quote

st.set_page_config(
    page_title="Pharma Drug Database",
    page_icon="💊",
    layout="wide"
)

DRUGS = [
    {
        "name": "Paracetamol",
        "class": "Analgesic / Antipyretic",
        "forms": "Tablet, Capsule, Syrup, Suspension, Injection",
        "routes": "Oral, Intravenous",
        "uses": "Pain and fever"
    },
    {
        "name": "Ibuprofen",
        "class": "NSAID",
        "forms": "Tablet, Capsule, Suspension, Gel",
        "routes": "Oral, Topical",
        "uses": "Pain, inflammation and fever"
    },
    {
        "name": "Aspirin",
        "class": "NSAID / Antiplatelet",
        "forms": "Tablet, Chewable Tablet",
        "routes": "Oral",
        "uses": "Pain, fever and antiplatelet therapy"
    },
    {
        "name": "Naproxen",
        "class": "NSAID",
        "forms": "Tablet, Capsule, Suspension",
        "routes": "Oral",
        "uses": "Pain and inflammation"
    },
    {
        "name": "Diclofenac",
        "class": "NSAID",
        "forms": "Tablet, Capsule, Gel, Injection, Suppository",
        "routes": "Oral, Topical, Intramuscular, Rectal",
        "uses": "Pain and inflammation"
    },
    {
        "name": "Amoxicillin",
        "class": "Penicillin Antibiotic",
        "forms": "Tablet, Capsule, Oral Suspension",
        "routes": "Oral",
        "uses": "Bacterial infections"
    },
    {
        "name": "Azithromycin",
        "class": "Macrolide Antibiotic",
        "forms": "Tablet, Capsule, Oral Suspension, Injection",
        "routes": "Oral, Intravenous",
        "uses": "Bacterial infections"
    },
    {
        "name": "Ciprofloxacin",
        "class": "Fluoroquinolone Antibiotic",
        "forms": "Tablet, Oral Suspension, Eye Drops, Injection",
        "routes": "Oral, Ophthalmic, Intravenous",
        "uses": "Bacterial infections"
    },
    {
        "name": "Levofloxacin",
        "class": "Fluoroquinolone Antibiotic",
        "forms": "Tablet, Eye Drops, Injection",
        "routes": "Oral, Ophthalmic, Intravenous",
        "uses": "Bacterial infections"
    },
    {
        "name": "Doxycycline",
        "class": "Tetracycline Antibiotic",
        "forms": "Tablet, Capsule",
        "routes": "Oral",
        "uses": "Bacterial infections"
    },
    {
        "name": "Metronidazole",
        "class": "Antibacterial / Antiprotozoal",
        "forms": "Tablet, Suspension, Gel, Injection",
        "routes": "Oral, Topical, Intravenous",
        "uses": "Anaerobic and protozoal infections"
    },
    {
        "name": "Tinidazole",
        "class": "Antiprotozoal",
        "forms": "Tablet",
        "routes": "Oral",
        "uses": "Protozoal and anaerobic infections"
    },
    {
        "name": "Cefixime",
        "class": "Cephalosporin Antibiotic",
        "forms": "Tablet, Capsule, Oral Suspension",
        "routes": "Oral",
        "uses": "Bacterial infections"
    },
    {
        "name": "Cephalexin",
        "class": "Cephalosporin Antibiotic",
        "forms": "Capsule, Tablet, Oral Suspension",
        "routes": "Oral",
        "uses": "Bacterial infections"
    },
    {
        "name": "Ceftriaxone",
        "class": "Cephalosporin Antibiotic",
        "forms": "Injection",
        "routes": "Intravenous, Intramuscular",
        "uses": "Serious bacterial infections"
    },
    {
        "name": "Pantoprazole",
        "class": "Proton Pump Inhibitor",
        "forms": "Tablet, Injection",
        "routes": "Oral, Intravenous",
        "uses": "Acid-related disorders"
    },
    {
        "name": "Omeprazole",
        "class": "Proton Pump Inhibitor",
        "forms": "Capsule, Tablet, Powder",
        "routes": "Oral",
        "uses": "Acid-related disorders"
    },
    {
        "name": "Esomeprazole",
        "class": "Proton Pump Inhibitor",
        "forms": "Tablet, Capsule, Injection",
        "routes": "Oral, Intravenous",
        "uses": "Acid-related disorders"
    },
    {
        "name": "Famotidine",
        "class": "H2-Receptor Antagonist",
        "forms": "Tablet, Injection",
        "routes": "Oral, Intravenous",
        "uses": "Acid-related disorders"
    },
    {
        "name": "Ondansetron",
        "class": "Antiemetic",
        "forms": "Tablet, Orally Disintegrating Tablet, Injection",
        "routes": "Oral, Intravenous",
        "uses": "Nausea and vomiting"
    },
    {
        "name": "Domperidone",
        "class": "Gastroprokinetic / Antiemetic",
        "forms": "Tablet, Suspension",
        "routes": "Oral",
        "uses": "Nausea and gastric motility disorders"
    },
    {
        "name": "Metoclopramide",
        "class": "Antiemetic / Gastroprokinetic",
        "forms": "Tablet, Injection, Oral Solution",
        "routes": "Oral, Intravenous, Intramuscular",
        "uses": "Nausea and vomiting"
    },
    {
        "name": "Loperamide",
        "class": "Antidiarrheal",
        "forms": "Capsule, Tablet, Oral Solution",
        "routes": "Oral",
        "uses": "Diarrhea"
    },
    {
        "name": "Lactulose",
        "class": "Osmotic Laxative",
        "forms": "Oral Solution, Syrup",
        "routes": "Oral",
        "uses": "Constipation and hepatic encephalopathy"
    },
    {
        "name": "Metformin",
        "class": "Biguanide Antidiabetic",
        "forms": "Tablet, Extended-Release Tablet",
        "routes": "Oral",
        "uses": "Type 2 diabetes"
    },
    {
        "name": "Glimepiride",
        "class": "Sulfonylurea Antidiabetic",
        "forms": "Tablet",
        "routes": "Oral",
        "uses": "Type 2 diabetes"
    },
    {
        "name": "Gliclazide",
        "class": "Sulfonylurea Antidiabetic",
        "forms": "Tablet, Modified-Release Tablet",
        "routes": "Oral",
        "uses": "Type 2 diabetes"
    },
    {
        "name": "Sitagliptin",
        "class": "DPP-4 Inhibitor",
        "forms": "Tablet",
        "routes": "Oral",
        "uses": "Type 2 diabetes"
    },
    {
        "name": "Dapagliflozin",
        "class": "SGLT2 Inhibitor",
        "forms": "Tablet",
        "routes": "Oral",
        "uses": "Diabetes and selected cardiovascular/renal conditions"
    },
    {
        "name": "Levothyroxine",
        "class": "Thyroid Hormone",
        "forms": "Tablet, Injection",
        "routes": "Oral, Intravenous",
        "uses": "Hypothyroidism"
    },
    {
        "name": "Amlodipine",
        "class": "Calcium Channel Blocker",
        "forms": "Tablet",
        "routes": "Oral",
        "uses": "Hypertension and angina"
    },
    {
        "name": "Atenolol",
        "class": "Beta Blocker",
        "forms": "Tablet, Injection",
        "routes": "Oral, Intravenous",
        "uses": "Hypertension and cardiovascular conditions"
    },
    {
        "name": "Metoprolol",
        "class": "Beta Blocker",
        "forms": "Tablet, Extended-Release Tablet, Injection",
        "routes": "Oral, Intravenous",
        "uses": "Hypertension and cardiovascular conditions"
    },
    {
        "name": "Losartan",
        "class": "Angiotensin Receptor Blocker",
        "forms": "Tablet",
        "routes": "Oral",
        "uses": "Hypertension"
    },
    {
        "name": "Telmisartan",
        "class": "Angiotensin Receptor Blocker",
        "forms": "Tablet",
        "routes": "Oral",
        "uses": "Hypertension"
    },
    {
        "name": "Enalapril",
        "class": "ACE Inhibitor",
        "forms": "Tablet, Injection",
        "routes": "Oral, Intravenous",
        "uses": "Hypertension and heart failure"
    },
    {
        "name": "Furosemide",
        "class": "Loop Diuretic",
        "forms": "Tablet, Oral Solution, Injection",
        "routes": "Oral, Intravenous, Intramuscular",
        "uses": "Edema and hypertension"
    },
    {
        "name": "Hydrochlorothiazide",
        "class": "Thiazide Diuretic",
        "forms": "Tablet, Capsule",
        "routes": "Oral",
        "uses": "Hypertension and edema"
    },
    {
        "name": "Spironolactone",
        "class": "Potassium-Sparing Diuretic",
        "forms": "Tablet, Oral Suspension",
        "routes": "Oral",
        "uses": "Edema and selected cardiovascular conditions"
    },
    {
        "name": "Atorvastatin",
        "class": "Statin",
        "forms": "Tablet",
        "routes": "Oral",
        "uses": "Dyslipidemia"
    },
    {
        "name": "Rosuvastatin",
        "class": "Statin",
        "forms": "Tablet",
        "routes": "Oral",
        "uses": "Dyslipidemia"
    },
    {
        "name": "Clopidogrel",
        "class": "Antiplatelet",
        "forms": "Tablet",
        "routes": "Oral",
        "uses": "Prevention of thrombotic cardiovascular events"
    },
    {
        "name": "Salbutamol",
        "class": "Bronchodilator",
        "forms": "Tablet, Syrup, Inhaler, Nebulizer Solution",
        "routes": "Oral, Inhalation",
        "uses": "Bronchospasm and asthma"
    },
    {
        "name": "Budesonide",
        "class": "Corticosteroid",
        "forms": "Inhaler, Nebulizer Suspension, Capsule",
        "routes": "Inhalation, Oral",
        "uses": "Respiratory and inflammatory conditions"
    },
    {
        "name": "Montelukast",
        "class": "Leukotriene Receptor Antagonist",
        "forms": "Tablet, Chewable Tablet, Granules",
        "routes": "Oral",
        "uses": "Asthma and allergic rhinitis"
    },
    {
        "name": "Cetirizine",
        "class": "Antihistamine",
        "forms": "Tablet, Syrup, Oral Solution",
        "routes": "Oral",
        "uses": "Allergic conditions"
    },
    {
        "name": "Loratadine",
        "class": "Antihistamine",
        "forms": "Tablet, Syrup",
        "routes": "Oral",
        "uses": "Allergic conditions"
    },
    {
        "name": "Fexofenadine",
        "class": "Antihistamine",
        "forms": "Tablet, Oral Suspension",
        "routes": "Oral",
        "uses": "Allergic conditions"
    },
    {
        "name": "Mupirocin",
        "class": "Topical Antibiotic",
        "forms": "Cream, Ointment",
        "routes": "Topical",
        "uses": "Local bacterial skin infections"
    },
    {
        "name": "Clotrimazole",
        "class": "Antifungal",
        "forms": "Cream, Lotion, Tablet, Vaginal Tablet",
        "routes": "Topical, Vaginal",
        "uses": "Fungal infections"
    },
    {
        "name": "Fluconazole",
        "class": "Triazole Antifungal",
        "forms": "Tablet, Capsule, Oral Suspension, Injection",
        "routes": "Oral, Intravenous",
        "uses": "Fungal infections"
    },
    {
        "name": "Acyclovir",
        "class": "Antiviral",
        "forms": "Tablet, Cream, Ointment, Injection",
        "routes": "Oral, Topical, Intravenous",
        "uses": "Herpes virus infections"
    },
    {
        "name": "Hydrocortisone",
        "class": "Corticosteroid",
        "forms": "Cream, Ointment, Tablet, Injection",
        "routes": "Topical, Oral, Intravenous",
        "uses": "Inflammatory and allergic conditions"
    }
]

EXCIPIENTS = {
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
        "Benzalkonium chloride"
    ],
    "Vehicle": [
        "Purified water",
        "Glycerin",
        "Propylene glycol"
    ],
    "Film former": [
        "Hypromellose",
        "Polyvinyl alcohol"
    ]
}


def safe_text(value):
    if isinstance(value, list):
        return " ".join(str(item) for item in value)
    return str(value) if value else "Not available"


@st.cache_data(ttl=86400, show_spinner=False)
def get_pubchem_data(drug_name):
    url = (
        "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/"
        + quote(drug_name)
        + "/property/MolecularFormula,MolecularWeight,"
        "CanonicalSMILES,IsomericSMILES/JSON"
    )

    try:
        response = requests.get(url, timeout=20)

        if response.status_code != 200:
            return {}

        properties = response.json()["PropertyTable"]["Properties"][0]

        return {
            "PubChem CID": properties.get("CID", "Not available"),
            "Molecular Formula": properties.get(
                "MolecularFormula", "Not available"
            ),
            "Molecular Weight": properties.get(
                "MolecularWeight", "Not available"
            ),
            "Canonical SMILES": properties.get(
                "ConnectivitySMILES", "Not available"
            ),
            "Isomeric SMILES": properties.get(
                "SMILES", "Not available"
            )
        }

    except Exception as error:
        return {"PubChem Error": str(error)}


@st.cache_data(ttl=86400, show_spinner=False)
def get_fda_data(drug_name):
    search_url = (
        "https://api.fda.gov/drug/label.json?"
        "search=openfda.generic_name:"
        + quote(drug_name.lower())
        + "&limit=1"
    )

    try:
        response = requests.get(search_url, timeout=20)

        if response.status_code != 200:
            return {
                "FDA Status": "No matching public label found"
            }

        result = response.json()["results"][0]

        return {
            "FDA Status": "Label found",
            "FDA Indications": safe_text(
                result.get("indications_and_usage")
            ),
            "FDA Warnings": safe_text(
                result.get("warnings")
            ),
            "FDA Dosage Text": safe_text(
                result.get("dosage_and_administration")
            ),
            "FDA Routes": safe_text(
                result.get("route")
            ),
            "FDA Manufacturers": safe_text(
                result.get("manufacturer_name")
            ),
            "FDA Label URL": "https://open.fda.gov/apis/drug/label/"
        }

    except Exception as error:
        return {"FDA Error": str(error)}


def find_drug(drug_name):
    for drug in DRUGS:
        if drug["name"] == drug_name:
            return drug
    return None


st.title("💊 Pharmaceutical Drug Database")

st.info(
    "This application is intended for educational and research use. "
    "Always verify information from current official product labels."
)

st.sidebar.header("Search Options")

search_text = st.sidebar.text_input(
    "Search drug name",
    placeholder="Example: Paracetamol"
)

if search_text:
    filtered_drugs = [
        drug for drug in DRUGS
        if search_text.lower() in drug["name"].lower()
    ]
else:
    filtered_drugs = DRUGS

drug_names = [drug["name"] for drug in filtered_drugs]

if not drug_names:
    st.error("No drug found.")
    st.stop()

selected_name = st.sidebar.selectbox(
    "Select a drug",
    drug_names
)

selected_drug = find_drug(selected_name)

st.header(selected_drug["name"])

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Drug class", selected_drug["class"])

with col2:
    st.metric("Routes", selected_drug["routes"])

with col3:
    st.metric("Dosage forms", len(
        selected_drug["forms"].split(",")
    ))

st.subheader("Basic Drug Information")

basic_data = pd.DataFrame(
    [
        ["API name", selected_drug["name"]],
        ["Therapeutic class", selected_drug["class"]],
        ["Common uses", selected_drug["uses"]],
        ["Possible dosage forms", selected_drug["forms"]],
        ["Routes", selected_drug["routes"]]
    ],
    columns=["Field", "Information"]
)

st.table(basic_data)

if st.button("Fetch API Data"):
    with st.spinner("Fetching PubChem and openFDA data..."):
        pubchem = get_pubchem_data(selected_name)
        fda = get_fda_data(selected_name)

    st.subheader("PubChem Chemical Properties")
    st.json(pubchem)

    st.subheader("openFDA Label Data")

    if "FDA Indications" in fda:
        st.write("#### Indications and Usage")
        st.write(fda["FDA Indications"])

        st.write("#### Warnings")
        st.write(fda["FDA Warnings"])

        st.write("#### Dosage and Administration")
        st.write(fda["FDA Dosage Text"])

        st.write("#### Routes")
        st.write(fda["FDA Routes"])

        st.write("#### Manufacturers")
        st.write(fda["FDA Manufacturers"])

        st.caption(
            "The displayed label information is retrieved from openFDA. "
            "Verify the current official label before relying on it."
        )
    else:
        st.warning(fda.get("FDA Status", "FDA data unavailable"))

st.subheader("Educational Excipient Categories")

excipient_rows = []

for category, materials in EXCIPIENTS.items():
    excipient_rows.append(
        {
            "Category": category,
            "Common examples": ", ".join(materials),
            "Selection note": (
                "Selection depends on API properties, dosage form, "
                "compatibility, stability and quality target."
            )
        }
    )

st.dataframe(
    pd.DataFrame(excipient_rows),
    use_container_width=True,
    hide_index=True
)

st.subheader("High-Level Development Workflow")

workflow = [
    "Preformulation study",
    "API-excipient compatibility assessment",
    "Dosage-form selection",
    "Excipient screening",
    "Laboratory formulation trials",
    "Evaluation of critical quality attributes",
    "Stability study",
    "Analytical method verification",
    "Documentation and regulatory review"
]

for step_number, step in enumerate(workflow, start=1):
    st.write(f"{step_number}. {step}")

st.subheader("References")

st.markdown(
    """
- [PubChem PUG REST](https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest-tutorial)
- [openFDA Drug Label API](https://open.fda.gov/apis/drug/label/)
- [openFDA API Documentation](https://open.fda.gov/apis/)
- [ICH Q8 Pharmaceutical Development](https://www.ema.europa.eu/en/documents/scientific-guideline/note-guidance-pharmaceutical-development_en.pdf)
"""
)

st.caption(
    "Educational application only. Not a prescribing, diagnostic or "
    "GMP manufacturing instruction system."
)
