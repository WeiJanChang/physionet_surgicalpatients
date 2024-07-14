/* TODO: need to modified type of age due to >89 ??*/
/* CDISC SDTM 3.2.1 Subject Demographics Domain(DM) Variables Demographics Domain*/
data surg.clinical_data;
	set surg.clinical_data;
	rename caseid=USUBJID subjectid=SUBJID opname=OPDECOD dx=OPEVDTYP 
		casestart=RFSTDTC caseend=RFENDTC anestart=RFXSTDTC aneend=RFXENDTC 
		opstart=RFCSTDTC opend=RFCENDTC;
		
run;

%macro rename_vars(input=, output=);

    data &output.;
        set &input.;
        rename caseid=USUBJID 
               subjectid=SUBJID 
               opname=OPDECOD 
               dx=OPEVDTYP 
               casestart=RFSTDTC 
               caseend=RFENDTC 
               anestart=RFXSTDTC 
               aneend=RFXENDTC 
               opstart=RFCSTDTC 
               opend=RFCENDTC;
    run;

%mend rename_vars;

/* Call the macro with appropriate parameters */
%rename_vars(input=surg.clinical_data, output=surg.clinical_data);


data surg.dm;
	set surg.clinical_data;
	drop intraop_ca intraop_colloid intraop_crystalloid intraop_ebl intraop_eph 
		intraop_epi intraop_ffp intraop_ftn intraop_mdz intraop_phe intraop_ppf 
		intraop_rbc intraop_rocu intraop_uo intraop_vecu preop_alb preop_alt 
		preop_aptt preop_ast preop_be preop_bun preop_cr preop_ecg preop_gluc 
		preop_hb preop_hco3 preop_k preop_na preop_paco2 preop_pao2 preop_pft 
		preop_ph preop_plt preop_pt preop_sao2;
run;

/*CDISC SDTM 3.1.3 The Findings Observation Class */
data surg.LBdomain;
	set surg.clinical_data;
	drop RFSTDTC RFENDTC RFXSTDTC RFXENDTC RFCSTDTC RFCENDTC adm ane_type approach 
		aline2 aline1 airway age asa bmi cline1 cline2 cormack death_inhosp 
		department dis dltubesize emop height icu_days iv1 iv2 lmasize optype 
		position sex tubesize weight OPDECOD OPEVDTYP preop_htn preop_dm;
run;

/* SDTM dataset */
/* --STRESC: character; --STRESN: numeric */
proc transpose data=surg.LBdomain 
		out=surg.LBdomain_SDTM_num(rename=(_NAME_=LBTESTCD COL1=LBSTRESN));
	by USUBJID;
	copy SUBJID;
	var preop_ecg preop_pft intraop_ca intraop_colloid intraop_crystalloid 
		intraop_ebl intraop_eph intraop_epi intraop_ffp intraop_ftn intraop_mdz 
		intraop_phe intraop_ppf intraop_rbc intraop_rocu intraop_uo intraop_vecu 
		preop_alb preop_alt preop_aptt preop_ast preop_be preop_bun preop_cr 
		preop_gluc preop_hb preop_hco3 preop_k preop_na preop_paco2 preop_pao2 
		preop_ph preop_plt preop_pt preop_sao2;
run;

/* --NRIND: "Y", "N"; "HIGH", "LOW";"NORMAL", "ABNORMAL" */
proc transpose data=surg.LBdomain 
		out=surg.LBdomain_SDTM_nr(rename=(_NAME_=LBTESTCD COL1=LBNRIND));
	by USUBJID;
	copy SUBJID;
	var preop_ecg preop_pft intraop_ca intraop_colloid intraop_crystalloid 
		intraop_ebl intraop_eph intraop_epi intraop_ffp intraop_ftn intraop_mdz 
		intraop_phe intraop_ppf intraop_rbc intraop_rocu intraop_uo intraop_vecu 
		preop_alb preop_alt preop_aptt preop_ast preop_be preop_bun preop_cr 
		preop_gluc preop_hb preop_hco3 preop_k preop_na preop_paco2 preop_pao2 
		preop_ph preop_plt preop_pt preop_sao2;
run;

/* add unit column. --STRESU: Standard Units*/
data surg.LBdomain_sdtm;
	merge surg.LBdomain_SDTM_num surg.LBdomain_SDTM_nr;
	by USUBJID;
	length LBSTRESU $20;

	if LBTESTCD in ('preop_hb', 'preop_alb') then do;
			LBSTRESU='g/dL';
		end;
	else if LBTESTCD='preop_plt' then do;
			LBSTRESU='x1000/mcL';
		end;
	else if LBTESTCD in ('preop_pt', 'preop_sao2') then do;
			LBSTRESU='%';
		end;
	else if LBTESTCD='preop_aptt' then do;
			LBSTRESU='sec';
		end;
	else if LBTESTCD in ('preop_na', 'preop_k', 'preop_hco3', 'preop_be') then do;
			LBSTRESU='mmol/L';
		end;
	else if LBTESTCD in ('preop_gluc', 'preop_bun', 'preop_cr') then
		do;
			LBSTRESU='mg/dL';
		end;
	else if LBTESTCD in ('preop_ast', 'preop_alt') then do;
			LBSTRESU='IU/L';
		end;
	else if LBTESTCD in ('preop_pao2', 'preop_paco2') then do;
			LBSTRESU='mmHg';
		end;
	else if LBTESTCD in ('intraop_ebl', 'intraop_uo', 'intraop_crystalloid', 
		'intraop_colloid') then do;
			LBSTRESU='ml';
		end;
	else if LBTESTCD in ('intraop_rbc', 'intraop_ffp') then do;
			LBSTRESU='Unit';
		end;
	else if LBTESTCD in ('intraop_ppf', 'intraop_mdz', 'intraop_rocu', 
		'intraop_vecu', 'intraop_eph', 'intraop_ca') then do;
			LBSTRESU='mg';
		end;
	else if LBTESTCD in ('intraop_ftn', 'intraop_phe', 'intraop_epi') then do;
			LBSTRESU='mcg';
		end;
	else do;
			LBSTRESU='';
		end;
run;
