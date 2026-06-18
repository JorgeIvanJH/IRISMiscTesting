# Global Reference API

This section provides API documentation for the methods of the `gref` class of the InterSystems IRIS Python Module. These methods allow you to access and manipulate InterSystems IRIS globals.

## Summary

The following table summaries the methods of the `gref` class of the InterSystems IRIS Python Module. To use this class from Embedded Python, first do `import iris`, and then use the `iris.gref()` function to obtain a reference to a global. (See iris.gref().)

<table><tr><th>Group</th><th>Settings</th></tr><tr><td>Work on a Node of a Global</td><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GEPYTHON_reference_gref#GEPYTHON_reference_gref_data">data()</a>, <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GEPYTHON_reference_gref#GEPYTHON_reference_gref_get">get()</a>, <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GEPYTHON_reference_gref#GEPYTHON_reference_gref_getasbytes">getAsBytes()</a>, <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GEPYTHON_reference_gref#GEPYTHON_reference_gref_kill">kill()</a>, <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GEPYTHON_reference_gref#GEPYTHON_reference_gref_set">set()</a></td></tr><tr><td>Traverse a Global</td><td><a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GEPYTHON_reference_gref#GEPYTHON_reference_gref_keys">keys()</a>, <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GEPYTHON_reference_gref#GEPYTHON_reference_gref_order">order()</a>, <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GEPYTHON_reference_gref#GEPYTHON_reference_gref_orderiter">orderiter()</a>, <a href="https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=GEPYTHON_reference_gref#GEPYTHON_reference_gref_query">query()</a></td></tr></table>

For background information on globals, see Introduction to Globals.

## data(key)

Checks if a node of a global contains data and/or has descendants. The `key` of the node is passed as a list. Passing a key with the value None (or an empty list) indicates the root node of the global.

You can use `data()` to inspect a node to see if it contains data before attempting to access that data and possibly encountering an error. The method returns 0 if the node is undefined (contains no data), 1 if the node is defined (contains data), 10 if the node is undefined but has descendants, or 11 if the node is defined and has descendants.

Assume you have a global `^a` with the following contents:

```
^a(2) = "two"
^a(3,1) = "three one"
^a(4) = "four"
^a(4,1) = "four one"
```

Then you can use `data()` to test the various nodes of the global as in these examples:

```
>>> a = iris.gref('^a')
>>> a.data([1])
0
>>> a.data([2])
1
>>> a.data([3])
10
>>> a.data([4])
11
>>> a.data([None])
10
>>> a.data([3,1])
1
```

You can use modulo 2 arithmetic to check whether a node contains data, regardless of whether it has descendants or not.

```
>>> a.data([3]) % 2
0
>>> a.data([4]) % 2
1
```

## get(key)

Gets the value stored at a node of a global. The `key` of the node is passed as a list. Passing a key with the value None (or an empty list) indicates the root node of the global.

Assume you have a global `^a` with the following contents:

```
^a(2) = "two"
^a(3,1) = "three one"
^a(4) = "four"
^a(4,1) = "four one"
```

Then you can use `get()` to retrieve data from the various nodes of the global as in these examples:

```
>>> a = iris.gref('^a')
>>> a.get([2])
'two'
>>> a.get([3,1])
'three one'
```

Alternatively, you can get the value of a node directly, as you would for a Python dictionary, or you can use the dunder method `__getitem__()`.

```
>>> a[3,1]
'three one'
>>> a.__getitem__([3,1])
'three one'
```

Using `get()` to get data from a node that is undefined returns None.

```
>>> x = a.get([5])
>>> print(x)
None
```

See also getAsBytes().

## getAsBytes(key)

Gets a string value stored at a node of a global and converts it to the Python bytes data type. The `key` of the node is passed as a list. Passing a key with the value None (or an empty list) indicates the root node of the global.

Assume you have a global `^a` with the following contents:

```
^a(2) = "two"
^a(3,1) = "three one"
^a(4) = "four"
^a(4,1) = "four one"
```

Then you can use `getAsBytes()` to retrieve data from the various nodes of the global as in these examples:

```
>>> a = iris.gref('^a')
>>> a.getAsBytes([2])
b'two'
>>> a.getAsBytes([3,1])
b'three one'
```

Using `getAsBytes()` to get data from a node that is undefined returns None.

```
>>> x = a.getAsBytes([5])
>>> print(x)
None
```

See also get().

## keys(key)

Returns the keys of a global, starting from a given key. The starting `key` is passed as a list. Passing an empty list indicates the root node of the global.

Assume you have a global `^mlb` with the following contents:

```
^mlb = "Major League Baseball"
^mlb("AL") = "American League"
^mlb("AL","Central") = "AL Central"
^mlb("AL","East") = "AL East"
^mlb("AL","East",1) = "Baltimore"
^mlb("AL","East",2) = "Boston"
^mlb("AL","East",3) = "NY Yankees"
^mlb("AL","East",4) = "Tampa Bay"
^mlb("AL","East",5) = "Toronto"
^mlb("AL","West") = "AL West"
^mlb("AL","West",1) = "Houston"
^mlb("AL","West",2) = "LA Angels"
^mlb("AL","West",3) = "Oakland"
^mlb("AL","West",4) = "Seattle"
^mlb("AL","West",5) = "Texas"
^mlb("NL") = "National League"
```

