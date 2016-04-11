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

You can use [src-test/test/res/pydtsxplode/dtsx/Package.dtsx](src-test/test/res/pydtsxplode/dtsx/Package.dtsx)
as a sample dtsx file.

dtsxdiff
--------

Produces a diff of 2 dtsx files. Explodes the xml inside the files before doing recursive diff, so that the ordering of
elements in the file does not matter. Also replaces UUIDs with something more real. Helps sanity a lot when trying to
find out why one package work and the other doesn't, or just to know if you are committing a dtsx with unintended
changes into source control.

Do:

    python -m dtsxdiff -- /home/me/Package1.dtsx /home/you/Package2.dtsx

You can redirect output into a diff file if you like. To try it out, diff the 2 packages in
[src-test](src-test/test/res/pydtsxplode/dtsx/) and see if you can understand what was changed.

Contribute
==========

If you fixed a bug/implemented a feature beneficial for everyone, please send me a pull
request.
    
If you have an idea/suggestion, feel free to drop me a mail/message.

Licence
=======

> Copyright 2016 Leon Poon and Contributors
>
> Licensed under the Apache License, Version 2.0 (the "License");
> you may not use this file except in compliance with the License.
> You may obtain a copy of the License at
>
>    http://www.apache.org/licenses/LICENSE-2.0
>
> Unless required by applicable law or agreed to in writing, software
> distributed under the License is distributed on an "AS IS" BASIS,
> WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
> See the License for the specific language governing permissions and
> limitations under the License.
