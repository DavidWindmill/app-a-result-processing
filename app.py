"""Sumidero funcional de la incubadora; su contenido NUNCA va a la plataforma."""
from fastapi import FastAPI
from pydantic import BaseModel
from qos_faults import FaultProfile
fault_profile = FaultProfile()
app = FastAPI(title='Incubator results')
processed = 0
@app.get('/health')
def health(): return {'status': 'ok'}
@app.get('/metrics')
def metrics(): return fault_profile.decorate({'status': 'ok', 'response_time_ms': 65, 'execution_time': 5, 'availability': 24, 'reliability': 0.06, 'cost': 0.1})
@app.post('/results')
def result(body: dict):
    global processed
    processed += 1
    # El resultado queda dentro de la aplicación y no se expone en el panel de gestión.
    return {'accepted': True}


@app.post('/admin/simulate')
def inject_qos_fault(payload: dict):
    """Modifica TEMPORALMENTE métricas expuestas por este contenedor real."""
    from fastapi import HTTPException
    try:
        return fault_profile.inject(payload)
    except (ValueError, TypeError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
