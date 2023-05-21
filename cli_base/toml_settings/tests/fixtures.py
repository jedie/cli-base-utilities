import dataclasses
from pathlib import Path


@dataclasses.dataclass
class SimpleExample:
    """
    A simple example
    """

    one: str = 'foo'
    two: str = 'bar'
    three: str = ''
    number: int = 123


###########################################################################################


@dataclasses.dataclass
class PathExample:
    path: Path = Path('/foo/bar')


@dataclasses.dataclass
class PathExample2:
    path: Path = Path('/foo/baz')
    sub_path: PathExample = dataclasses.field(default_factory=PathExample)


###########################################################################################


@dataclasses.dataclass
class SubClass1:
    """
    This is SubClass ONE on second level of FirstLevel
    """

    number: int = 123


@dataclasses.dataclass
class SubClass2:
    """
    This is SubClass TWO on second level of FirstLevel
    """

    something: float = 0.5


@dataclasses.dataclass
class SubClass3:
    one_value: bool = True


@dataclasses.dataclass
class ComplexExample:
    """
    This is the doc string, of the first level.
    It's two lines of doc string ;)
    """

    foo: str = 'bar'
    sub_class_one: dataclasses = dataclasses.field(default_factory=SubClass1)
    sub_class_two: dataclasses = dataclasses.field(default_factory=SubClass2)
    sub_class_three: dataclasses = dataclasses.field(default_factory=SubClass3)
