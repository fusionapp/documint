=================================================
Documint: Document rendering service (deprecated)
=================================================

.. attention::
   This software is deprecated in favour of the more functional HTTP version,
   `clj-documint`_.

.. _clj-documint: https://github.com/fusionapp/clj-documint

Quick start
-----------

Install the software:

.. code-block:: shell

   $ pip install documint

Create a Java keystore (for the ``Certify`` command):

.. code-block:: shell
   $ keytool -genkey -keyalg RSA \
             -alias ssl \
             -keystore documint_keystore_dev.jks \
             -validity 3650 \
             -keysize 2048

Run the software:

.. code-block:: shell

   $ twistd -n documint --pidfile '' \
            --keystore documint_keystore.jks \
            --password 123456 \          # From the `keytool` interaction.
            --privateKeyPassword 123456  # From the `keytool` interaction.
