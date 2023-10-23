from .utils import Map, EventEmitter, Shell
from uuid import uuid4 as uuid


class Runner(EventEmitter):
    def __init__(self, data: dict) -> None:
        super().__init__()
        self.ctx: Map = Map({})
        self.data = data

    def execute_step(self, step, flow_id, confar_id):
        _id = str(uuid())
        error = False
        self.emit(
            's-start', {'id': _id, 'name': step['name'], 'flow_id': flow_id, 'confar_id': confar_id})
        try:
            if 'skip' in step and step['skip']:
                self.emit('s-data', {'id': _id, 'data': "$ skip_step",
                          'flow_id': flow_id, 'confar_id': confar_id})
                self.emit('s-data', {'id': _id, 'data': "step skipped",
                          'flow_id': flow_id, 'confar_id': confar_id})
            elif 'env' in step:
                for k, v in step['env'].items():
                    self.ctx[k] = str(str(v).replace(
                        '{$.', '{')).format(**self.ctx.__dict__)
                    cmd = f"export {k} = {self.ctx[k]}"
                    self.emit('s-data', {'id': _id, 'data': f"$ {cmd}",
                                         'flow_id': flow_id, 'confar_id': confar_id})
                self.emit('s-data', {'id': _id, 'data': 'added env',
                          'flow_id': flow_id, 'confar_id': confar_id})
            elif 'shell' in step:
                self.emit('s-data', {'id': _id, 'data': f"$ {step['shell']}",
                          'flow_id': flow_id, 'confar_id': confar_id})
                shell = Shell(cmd=str(str(step['shell']).replace(
                    '{$.', '{')).format(**self.ctx.__dict__))
                shell.on('data', lambda d: self.emit(
                    's-data', {'id': _id, 'data': d.data, 'flow_id': flow_id, 'confar_id': confar_id}))
                if shell.run():
                    raise KeyError('shell cmd failed')
            elif 'call' in step:
                self.emit(
                    's-data', {'id': _id, 'data': f"$ call {step['call']}",
                               'flow_id': flow_id, 'confar_id': confar_id})
                self.execute_steps(
                    flow=step['call'], confar_id=confar_id, flow_id=flow_id)
            elif 'if' in step:
                if eval(str(step['if']).replace('$.', 'self.ctx.__dict__.')):
                    self.emit(
                        's-data', {'id': _id, 'data': "$ invoke_if_steps",
                                   'flow_id': flow_id, 'confar_id': confar_id})
                    for the in step['then']:
                        self.execute_step(
                            step=the, flow_id=flow_id, confar_id=confar_id)
                elif 'else' in step:
                    self.emit(
                        's-data', {'id': _id, 'data': "$ invoke_else_steps",
                                   'flow_id': flow_id, 'confar_id': confar_id})
                    for the in step['else']:
                        self.execute_step(
                            step=the, flow_id=flow_id, confar_id=confar_id)
                else:
                    self.emit('s-data', {'id': _id, 'data': "skiped if_step",
                                         'flow_id': flow_id, 'confar_id': confar_id})
        except Exception as e:
            if 'catch' in step:
                self.emit('s-error', {'id': _id, 'data': f"$ invoke_catch_steps : {str(e)}",
                                      'flow_id': flow_id, 'confar_id': confar_id})
                for the in step['catch']:
                    self.execute_step(
                        step=the, flow_id=flow_id, confar_id=confar_id)
            else:

                self.emit('s-error', {'id': _id, 'data': str(e),
                                      'flow_id': flow_id, 'confar_id': confar_id})
                error = True
        self.emit('s-end', {'id': _id, 'name': step['name'],
                            'flow_id': flow_id, 'confar_id': confar_id})
        return error

    def execute_steps(self, confar_id: str, flow='default', flow_id=None):
        _id = str(uuid())
        self.emit('f-start', {'id': _id, 'confar_id': confar_id, 'flow_id': flow_id,
                  'name': flow})
        for step in self.data['flows'][flow]:
            if self.execute_step(
                    step=step, flow_id=_id, confar_id=confar_id):
                break
        self.emit('f-end', {'id': _id, 'name': flow,
                  'flow_id': flow_id, 'confar_id': confar_id})

    def execute_flow(self, confar_id: str, flow: str):
        if not confar_id:
            raise KeyError('Configuration id is required!')
        if not flow:
            raise KeyError('Bootstrap flow is required!')
        self.emit('c-start', {'id': confar_id,
                  'data': f"$ invoke_config {self.data['name']}"})
        self.execute_steps(flow=flow, confar_id=confar_id)
        self.emit('c-end', {'id': confar_id, 'name': self.data['name']})
        return self
