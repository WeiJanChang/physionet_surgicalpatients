/* To import the CSV file into a SAS dataset*/
PROC IMPORT 
		DATAFILE="/home/u63831316/physionet_surgicalpatients/clinical_data.csv" 
		DBMS=CSV OUT=surg.clinical_data
		/*     DBMS(Database Management System). This can be CSV/EXCEL/XLSX, etc */
		REPLACE;
	/* REPLACE: if work.clinical_data already there, the new one will replace it*/
RUN;