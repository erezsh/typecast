# Typecast: Cast-Oriented programming

Typecast is an experimental python library for defining casts (transformations) between different classes.

Casts:
* Defined as Type1 -> Type2
* Are applied to instances (in this example, instances of Type1)
* Connect into cast-chains (shortest path is chosen)

In order to demonstrate the power and usefulness of this mechanism, let's look at a few case studies:

## Case study 1: Time units

Typecasts library comes with time units which allow you to convert between different units:

    >>> from typecast.lib.time import Seconds, Minutes, Hours, Days, Weeks
    >>> Minutes(60) >> Seconds
    Seconds(3600)
    >>> Hours(60) >> Days
    Days(2.5)

You can cast from any unit to any unit. However, the library doesn't implement O(n!) of casts. Every unit can cast to and from Seconds, and the chaining mechanism lets us get away with only O(n) cast implementations.

Let's have a better look at chaining, when we try to add a new Fortnight class.

    >>> from typecast import Typecast
    >>>
    >>> class Fortnights(metaclass=Typecast):
    >>>     def __init__(self, fortnights):
    >>>         self.fortnights = fortnights
    >>>     def to__Weeks(self, cls):
    >>>         return cls(self.fortnights * 2)
    >>>
    >>>  Fortnights(2) >> Days
    Days(28)
    >>>  Fortnights(2) >> Hours
    Hours(672)

The *to\_\_* prefix is special to the Typecast metaclass.

Notice how the chaining mechanism automatically lets us cast to days, even though we only defined a cast to weeks. We could have chosen any unit (Hours, Seconds, etc.) and it would just work.

(Of course, to cast into Fortnights we'll also have to define a from\_\_ cast)

Another little benefit of these units is using operations on them:

    >>>  Hours(1) + Minutes(30)
    Hours(1.5)
    >>>  Days(1) < Minutes(800)
    False
    >>>  Days(1) <= Minutes(2000)
    True

## Case study 2: HTML & type-safety

The typecast library defines a HTML type, with a few basic casts:

    >>> from typecast.lib.web import HTML
    >>>
    >>>  HTML << 'a < b'
    HTML('a &lt; b')
    >>>  HTML << ['a', 'b']
    '<ol>\n<li>a</li>\n<li>b</li>\n</ol>'

Notice that we can be confident that a HTML type is safe to insert into a html document.

Another feature of typecast, called "autocast", allows us to write safe operations on html without much effort:

    >>> from typecast import autocast
    >>>
    >>> @autocast
    >>> def div(html: HTML):
    >>>     return HTML(f'<div>{html.html}</div>')
    >>>
    >>>  div(div('use <b>to emphasize</b>'))
    HTML('<div><div>use &lt;b&gt;to emphasize&lt;/b&gt;</div></div>')

Typecast lets us have html correctness, without having to worry about stacking operations.

Of course, it's possible to define new casts (from database objects?) and chain them if necessary.

# Support

Typecast works on all versions of Python 3. (autocast relies on annotations)

If there's enough demand, I will make it work for Python 2 too.

# Installation

...

# How to contribute

If you want to contribute the typecast's lib of classes, or have ideas on how I can improve typecast, please let me know!

