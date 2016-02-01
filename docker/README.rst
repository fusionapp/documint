Building the Documint Docker container
======================================

Documint is built off of the standard fusionapp/base container.

Build process
-------------

1. Pull

   .. code-block:: shell-session

      $ docker pull fusionapp/base

2. Run the base container to build the necessary wheels.

   .. code-block:: shell-session

      $ docker run --rm -ti -v "${PWD}:/application" -v "${PWD}/wheelhouse:/wheelhouse" fusionapp/base

   The built wheels will be placed in the "wheelhouse" directory at the root
   of the repository.

3. Copy the clj-neon uberjar wheel into bin.

   .. code-block:: shell-session

      $ cp .../clj-neon/target/uberjar/clj-neon-*-standalone.jar bin/clj-neon.jar

4. Place any needed fonts in fonts/.

5. Build the Documint container.

   .. code-block:: shell-session

      $ docker build --tag=fusionapp/documint --file=docker/documint.docker .

You only need to rerun steps 2 and 5 to build a container from modified source.
