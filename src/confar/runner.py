import subprocess

from .utils import Map
from uuid import uuid4 as uuid
import copy


class Runner:
    def __init__(self, data: dict) -> None:
        self.ctx: Map = Map({})
        self.data = data
        self.seq = []

    def execute_step(self, step):
        _id = str(uuid())
        result = {'id': _id, 'name': step['name']}
        try:
            if 'skip' in step and step['skip']:
                result['result'] = 'step skipped'
                self.seq.append(result)
            elif 'env' in step:
                result['cmd'] = []
                for k, v in step['env'].items():
                    self.ctx[k] = str(str(v).replace(
                        '{$.', '{')).format(**self.ctx.__dict__)
                    result['cmd'].append(f"export {k} = {self.ctx[k]}")
                result['result'] = 'added env'
                self.seq.append(result)
            elif 'shell' in step:
                if type(step['shell']) is not list:
                    raise ValueError('Shell command must be in list')
                text = [str(str(s).replace(
                    '{$.', '{')).format(**self.ctx.__dict__) for s in step['shell']]
                result['cmd'] = f'Executing shell cmd : {text}'
                result['result'] = (subprocess.getoutput(
                    text, encoding='UTF-8')).splitlines()
                self.seq.append(result)
            elif 'call' in step:
                result['cmd'] = f'Invoking confar sub-flow : {step["call"]}'
                self.seq.append(copy.copy(result))
                result['flows'] = self.execute_steps(flow=step['call'])
            elif 'if' in step:
                self.seq.append(copy.copy(result))
                if eval(str(step['if']).replace('$.', 'self.ctx.__dict__.')):
                    result['flows'] = [self.execute_step(step=the)
                                       for the in step['then']]
                elif 'else' in step:
                    result['flows'] = [self.execute_step(step=the)
                                       for the in step['else']]
                else:
                    result['result'] = 'step skipped'
        except Exception as e:
            if 'catch' in step:
                result['flows'] = [self.execute_step(step=the)
                                   for the in step['catch']]
                result["cmd"] = f"Invoking catch flow due to error : {str(e)}"
            else:
                result['error'] = f'error : {str(e)}'
                if self.seq[len(self.seq)-1]['id'] == _id:
                    self.seq.pop()
                    self.seq.append(copy.copy(result))

        return result

    def execute_steps(self, flow='default'):
        result = []
        for step in self.data['flows'][flow]:
            res = self.execute_step(step=step)
            result.append(res)
            if 'error' in res:
                break

        return result

    def execute_flow(self, flow='default'):
        return {'id': self.data['id'], 'name': self.data['name'], 'flows': self.execute_steps(flow=flow), 'seq': self.seq}
