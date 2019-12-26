from brickschema import __version__
from brickschema.inference import TagInferenceSession, HaystackInferenceSession
import json


def test_version():
    assert __version__ == '0.0.1-alpha1'


def test_lookup_tagset():
    session = TagInferenceSession()
    assert session is not None

    tagset1 = ['AHU', 'Equipment']
    inferred, leftover = session.most_likely_tagsets(tagset1)
    assert inferred == ['AHU']
    assert len(leftover) == 0

    tagset2 = ['Air', 'Flow', 'Sensor']
    inferred, leftover = session.most_likely_tagsets(tagset2)
    assert inferred == ['Air_Flow_Sensor']
    assert len(leftover) == 0

    tagset3 = ['Air', 'Flow', 'Sensor', 'Equipment']
    inferred, leftover = session.most_likely_tagsets(tagset3)
    assert inferred == ['Air_Flow_Sensor']
    assert len(leftover) == 1


def test_haystack_inference():
    session = HaystackInferenceSession("http://example.org/carytown")
    assert session is not None
    raw_model = json.load(open('carytown.json'))
    brick_model = session.infer_model(raw_model)
    points = brick_model.query("""SELECT ?p WHERE {
        ?p rdf:type/rdfs:subClassOf* brick:Point
    }""")
    assert len(points) == 17

    equips = brick_model.query("""SELECT ?e WHERE {
        ?e rdf:type/rdfs:subClassOf* brick:Equipment
    }""")
    assert len(equips) == 2