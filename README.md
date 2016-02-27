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
    
Contribute
==========

If you fixed a bug/implemented a feature beneficial for everyone, send me a pull
request.
    
If you have an idea/suggestion, please drop me a mail/message.

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
