from typing import List


class Flow(object):
    pass


class StepError(RuntimeError):
    pass


class FieldError(RuntimeError):
    pass


class Step(object):
    def __init__(self, name: str = 'invalid step') -> None:
        self.name = name
        self.fields: List[Field] = [Field(name='name', optional=False)]

    def get_step_name(self):
        return self.name

    def run(self):
        raise StepError('Step not implemented!')

    def is_valid(self):
        raise StepError('step invalid')


class Field(object):
    def __init__(self, name: str, type=str,  optional: bool = True, value: str = None) -> None:
        self.name = name
        self.type = type
        self.value = value
        self.optional = optional

    def __repr__(self) -> str:
        return f"{self.name} = {self.value}"


class ConditionalStep(Step):

    def __init__(self, step: dict) -> None:
        super().__init__('Conditional Step')
        self.step = step
        self.fields.append(Field(name='if', optional=False))
        self.fields.append(Field(name='else'))
        self.fields.append(Field(name='then', optional=False))
        self.__parse()

    def __parse(self):
        try:
            if len(self.step) > len(self.fields) or self.__diff_keys() != 0:
                raise FieldError('Length mismatch / Invalid fields found')
            for field in self.fields:
                if field.name in self.step:
                    field.value = self.step[field.name]
                    if type(field.value) != field.type:
                        raise FieldError(
                            f'type mismatch or {field.name} exp : {field.type} got: {type(field.value)}')
                elif not field.optional:
                    raise FieldError(f'{field.name} is mandatory')
        except FieldError as e:
            raise StepError(f'Field : {str(e)}')

    def __repr__(self) -> str:
        return '\n'.join([str(f) for f in self.fields])

    def __diff_keys(self):
        return len([f for f in self.fields if f.name not in self.step])

    def run(self, context):
        return super().run()


obj = {
    'flows': {
        'first-flow': [
            {
                'name': 'conditional step',
                'if': '$.hello',
                'then': [],
                'else':[],
            },
            {'try': [
                {'name': 'calling step',
                 'call': 'call-step'}
            ],
                'catch': [{
                    'name': 'catch block of try'
                }],
                'finally': [{
                    'name': 'finally block of try'
                }]
            }
        ]
    }
}

context = {'flows': []}


step: Step = ConditionalStep({
    'name': 'conditional step',
    'if': '$.hello',
    'then': 'helo-if',
    'else': 'hello-else',
})

print(step)
# print(step.run())
