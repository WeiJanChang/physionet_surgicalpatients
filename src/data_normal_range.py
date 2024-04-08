__all__ = {'DATA_NORMAL_RANGE'}, ["extract_values"]

DATA_NORMAL_RANGE = {
    "preop_ecg": 'Normal Sinus Rhythm',  # type:str
    "preop_pft": 'Normal',  # type: str
    "preop_hb": (13, 17),  # type: int  # g/dL
    "preop_plt": (130, 400),  # type: int  # x1000/mcL
    "preop_pt": (80, 120),  # type: int  # %
    "preop_aptt": (26.7, 36.6),  # type: int  # sec
    "preop_na": (135, 145),  # type: int  # mmol/L
    "preop_k": (3.5, 5.5),  # type: int  # mmol/L
    "preop_gluc": (70, 110),  # type: int  # mg/dL
    "preop_alb": (3.3, 5.2),  # type: int  # g/dL
    "preop_ast": (1, 40),  # type: int  # IU/L
    "preop_alt": (1, 40),  # type: int  # IU/L
    "preop_bun": (10, 26),  # type: int  # mg/dL
    "preop_cr": (0.70, 1.40),  # type: int  # mg/dL
    "preop_ph": (7.35, 7.45),  # type: int
    "preop_hco3": (18, 23),  # type: int  # mmol/L
    "preop_be": (-2.0, 3.0),  # type: int  # mmol/L
    "preop_pao2": (83, 108),  # type: int  # mmHg
    "preop_paco2": (35, 48),  # type: int  # mmHg
    "preop_sao2": (95, 98),  # type: int  # %
}


def extract_values(dictionary):
    preop_ecg = dictionary.get('preop_ecg')
    preop_pft = dictionary.get('preop_pft')
    preop_hb = dictionary.get('preop_hb')
    preop_plt = dictionary.get("preop_plt")
    preop_pt = dictionary.get("preop_pt")
    preop_aptt = dictionary.get("preop_aptt")
    preop_na = dictionary.get("preop_na")
    preop_k = dictionary.get("preop_k")
    preop_gluc = dictionary.get("preop_gluc")
    preop_alb = dictionary.get('preop_alb')
    preop_ast = dictionary.get('preop_ast')
    preop_alt = dictionary.get('preop_alt')
    preop_bun = dictionary.get('preop_bun')
    preop_cr = dictionary.get('preop_cr')
    preop_ph = dictionary.get('preop_ph')
    preop_hco3 = dictionary.get('preop_hco3')
    preop_be = dictionary.get('preop_be')
    preop_pao2 = dictionary.get('preop_pao2')
    preop_paco2 = dictionary.get('preop_paco2')
    preop_sao2 = dictionary.get('preop_sao2')
    return (preop_ecg, preop_pft, preop_hb, preop_plt, preop_pt, preop_aptt, preop_na,
            preop_k, preop_gluc, preop_alb, preop_ast, preop_alt, preop_bun, preop_cr,
            preop_ph, preop_hco3, preop_be, preop_pao2, preop_paco2, preop_sao2)