You can use `keys()` to get the keys of the global and print out their values, as follows:

```
>>> m = iris.gref('^mlb')
>>> for key in m.keys([]):
...     value = m[key]
...     print(f'{key} = {value}')
...
['AL'] = American League
['AL', 'Central'] = AL Central
['AL', 'East'] = AL East
['AL', 'East', '1'] = Baltimore
['AL', 'East', '2'] = Boston
['AL', 'East', '3'] = NY Yankees
['AL', 'East', '4'] = Tampa Bay
['AL', 'East', '5'] = Toronto
['AL', 'West'] = AL West
['AL', 'West', '1'] = Houston
['AL', 'West', '2'] = LA Angels
['AL', 'West', '3'] = Oakland
['AL', 'West', '4'] = Seattle
['AL', 'West', '5'] = Texas
['NL'] = National League
```

Note that the starting key does not have to exist as a node in the global. Since a global is stored in sorted order, `keys()` begins with the key of the next node according to the sort order, for example:

```
>>> m = iris.gref('^mlb')
>>> for key in m.keys(['AL','North']):
...     value = m[key]
...     print(f'{key} = {value}')
...
['AL', 'West'] = AL West
['AL', 'West', '1'] = Houston
['AL', 'West', '2'] = LA Angels
['AL', 'West', '3'] = Oakland
['AL', 'West', '4'] = Seattle
['AL', 'West', '5'] = Texas
['NL'] = National League
```

You can also use get() to retrieve the value of each node, but you need to test each node first by using data() to make sure it is contains data.

Use order() to traverse the nodes at one level of a global.

## kill(key)

Deletes the node of a global, if it exists. The `key` of the node is passed as a list. This also deletes any descendants of the node. Passing a key with the value None (or an empty list) indicates the root node of the global.

Assume you have a global `^a` with the following contents:

```
^a(2) = "two"
^a(3,1) = "three one"
^a(4) = "four"
^a(4,1) = "four one"
```

Then you can use `kill()` to kill a node of the global, and its descendants, as in this example:

```
>>> a = iris.gref('^a')
>>> a.kill([4])
```

Now the global has the following contents:

```
^a(2) = "two"
^a(3,1) = "three one"
```

Passing None for the key kills the entire global.

```
>>> a.kill([None])
```

## order(key)

Returns the next key in that level of the global, starting from a given key. The starting `key` is passed as a list. If no key follows the starting key, `order()` returns None.

Assume you have a global `^mlb` with the following contents:

```
^mlb = "Major League Baseball"
^mlb("AL") = "American League"
^mlb("AL","Central") = "AL Central"
^mlb("AL","East") = "AL East"
^mlb("AL","East",1) = "Baltimore"
^mlb("AL","East",2) = "Boston"
^mlb("AL","East",3) = "NY Yankees"
^mlb("AL","East",4) = "Tampa Bay"
^mlb("AL","East",5) = "Toronto"
^mlb("AL","West") = "AL West"
^mlb("AL","West",1) = "Houston"
^mlb("AL","West",2) = "LA Angels"
^mlb("AL","West",3) = "Oakland"
^mlb("AL","West",4) = "Seattle"
^mlb("AL","West",5) = "Texas"
^mlb("NL") = "National League"
```

You can use `order()` to get the next key from a given key, as in the following examples:

```
>>> m = iris.gref('^mlb')
>>> m.order(['AL','Central'])
'East'
>>> m.order(['AL','East'])
'West'
>>> m.order(['AL','East',1])
'2'
>>> m.order(['AL','East',2])
'3'
```

Note that the starting key does not have to exist as a node in the global. Since a global is stored in sorted order, `order()` returns the key of the next node according to the sort order, for example:

```
>>> m.order(['AL','West',3.5])
'4'
```

Use a `while` loop to traverse the nodes of a global at a certain level, breaking when the return value is None. Setting the starting key to the empty string means “start at the beginning of that level.”

The following example traverses the top-level nodes of a global:

```
>>> m = iris.gref('^mlb')
>>> key = ''
>>> while True:
...     key = m.order([key])
...     if key == None:
...         break
...     print(m[key])
...
American League
National League
```

The following example traverses the third-level nodes of a global:

```
>>> m = iris.gref('^mlb')
>>> key = ''
>>> while True:
...     key = m.order(['AL','East',key])
...     if key == None:
...         break
...     print(m['AL','East',key])
...
Baltimore
Boston
NY Yankees
Tampa Bay
Toronto
```

You can nest `while` loops as necessary, or use keys() or query() to traverse an entire global.

## orderiter(key)

Returns the keys and values of a global, starting from a given key, down to the next leaf node. The starting `key` is passed as a list. Passing an empty list indicates the root node of the global.

