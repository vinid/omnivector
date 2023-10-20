==========
OmniVector
==========


.. image:: https://img.shields.io/pypi/v/omnivector.svg
        :target: https://pypi.python.org/pypi/omnivector

.. image:: https://img.shields.io/travis/vinid/omnivector.svg
        :target: https://travis-ci.com/vinid/omnivector

.. image:: https://readthedocs.org/projects/omnivector/badge/?version=latest
        :target: https://omnivector.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status




OmniVector provides a simple interface to vector databases. We integrate the main functionalities of different vector dbs,
generally indexing and searching, into a single interface. This allows us to easily switch between different vector dbs.


.. code-block:: python

    db = WeaviateDB()  # or PineconeDB() or LanceDB()

    encoder = SentenceTransformerEmbedder("paraphrase-MiniLM-L6-v2", device="cpu")
    docs = ["the cat is on the table", "the table is on the cat", "the dog is mining bitcoins"]


    ids = list(range(4, len(docs) + 4))
    embeddings = encoder.embed(docs)

    db.create_index(ids, docs, embeddings)

    search_vector = encoder.embed(["the dog is mining bitcoins"])[0]
    print(db.vector_search(search_vector, k=1))

* Free software: MIT license
* Documentation: https://omnivector.readthedocs.io.


Features
--------

* The AbstractDB requires setting OMNIVECTOR_CONFIG env variable to a config file (an example is in config.yaml)

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
