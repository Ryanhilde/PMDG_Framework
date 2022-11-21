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

<h4> Part 1: Control-Flow Vectorization </h4> Start with loading the files in Component 1 into an IDE. Select the event log you would like to anonymize and the K parameter inside of ApplyK.py.
Run this code and specify the output file to write the log to.

<h4> Part 2: Attribute Anonymization</h4> Plug the ARX files into a Java environment with ARX's specified dependencies (see **Requirements**). Each file must be individually run with the specified K vlaue. 

<h4> Part 3: Applying Attribute Anonymization</h4> For each attribute, you will need to run Anonymize_BLANK_File.py twice within the Compoenent 3 folder. The first time we grab the required attributes from the control-flow anonymized event log and the second run will overwrite their values and reconstruct the log. The first run needs to call the encode_log() method, while the second run needs to call the apply_privacy() method. 

<h4> Part 4: Organizational Mining Experiments</h4> You can run the experiments for handovers and decision trees by running the scipts in the Experiments folder. These experiments are created using PM4PY, and the any additional documentation to run them can be found at https://pm4py.fit.fraunhofer.de. 

<h1> How to contact us </h1>
PACE was developed through a collaboration with San Diego State University and Humboldt-Universität zu Berlin. If you want to contact us, please email rhildebrant@sdsu.edu. 
