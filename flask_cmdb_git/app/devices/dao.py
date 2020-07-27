from .models import DeviceManufacturer


class MemoryModelDAO:
    def query_order_by(self, param):
        return DeviceManufacturer.query.order_by(param)