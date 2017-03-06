tablebar
========

.. code-block:: console

    usage: micca tablebar [-h] -i FILE -o FILE [-r] [-t N] [--xticklabelsize SIZE]
                        [-f {pgf,ps,svg,rgba,raw,svgz,pdf,eps,png}]

    micca tablebar generates a relative abundance bar plot from
    OTU or taxa tables. The table must be an OTU/taxon x sample,
    TAB-separated file (see 'micca otu').

    optional arguments:
    -h, --help            show this help message and exit

    arguments:
    -i FILE, --input FILE
                            input OTU table file (required).
    -o FILE, --output FILE
                            output image file (required).
    -r, --raw             plot raw values (i.e. counts) instead of relative
                            abundances.
    -t N, --topn N        plot the top N abundant taxa (default 12).
    --xticklabelsize SIZE
                            x tick label size (default 8).
    -f {pgf,ps,svg,rgba,raw,svgz,pdf,eps,png}, --format {pgf,ps,svg,rgba,raw,svgz,pdf,eps,png}
                            output file format (default png).

    Example

        micca tablebar -i otutable.txt -o otutable_plot.png
