/* Benefits of Frequency Reports in Clinical Trials:
1. Identifying Patterns: Helps in identifying common patterns and trends across 
different surgeries, which can be crucial for understanding practice standards and deviations.

2. Quality Control: Assists in monitoring and ensuring consistency in 
how surgeries are categorized and reported, which is vital for maintaining high data quality.

3. Operational Efficiency: By understanding the most frequent types of operations or 
anesthesia used, hospitals can optimize resource allocation and staff training.

4. Safety Monitoring: Frequent analysis of specific surgical approaches and positions 
can help identify potential safety issues, leading to improvements in patient care. */

ODS PDF FILE = "&output_path/surgical_freq.pdf" STYLE = Journal;
title "Surgical Data Analysis";
title2 "Frequency Report for surgery";
proc freq data=surg.clinical_data order=freq;
	tables department optype ane_type approach position/ nocum;
run;

/* Create graphics */
ODS GRAPHICS ON;
ODS noproctitle;
title "Frequency Report in Each Department";
PROC FREQ data = surg.clinical_data order=freq;
	tables department / nocum plots=freqplot;
run;
title;

title "Frequency Report in operation type";
PROC FREQ data = surg.clinical_data order=freq;
	tables optype / nocum plots=freqplot;
run;
title;

title "Frequency Report in anesthesia type";
PROC FREQ data = surg.clinical_data order=freq;
	tables ane_type*position / nocum plots=freqplot;
run;
title;

ODS proctitle;
ODS GRAPHICS OFF;

ODS PDF CLOSE;


/* To identify which departments have more patients with longer ICU stays, 
in order to address potential safety issues and improve patient care */
ODS PDF FILE= "&output_path/surgical_avg_icu.pdf" STYLE = Journal;
%let inde_var = ane_type;
title "Surgical Data Analysis";
title2 "Average ICU Days in &inde_var";

proc sql;
    create table AvgICU as
    select &inde_var, 
           mean(icu_days) as Avg_ICU_Days
    from surg.clinical_data
    group by &inde_var
    order by Avg_ICU_Days;
    select * from AvgICU;
quit;

ODS PDF CLOSE;


