#!/bin/bash

mongoimport --db coder \
--collection users  \
--file ./mocking/test_data.json \
--jsonArray

mongoimport --db coder \
--collection languages \
--file ./mocking/test_data_lang.json \
--jsonArray