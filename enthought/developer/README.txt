This package contains a number of useful developer-oriented tools that can aid
in developing, testing and debugging Traits and Envisage based applications.

As such, the tools are intended to be included as plugins within an
Envisage-based application that is being developed or debugged.

The 'plugin_definition.py' file contains the necessary Envisage plugin
definitions needed to add all of the tools and their associated DockWindow
features to an Envisage application. Simply include a reference to the file
in your application's main plugin definitions file to make all of the tools
available within your application.

Besides adding the developer tools, the plugin definition file will also add
a new "Developer Tools" perspective to your application, as well as a
"Developer Tools" top-level menu section to your application menu bar. Refer to
the documentation for more information on how to use the tools and added menu
options.

If you do not need access to all of the tools in the package, simply:
  - Copy the plugin_definition.py file.
  - Remove the unnecessary tool plugin definitions from the copied file.
  - Reference the copied file in your application's main plugin definitions
    file instead of the original 'plugin_definition.py' file.

If you want to quickly see the tools in action, we have provided a demo in the
source's examples directory.  This example is an Envisage application
containing only a single 'Developer Tools' perspective which will initially
contain only a few of the developer plugins.

If you encounter any problems or have any questions about how to use the tools,
please post or ask them on the enthought-dev mailing list. Additionally, you
should also feel to report problems by creating 'tickets' on the enthought.com
Trac system.
