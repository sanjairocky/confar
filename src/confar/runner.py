import subprocess

from .utils import Map

# result = execute_steps(flow=flow)

# print(result)


class Runner:
    def __init__(self, data: dict) -> None:
        self.ctx: Map = Map({})
        self.data = data

    def execute_step(self, step):
        result = {'name': step['name']}
        try:
            if 'skip' in step and step['skip']:
                result['result'] = 'step skipped'
            elif 'env' in step:
                for k, v in step['env'].items():
                    self.ctx[k] = str(str(v).replace(
                        '{$.', '{')).format(**self.ctx.__dict__)
                result['result'] = 'added env'
            elif 'shell' in step:
                text = str(str(step['shell']).replace(
                    '{$.', '{')).format(**self.ctx.__dict__)
                result['result'] = subprocess.run(
                    text.split(), stdout=subprocess.PIPE).stdout
            elif 'call' in step:
                result['flows'] = self.execute_flow(flow=step['call'])
            elif 'if' in step:
                if eval(str(step['if']).replace('$.', 'self.ctx.')):
                    result['res'] = [self.execute_step(step=the)
                                     for the in step['then']]
                elif 'else' in step:
                    result['res'] = [self.execute_step(step=the)
                                     for the in step['else']]
                else:
                    result['result'] = 'step skipped'
        except Exception as e:
            result['error'] = e
        return result

    def execute_flow(self, flow='default'):
        return [self.execute_step(step=step) for step in self.data['flows'][flow]]
