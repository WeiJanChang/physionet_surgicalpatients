from typing import TypedDict


class AnesDict(TypedDict):
    caseid: str
    subjectid: str  # de-identified hospital ID of patient
    casestart: int  # sec
    caseend: int  # sec
    anestart: int  # sec, from casestart
    aneend: int  # sec, from casestart
    opstart: int  # sec, from casestart
    opend: int  # sec, from casestart
    adm: int  # sec, admission time from casestart
    dis: int  # sec, discharge time from casestart
    icu_days: int
    death_inhosp: int  # in-hospital mortality
    age: int
    sex: str
    height: int  # cm
    weight: int  # kg
    bmi: int  # kg/m2
    asa: int  # ASA classification
    emop: int  # binary, emergency operation
    department: str  # surgical depart.
    optype: str
    dx: str
    opname: str
    approach: str
    position: str
    ane_type: str
    preop_htn: int  # binary
    preop_dm: int  # binary
    preop_ecg: str
    preop_pft: str  # pulmonary function
    preop_hb: int  # g/dL
    preop_plt: int  # x1000/mcL
    preop_pt: int  # %
    preop_aptt: int  # sec
    preop_na: int  # mmol/L
    preop_k: int  # mmol/L
    preop_gluc: int  # mg/dL
    preop_alb: int  # g/dL
    preop_ast: int  # IU/L
    preop_alt: int  # IU/L
    preop_bun: int  # mg/dL
    preop_cr: int  # mg/dL
    preop_ph: int
    preop_hco3: int  # mmol/L
    preop_be: int  # mmol/L
    preop_pao2: int  # mmHg
    preop_paco2: int  # mmHg
    preop_sao2: int  # %
    cormack: str  # Cormack's grade
    airway: str  # airway toute
    tubesize: int
    dltubesize: str  # double lumen tube size
    lmasize: int  # LMA size
    iv1: str
    iv2: str
    aline1: str
    aline2: str
    cline1: str
    cline2: str
    intraop_ebl: int  # estimated blood loss, ml
    intraop_uo: int  # urine output, ml
    intraop_rbc: int  # RBC transfusion, Unit
    intraop_ffp: int
    intraop_ctystalloid: int  # ml
    intraop_colloid: int  # ml
    intraop_ppf: int  # propofol bolus, mg
    intraop_mdz: int  # midazolam, mg
    intraop_ftn: int  # fentanyl, mcg
    intraop_rocu: int  # Rocuronium, mg
    intraop_vecu: int  # Vecuronium, mg
    intraop_eph: int  # Ephedrine, mg
    intraop_phe: int  # Phenylephrine, mcg
    intraop_epi: int  # Epinephrine, mcg
    intraop_ca: int  # Calcium chloride, mg
