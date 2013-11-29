ageliaco.schoolsite
===================

Plone site customization package for upper secondary schools in Geneva, developed by the AGELIACO community.

Only tested on Plone 4.3 for now.

Dependencies
------------

- collective.makesitestructure: https://github.com/kamon/collective.makesitestructure
  Would be nice, later, to reduce the code there, and even remove that dependency, by using plone.api.

TODO
----

- More cleanup. [Immediate Term]
  We currently add groups/users which are really "test accounts", via the setupVarious import step,
  and it is a bit confusing to do things this way. 
  Instead, we could add a browser view for the Administrator to execute the creation of those accounts if needed.
  Once done, to simplify our code, remove the setupVarious import step altogether since it is the only thing it currently does.
  
- Update the CSS with more common rules for school sites. [Immediate Term]

- Add tests to the package. [Near Term]
