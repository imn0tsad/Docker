from prometheus_client import CollectorRegistry, Gauge, generate_latest, push_to_gateway
import psutil
import time

# Конфигурация Pushgateway
PUSHGATEWAY_URL = 'http://ip:9091' #server ip на котором стоит compose файл
JOB_NAME = 'system_metrics'

def collect_metrics():
    registry = CollectorRegistry()
    
    
    memory_gauge = Gauge('system_memory_usage', 'Memory usage in percentage', registry=registry)
    memory_gauge.set(psutil.virtual_memory().percent)
    
  
    cpu_load_gauge = Gauge('system_cpu_load', 'CPU load in percentage', registry=registry)
    cpu_load_gauge.set(psutil.cpu_percent(interval=1))
    
    return registry

def push_metrics():
    while True:
        try:
            registry = collect_metrics()
            push_to_gateway(PUSHGATEWAY_URL, job=JOB_NAME, registry=registry)
        except Exception as e:
            print(f"Failed to push metrics to Pushgateway: {e}")
        time.sleep(15)  

if __name__ == "__main__":
    push_metrics()
