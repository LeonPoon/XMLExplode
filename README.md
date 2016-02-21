This project contains a XML exploder, so that you can put different parts of a
XML file into their own separate files.

Command Line Tools
==================

pydtsxplode
-----------

Try:

    python -m pydtsxplode -- /home/me/Package.dtsx /home/me/exploded

Then:

    find /home/me/exploded -type f -print0 | xargs -0 file