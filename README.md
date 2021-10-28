# Getting data from TMDB

Quick solution (hopefully) for COMP0035 students having issues accessing TMDB data.

There are a number of Python libraries designed to make accessing data from TMDB that you can use.

Alternatively you can also make HTTP requests using the [requests](https://docs.python-requests.org/en/latest/user/quickstart/#make-a-request) library.

This repo is just a quick demo combining the BFI data with the TMDB records.

There are two versions of the get_data method in get_tmdb_data.py, the first uses [tmdbv3api](https://github.com/AnthonyBloomer/tmdbv3api) and the second uses requests.

Add your TMDB v3 API Key to the code and try to run it.