# Brick 2 Electric Boogaloo

Here's the gist of how I'm doing things and what kinds of inference/modeling are enabled

## Ontology Implementation

### Complexity

Almost everything we are using falls under [OWL Lite](https://www.w3.org/TR/owl-ref/#Sublanguage-def) with the exception of the `owl:hasValue` property which we use to define a 1-1 mapping between sets of tags and names of classes.
Because of this, the current solution falls under [OWL DL](https://www.w3.org/TR/owl-ref/#hasValue-def).

This also means that we need a reasoner, but thankfully not one that supports OWL Full :).
[OWL-RL](https://owl-rl.readthedocs.io/en/latest/owlrl.html) is a nice choice that works with [RDFlib](https://github.com/RDFLib/rdflib).


```python
# G is our RDFlib Graph

# apply reasoning to expand all of the inferred triples
import owlrl
owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(G)

G.query("SELECT ?x WHERE { ?x brick:hasTag tag:Equip }")
```

We can serialize the expanded form of the graph to disk if we need to use a SPARQL query processor that does not support reasoning.

### Classes

- The Brick class namespace is `https://brickschema.org/schema/1.0.3/Brick#`
- Classes belong to `owl:Class` and are arranged into a hierarchy with `rdfs:subClassOf`
- Equivalent classes (the members of the classes are the same) are related with the `owl:equivalentClass` property
- Classes are equivalent to a set of tags

The root classes we have defined are:

- `Equipment`
- `Location`
- `Point`
- `Tag`
- `Substance`

### Tags

- Tag ontology namespace is `https://github.com/RDFLib/rdflib`
- Tags are atomic, much like in Haystack
- We use Haystack tags and define our own set
- Tags should have definitions, but this is not included yet
- Sets of tags have a 1-1 mapping with a class name



This is accomplished by declaring a Brick class (e.g. `Air_Temperature_Sensor`) as equivalent to an anonymous class, which is an `owl:Restriction` that is the intersection of entities that have certain tags.

```
# in turtle format
brick:Temperature_Sensor a owl:Class ;
    rdfs:subClassOf brick:Sensor ;
    owl:equivalentClass [ owl:intersectionOf ( 
                            [ a owl:Restriction ;
                                owl:hasValue tag:Sensor ;
                                owl:onProperty brick:hasTag 
                            ] 
                            [ a owl:Restriction ;
                                owl:hasValue tag:Temperature ;
                                owl:onProperty brick:hasTag 
                            ] 
                            [ a owl:Restriction ;
                                owl:hasValue tag:Point ;
                                owl:onProperty brick:hasTag 
                            ] 
                        ) ] .
```

The first `owl:Restriction` is the set of all classes that have `tag:Sensor` as the value for one of their `brick:hasTag` properties.

This means that a temperature sensor `:ts1` could be defined in two different ways and the reasoner would infer the other triples:

```
# using classes
:ts1   a   brick:Temperature_Sensor

# using tags
:ts1    brick:hasTag    tag:Temp
:ts1    brick:hasTag    tag:Sensor
:ts1    brick:hasTag    tag:Point
```

## Python Framework

## TODOs

- [ ] pull all tags from haystack
- [ ] add Tag definitions
