from src.confar.utils.renderer import render_result

render_result({'id': 'gdsvdsv_vdsvfd_FDvfd', 'name': 'vdvs', 'flows': [
    {
        "name": "calling flow",
        "flows": [
            {
                "name": "shell exe",
                "result": "/Users/s0a0b6e/git/confar\n"
            },
            {
                "name": "shell with env",
                "error": "KeyError('hello')"
            },
            {
                "name": "call if",
                "flows": [
                    {
                        "name": "conditional flow if",
                        "result": "step skipped"
                    }
                ]
            }
        ]
    }
]
})
