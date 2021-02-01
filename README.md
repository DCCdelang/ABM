# Epstein Civil Violence Model with an Media and Social Media component

# ABM project of Dante de Lang, Louky Schutten, Caterina Buranelli, Ignas Krikštaponis and Kamiel Gulpen

## The model

The model is an extension of Epstein's civil violence model. Similar to Lemos et al. We broaden Epstein's Model with a delay in time before agents are imprisoned, representing the fighting time prior to an arrest and a feedback mechanism that allows the legitimacy to vary as a function of the number of arrests and violent episodes.
The purpose of the model is to introduce a network representing social media contacts in the extended version of the ABM of civil violence of Epstein. 

## How to Run

This repository contains 2 models, one model with a network which is in the ``epstein_civil_violence_Normal+Network Grid`` folder and one model without a network, which can be found in the ``epstein_civil_violence_NormalGrid`` folder. To run the model one must first choose which model he/she wants to run. 

The model can then be played by executing: ``run.py`` in this directory. e.g.

```
    $ python model_run.py
``` 

Then open your browser to [http://127.0.0.1:8521/](http://127.0.0.1:8521/) and press Reset, then Run. 


![GitHub Logo](\epstein_civil_violence_Normal+Network Grid\Images\Model.png)
Format: ![Alt Text](url)


This shows how the agents move in the grid as shown above. The red dots represent the active citizens, the green dots the fighting citizens and the blue dots the quiscent citizens. The small black dots are the cops.

## Files

* ``EpsteinCivilViolence.py``: Core model and agent code.
* ``EpsteinCivilViolenceServer.py``: Sets up the interactive visualization.
* ``Epstein Civil Violence.ipynb``: Jupyter notebook conducting some preliminary analysis of the model.

## Further Reading

This model is based adapted from:

[Epstein, J. “Modeling civil violence: An agent-based computational approach”, Proceedings of the National Academy of Sciences, Vol. 99, Suppl. 3, May 14, 2002](http://www.pnas.org/content/99/suppl.3/7243.short)

A similar model is also included with NetLogo:

Wilensky, U. (2004). NetLogo Rebellion model. http://ccl.northwestern.edu/netlogo/models/Rebellion. Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.
