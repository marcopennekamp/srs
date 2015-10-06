#!/bin/bash

printf "exec(open('insert_data.py').read())" | python ../manage.py shell
