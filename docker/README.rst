Building the Documint Docker container
======================================

There are three Docker containers defined: run.docker defines the actual
container used to run Documint, build.docker is used to build the wheels required
for the "run" container, and base.docker is used to define a base container
which is shared between the "build" and "run" containers as an optimization.

Build process
-------------

1. Build the base container.

   .. code-block:: shell-session

      $ docker build -t fusionapp/documint-base -f docker/base.docker .

2. Build the build container.

   .. code-block:: shell-session

      $ docker build -t fusionapp/documint-build -f docker/build.docker .

3. Run the build container to build the necessary wheels.

   .. code-block:: shell-session

      $ docker run --rm -ti -v "${PWD}:/application" -v "${PWD}/wheelhouse:/wheelhouse" fusionapp/documint-build

   The built wheels will be placed in the "wheelhouse" directory at the root
   of the repository. This is necessary for building the final container.

4. Copy the clj-neon uberjar wheel into bin.

   .. code-block:: shell-session

      $ cp .../clj-neon/target/uberjar/clj-neon-*-standalone.jar bin/clj-neon.jar

5. Place any needed fonts in fonts/.

6. Build the run container.

   .. code-block:: shell-session

      $ docker build -t fusionapp/documint -f docker/run.docker .

You only need to rerun steps 3 and 6 to build a container from modified source.
