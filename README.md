**PMDG_Framework**
Code required to run PMDG on the BPIC 2013 Incident Management, CoSeLoG, and Traffic Fines Event Logs. 

<h1>Requirements </h1>

To run our framework, you will need a series of packages for Java and Python. We break down the requirements here based on the language.

<h3> Python Packages </h3>

<ul>
  <li>SciPy (https://www.scipy.org)</li>
  <li>PM4Py (https://pm4py.fit.fraunhofer.de)</li>
  <li>Pandas (https://pandas.pydata.org/)</li>
  <li>scikit-learn (https://scikit-learn.org/)</li>
</ul>

We are using Python 3.10 and cannot guarentee this will run on previous versions.

<h3> Java Packages </h3>

The ARX Framework has a list of requirements to run: https://arx.deidentifier.org/development/dependencies/

We recommend pulling their github repo and adding our code into the examples folder. 

The repo can be found here: https://github.com/arx-deidentifier/arx 
Documentation for ARX methods and tools can be found here: https://arx.deidentifier.org/wp-content/uploads/javadoc/current/api/index.html 

<h1>How to run PMDG </h1>
<h3> Each Component is broken down into a folder <h3>
<h3> Component 1: Control-Flow Vectorization </h3> Before we can apply k-anonymity to the trace variants, we need to select an alignment strategy.
In this work, we offer a naive and MSA vectorizations.

<h5> MSA Vectorization: Run get_traces_<b>LOG_NAME<b>.py depending on the log to convert the event names into a format that is usable for MSA. We use the open source tool, MAFFA for the MSA vectorization: https://mafft.cbrc.jp/alignment/software/. Once the traces are aligned, you can reconstruct the aligned trace variants using <b>LOG_NAME<b>_Clustering.py, respectively. Next these trace variants need to be passed to ARX for anonymization, then finally the log needs to be reconstructed using rewrite_traces_in_log.py. 

<h5> Naive Vectorization: First the encoding must be created using <b>Log_Name<b>_naive_encoding.py. Then we pass these variants to ARX and finally reconstruct the log using rewrite_traces_in_log.py. 


<h3> Component 2: Attribute Anonymization</h3> Now the attributes need to be selected within each trace variant. We do this based on length in <b>INSERT PY FILE FROM PC<b>. Next, we take these variants and run them in an ARX Java environment. The script is run using AnonymizeAttributes.java. Final these files are combined and passed back to our PM4Py environment to be rewritten into event logs.

<h3> Component 3: Applying Attribute Anonymization</h3> The ARX attribute anonymizations are applied to the event logs in rewrite_attributes.py and the privay-enhanced event log is then passed to various organizational mining applications. 

<h3> Component 4: Organizational Mining Experiments</h3> You can run the experiments for handovers and decision trees by running the scipts in the Experiments folder. These experiments are created using PM4PY, and the any additional documentation to run them can be found at https://pm4py.fit.fraunhofer.de. 

<h1> How to contact us </h1>
PACE was developed through a collaboration with San Diego State University and Humboldt-Universität zu Berlin. If you want to contact us, please email rhildebrant@sdsu.edu. 
