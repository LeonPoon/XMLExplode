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
    
Contribute
==========

If you fixed a bug/implemented a feature beneficial for everyone, send me a pull
request.
    
Licence
=======

> Copyright (C) 2016 Leon Poon and Contributors
> 
> This program is free software: you can redistribute it and/or modify
> it under the terms of the GNU General Public License as published by
> the Free Software Foundation, either version 3 of the License, or
> (at your option) any later version.
> 
> This program is distributed in the hope that it will be useful,
> but WITHOUT ANY WARRANTY; without even the implied warranty of
> MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
> GNU General Public License for more details.
> 
> You should have received a copy of the [GNU General Public License](LICENSE)
> along with this program.  If not, see <[http://www.gnu.org/licenses/](http://www.gnu.org/licenses/)>