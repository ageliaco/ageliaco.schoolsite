ageliaco.schoolsite
===================

Plone site customization package for upper secondary schools in Geneva, developed by the AGELIACO community.

Only tested on Plone 4.3 for now.

Dependencies
------------

- plone.app.contenttypes.

TODO
----

- Specific to DIP
  * Impressum link on image in the header: Use Plone registry to store the impressum page URL 
    which is different for each school.

- Re-work footer content implementation: Either simply use Products.Doormat or create "Site Administration" contents, 
  such as those used to provide the footer blocks, introduce and use a Dexterity content type which fields 
  are not searchable. Thus avoiding those to appear in search results.

- Add tests to the package. [Near Term]