Assume you have a global `^mlb` with the following contents:

```
^mlb = "Major League Baseball"
^mlb("AL") = "American League"
^mlb("AL","Central") = "AL Central"
^mlb("AL","East") = "AL East"
^mlb("AL","East",1) = "Baltimore"
^mlb("AL","East",2) = "Boston"
^mlb("AL","East",3) = "NY Yankees"
^mlb("AL","East",4) = "Tampa Bay"
^mlb("AL","East",5) = "Toronto"
^mlb("AL","West") = "AL West"
^mlb("AL","West",1) = "Houston"
^mlb("AL","West",2) = "LA Angels"
^mlb("AL","West",3) = "Oakland"
^mlb("AL","West",4) = "Seattle"
^mlb("AL","West",5) = "Texas"
^mlb("NL") = "National League"
```

The following example uses `orderiter()` to traverse the global down to the next leaf node starting from the root:

```
>>> m = iris.gref('^mlb')
>>> for (key, value) in m.orderiter([]):
...     print(f'{key} = {value}')
...
['AL'] = American League
['AL', 'Central'] = AL Central
```

Note that the starting key does not have to exist as a node in the global. Since a global is stored in sorted order, `orderiter()` finds the next node according to the sort order, for example:

```
>>> m = iris.gref('^mlb')
>>> for (key, value) in m.orderiter(['AL','North']):
...     print(f'{key} = {value}')
...
['AL', 'West'] = AL West
['AL', 'West', '1'] = Houston
```

## query(key)

Traverses a global starting at the specified key, returning each key and value. The starting `key` is passed as a list. Passing an empty list indicates the root node of the global.

Assume you have a global `^mlb` with the following contents:

```
^mlb = "Major League Baseball"
^mlb("AL") = "American League"
^mlb("AL","Central") = "AL Central"
^mlb("AL","East") = "AL East"
^mlb("AL","East",1) = "Baltimore"
^mlb("AL","East",2) = "Boston"
^mlb("AL","East",3) = "NY Yankees"
^mlb("AL","East",4) = "Tampa Bay"
^mlb("AL","East",5) = "Toronto"
^mlb("AL","West") = "AL West"
^mlb("AL","West",1) = "Houston"
^mlb("AL","West",2) = "LA Angels"
^mlb("AL","West",3) = "Oakland"
^mlb("AL","West",4) = "Seattle"
^mlb("AL","West",5) = "Texas"
^mlb("NL") = "National League"
```

The following example uses `query()` to traverse the global starting from the root:

```
>>> m = iris.gref('^mlb')
>>> for (key, value) in m.query([]):
...     print(f'{key} = {value}')
...
['AL'] = American League
['AL', 'Central'] = AL Central
['AL', 'East'] = AL East
['AL', 'East', '1'] = Baltimore
['AL', 'East', '2'] = Boston
['AL', 'East', '3'] = NY Yankees
['AL', 'East', '4'] = Tampa Bay
['AL', 'East', '5'] = Toronto
['AL', 'West'] = AL West
['AL', 'West', '1'] = Houston
['AL', 'West', '2'] = LA Angels
['AL', 'West', '3'] = Oakland
['AL', 'West', '4'] = Seattle
['AL', 'West', '5'] = Texas
['NL'] = National League
```

Note that the starting key does not have to exist as a node in the global. Since a global is stored in sorted order, `query()` finds the next node according to the sort order, for example:

```
>>> m = iris.gref('^mlb')
>>> for (key, value) in m.query(['AL','North']):
...     print(f'{key} = {value}')
...
['AL', 'West'] = AL West
['AL', 'West', '1'] = Houston
['AL', 'West', '2'] = LA Angels
['AL', 'West', '3'] = Oakland
['AL', 'West', '4'] = Seattle
['AL', 'West', '5'] = Texas
['NL'] = National League
```

## set(key, value)

Sets a node in a global to a given value. The `key` of the node is passed as a list, and `value` is the value to be stored. Passing a key with the value None (or an empty list) indicates the root node of the global.

The following example obtains a reference to global `^messages` and uses `set()` to set the value of some nodes in the global:

```
>>> msg = iris.gref('^messages')
>>> msg.set([None], 'list of messages')
>>> msg.set(['greeting',1], 'hello')
>>> msg.set(['greeting',2], 'goodbye')
```

If the global `^messages` did not already exist, it would look as follows:

```
^messages = "list of messages"
^messages("greeting",1) = "hello"
^messages("greeting",2) = "goodbye"
```

If `^messages` already existed, the new values would be added to the global, possibly overwriting existing data at those nodes. You can use the data() method to test whether a node already contains data before trying to set it.

You can also set a global node directly, as you would for a Python dictionary, as in the following example:

```
>>> msg = iris.gref('^messages')
>>> msg['greeting',3] = 'aloha'
```

Now the global `^messages` looks like this:

```
^messages = "list of messages"
^messages("greeting",1) = "hello"
^messages("greeting",2) = "goodbye"
^messages("greeting",3)="aloha"
```
